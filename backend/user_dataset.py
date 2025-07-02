import pandas as pd
import numpy as np
from sklearn.preprocessing import (StandardScaler, MinMaxScaler, RobustScaler,
                                   LabelEncoder, OneHotEncoder, KBinsDiscretizer)
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
from sklearn.decomposition import PCA
from typing import Union, List, Dict,Optional
from sqlmodel import select, SQLModel, Field,Session,Column,JSON
import string
import random
from fastapi import HTTPException
from datetime import datetime
from sqlalchemy import text

class Datasets(SQLModel, table=True):
    name: str = Field(primary_key=True)
    user_id: int
    file_path: str
    uploaded_at: Optional[datetime] = None
    measures: Optional[Dict] = Field(default=None, sa_column=Column(JSON))

class All_Datasets:
    def __init__(self, session: Session):
        self.session = session

    def generate_id(self):
        date_str = datetime.now().strftime("%Y%m%d")[2:]  # 获取当前日期，格式为 YYYYMMDD 去掉20
        random_str = ''.join(random.choices(string.digits, k=3))  # 生成指定长度的随机数字字符串
        return int(date_str + random_str)

    def show_dataset(self, data):
        existing = self.session.exec(
            select(Datasets).where(
                Datasets.name == data.name,
                Datasets.user_id == data.user_id
            )
        ).first()
        if not existing:
            raise HTTPException(status_code=404, detail="数据集不存在")
        df = pd.read_csv(existing.file_path)
        df.replace([float('inf'), float('-inf')], None, inplace=True)
        df = df.where(pd.notnull(df), None)
        return df.to_dict(orient="records")


    def get_all(self, user_id: int):
        result = self.session.connection().execute(
            text("CALL get_user_datasets(:uid)"), {"uid": user_id}
        )
        return result.fetchall()

    def create(self, data):
        New_Dataset = Datasets(dataset_id=self.generate_id(),name=data['name'], user_id=data['user_id'], file_path=data['file_path'])
        self.session.add(New_Dataset)
        self.session.commit()
        self.session.refresh(New_Dataset)
        return {"message": f"数据集 {data['name']} 上传成功"}

    def delete(self, dataset_name: str, user_id: int):
        existing = self.session.exec(
            select(Datasets).where(Datasets.name == dataset_name, Datasets.user_id == user_id)
        ).first()
        if not existing:
            raise HTTPException(status_code=404, detail="数据集不存在")
        self.session.connection().execute(text("CALL user_delete_dataset(:uid, :name)"),{"uid": user_id, "name": dataset_name})
        self.session.commit()
        return {"message": f"数据集 {dataset_name} 删除成功"}

    def change(self, data):
        return DatasetService(self.session).change_dataset(data)


class DatasetService:
    def __init__(self, session):
        self.session = session


    def change_dataset(self, data):
        existing = self.session.exec(
            select(Datasets).where(
                Datasets.name == data.name,
                Datasets.user_id == data.user_id
            )
        ).first()
        if not existing:
            raise HTTPException(status_code=404, detail="数据集不存在")
        df = pd.read_csv(existing.file_path)
        processor = FeatureProcessor(df)
        try:
            processor.apply_pipeline(data.measures)  # measures 是 List[Dict] 类型，形如: [{operation: ..., args: [...], kwargs: {...}}]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))  # 返回错误详情


        processor.save(existing.file_path)
        existing.measures = data.measures

        self.session.commit()

        result = {
            "message": "数据集处理并更新成功",
            "name": data.name,
            "file_path": existing.file_path,
            "measures": data.measures
        }
        return result

class FeatureProcessor:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.label_encoders = {}
        self.onehot_encoders = {}
        self.scalers = {}
        self.feature_selectors = {}

        self.operations_map = {
            'drop': self.drop_feature,
            'fill_mean': self.fill_mean,
            'fill_median': self.fill_median,
            'fill_mode': self.fill_mode,
            'remove_outliers': self.remove_outliers,
            'one_hot': self.one_hot_encode,
            'label_encode': self.label_encode,
            'standardize': self.standardize_features,
            'normalize': self.normalize_features,
            'robust_scale': self.robust_scale_features,
            'log_transform': self.log_transform,
            'binning': self.binning,
            'pca': self.apply_pca,
            'handle_skewness': self.handle_skewness,
            'datetime_extraction': self.extract_datetime_features,
            'text_length': self.extract_text_length,
            'interaction_terms': self.create_interaction_terms,
            'polynomial_features': self.create_polynomial_features,
            'drop_duplicates': self.drop_duplicates,
            'drop_high_missing': self.drop_high_missing,
            'drop_low_variance': self.drop_low_variance,
            'target_encoding': self.target_encode,
            'transpose': self.transpose,
        }

    def apply_pipeline(self, pipeline: List[Dict]):
        for step in pipeline:
            operation = step['operation']
            args = step.get('args', [])
            kwargs = step.get('kwargs', {})
            self.apply_operation(operation, *args, **kwargs)

    def apply_operation(self, op_name: str, *args, **kwargs):
        if op_name not in self.operations_map:
            raise ValueError(f"未知操作: {op_name}. 可用操作: {list(self.operations_map.keys())}")
        return self.operations_map[op_name](*args, **kwargs)

    def get_processed_df(self) -> pd.DataFrame:
        return self.df

    def save(self, path):
        self.df.to_csv(path, index=False)

    def drop_feature(self, cols: Union[str, List[str]]):
        if isinstance(cols, str):
            cols = [cols]
        self.df.drop(columns=cols, inplace=True, errors='ignore')

    def fill_mean(self, cols: Union[str, List[str]]):
        if isinstance(cols, str):
            cols = [cols]
        for col in cols:
            self.df[col] = self.df[col].fillna(self.df[col].mean())

    def fill_median(self, cols: Union[str, List[str]]):
        if isinstance(cols, str):
            cols = [cols]
        for col in cols:
            self.df[col] = self.df[col].fillna(self.df[col].median())

    def fill_mode(self, cols: Union[str, List[str]]):
        if isinstance(cols, str):
            cols = [cols]
        for col in cols:
            mode_val = self.df[col].mode()
            self.df[col] = self.df[col].fillna(mode_val[0] if not mode_val.empty else np.nan)

    def remove_outliers(self, cols: Union[str, List[str]], method: str = 'zscore', threshold: float = 3.0):
        if isinstance(cols, str):
            cols = [cols]
        for col in cols:
            if method == 'zscore':
                z_scores = (self.df[col] - self.df[col].mean()) / self.df[col].std()
                self.df = self.df[abs(z_scores) <= threshold]
            elif method == 'iqr':
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                self.df = self.df[~((self.df[col] < (Q1 - threshold * IQR)) |
                                    (self.df[col] > (Q3 + threshold * IQR)))]

    def one_hot_encode(self, cols: Union[str, List[str]], drop_first: bool = False):
        if isinstance(cols, str):
            cols = [cols]
        for col in cols:
            encoder = OneHotEncoder(drop='first' if drop_first else None, sparse=False)
            encoded_data = encoder.fit_transform(self.df[[col]])
            encoded_cols = [f"{col}_{val}" for val in encoder.categories_[0]]
            self.df.drop(columns=[col], inplace=True)
            self.df = pd.concat([self.df,
                                 pd.DataFrame(encoded_data, columns=encoded_cols, index=self.df.index)], axis=1)
            self.onehot_encoders[col] = encoder

    def label_encode(self, cols: Union[str, List[str]]):
        if isinstance(cols, str):
            cols = [cols]
        for col in cols:
            if col not in self.df.columns:
                raise ValueError(f"列 '{col}' 不存在于数据框中")
            col_data = self.df[col].astype(str).fillna('MISSING')
            le = LabelEncoder()
            try:
                encoded = le.fit_transform(col_data)
                self.df[col] = encoded
                self.label_encoders[col] = le
            except Exception as e:
                raise ValueError(f"列 '{col}' 标签编码失败: {str(e)}")

    def standardize_features(self, cols: Union[str, List[str]]):
        if isinstance(cols, str):
            cols = [cols]
        scaler = StandardScaler()
        self.df[cols] = scaler.fit_transform(self.df[cols])
        self.scalers['standardize'] = scaler

    def normalize_features(self, cols: Union[str, List[str]]):
        if isinstance(cols, str):
            cols = [cols]
        scaler = MinMaxScaler()
        self.df[cols] = scaler.fit_transform(self.df[cols])
        self.scalers['normalize'] = scaler

    def robust_scale_features(self, cols: Union[str, List[str]]):
        if isinstance(cols, str):
            cols = [cols]
        scaler = RobustScaler()
        self.df[cols] = scaler.fit_transform(self.df[cols])
        self.scalers['robust_scale'] = scaler

    def log_transform(self, cols: Union[str, List[str]], add_small_constant: bool = True):
        if isinstance(cols, str):
            cols = [cols]
        for col in cols:
            self.df[col] = np.log1p(self.df[col]) if add_small_constant else np.log(self.df[col])

    def binning(self, cols: Union[str, List[str]], n_bins: int = 5, strategy: str = 'quantile'):
        if isinstance(cols, str):
            cols = [cols]
        for col in cols:
            binner = KBinsDiscretizer(n_bins=n_bins, encode='ordinal', strategy=strategy)
            self.df[col] = binner.fit_transform(self.df[[col]]).astype(int)

    def apply_pca(self, cols: Union[str, List[str]], n_components: int = 2, prefix: str = 'pca_'):
        if isinstance(cols, str):
            cols = [cols]
        pca = PCA(n_components=n_components)
        pca_features = pca.fit_transform(self.df[cols])
        self.df.drop(columns=cols, inplace=True)
        pca_cols = [f"{prefix}{i + 1}" for i in range(n_components)]
        self.df = pd.concat([self.df, pd.DataFrame(pca_features, columns=pca_cols, index=self.df.index)], axis=1)

    def handle_skewness(self, cols: Union[str, List[str]], threshold: float = 1.0):
        if isinstance(cols, str):
            cols = [cols]
        for col in cols:
            skewness = self.df[col].skew()
            if abs(skewness) > threshold:
                self.df[col] = np.log1p(self.df[col]) if skewness > 0 else np.square(self.df[col])

    def extract_datetime_features(self, cols: Union[str, List[str]]):
        if isinstance(cols, str):
            cols = [cols]
        for col in cols:
            self.df[col] = pd.to_datetime(self.df[col])
            self.df[f"{col}_year"] = self.df[col].dt.year
            self.df[f"{col}_month"] = self.df[col].dt.month
            self.df[f"{col}_day"] = self.df[col].dt.day
            self.df[f"{col}_hour"] = self.df[col].dt.hour
            self.df[f"{col}_dayofweek"] = self.df[col].dt.dayofweek
            self.df[f"{col}_is_weekend"] = self.df[col].dt.dayofweek >= 5
            self.df.drop(columns=[col], inplace=True)

    def extract_text_length(self, cols: Union[str, List[str]]):
        if isinstance(cols, str):
            cols = [cols]
        for col in cols:
            self.df[f"{col}_length"] = self.df[col].astype(str).apply(len)

    def create_interaction_terms(self, cols: List[str]):
        """对两个列构建交互项（乘法）"""
        if len(cols) != 2:
            raise HTTPException(status_code=500,detail="交互特征构造只能传入两个列名")
        col1, col2 = cols
        self.df[f"{col1}_x_{col2}"] = self.df[col1] * self.df[col2]

    def transpose(self, cols: List[str]):
        """
        在 DataFrame 中交换两个列的位置。
        例如：将 'col1' 和 'col2' 的列顺序互换。
        """
        if len(cols) != 2:
            raise HTTPException(status_code=500, detail="列交换只能传入两个列名")

        col1, col2 = cols

        # 校验列是否存在
        for col in [col1, col2]:
            if col not in self.df.columns:
                raise HTTPException(status_code=400, detail=f"列 {col} 不存在于数据中")

        # 获取当前列顺序
        cols_list = list(self.df.columns)

        # 获取索引
        idx1, idx2 = cols_list.index(col1), cols_list.index(col2)

        # 交换位置
        cols_list[idx1], cols_list[idx2] = cols_list[idx2], cols_list[idx1]

        # 重新排列列
        self.df = self.df[cols_list]

        print(f"已交换列顺序: {col1} <--> {col2}")


    def create_polynomial_features(self, cols: Union[str, List[str]], degree: int = 2):
        if isinstance(cols, str):
            cols = [cols]
        for col in cols:
            for d in range(2, degree + 1):
                self.df[f"{col}_power{d}"] = self.df[col] ** d

    def drop_duplicates(self):
        self.df.drop_duplicates(inplace=True)

    def drop_high_missing(self, threshold: float = 0.5):
        missing_ratio = self.df.isnull().mean()
        cols_to_drop = missing_ratio[missing_ratio > threshold].index.tolist()
        self.df.drop(columns=cols_to_drop, inplace=True)
        return cols_to_drop

    def drop_low_variance(self, threshold: float = 0.01):
        variances = self.df.var(numeric_only=True)
        cols_to_drop = variances[variances < threshold].index.tolist()
        self.df.drop(columns=cols_to_drop, inplace=True)
        return cols_to_drop

    def target_encode(self, cols: Union[str, List[str]], smooth: float = 20):
        """目标编码分类变量（最后一列为目标列）"""
        if isinstance(cols, str):
            cols = [cols]
        if len(cols) < 2:
            raise ValueError("请至少传入一个分类列和一个目标列（最后一个）")

        target = cols[-1]
        cat_cols = cols[:-1]

        global_mean = self.df[target].mean()
        for col in cat_cols:
            stats = self.df.groupby(col)[target].agg(['count', 'mean'])
            stats['smooth'] = (stats['count'] * stats['mean'] + smooth * global_mean) / (stats['count'] + smooth)
            self.df[f"{col}_encoded"] = self.df[col].map(stats['smooth'])
            self.df.drop(columns=[col], inplace=True)


