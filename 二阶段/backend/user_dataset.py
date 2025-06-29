import pandas as pd
import numpy as np
from sklearn.preprocessing import (StandardScaler, MinMaxScaler, RobustScaler,
                                   LabelEncoder, OneHotEncoder, KBinsDiscretizer)
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
from sklearn.decomposition import PCA
from typing import Union, List, Dict,Optional
from sqlmodel import select, SQLModel, Field,Session
import logging
from functools import wraps
from fastapi import HTTPException
from datetime import datetime
from sqlalchemy import text

class Datasets(SQLModel, table=True):
    name: str = Field(primary_key=True)
    user_id: int
    file_path: str
    uploaded_at: Optional[datetime] = None

class All_Datasets:
    def __init__(self, session: Session):
        self.session = session

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
        New_Dataset = Datasets(name=data['name'], user_id=data['user_id'], file_path=data['file_path'])
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
            raise HTTPException(status_code=500, detail=f"特征处理失败: {str(e)}")

        new_path = existing.file_path.replace(".csv", "_processed.csv")
        processor.save(new_path)

        existing.file_path = new_path
        existing.measures = data.measures
        self.session.commit()

        return {
            "message": "数据集处理并更新成功",
            "name": data.name,
            "new_file_path": new_path,
            "measures": data.measures
        }

class FeatureProcessor:
    def __init__(self, df: pd.DataFrame):
        """初始化特征处理器"""
        self.df = df.copy()
        self.label_encoders = {}
        self.onehot_encoders = {}
        self.scalers = {}
        self.feature_selectors = {}

        # 操作名称到方法的映射
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
        }

    def apply_pipeline(self, pipeline: List[Dict]):
        """应用预定义的处理流程"""
        for step in pipeline:
            operation = step['operation']
            args = step.get('args', [])
            kwargs = step.get('kwargs', {})
            self.apply_operation(operation, *args, **kwargs)

    def apply_operation(self, op_name: str, *args, **kwargs):
        """执行单个特征处理操作"""
        if op_name not in self.operations_map:
            raise ValueError(f"未知操作: {op_name}. 可用操作: {list(self.operations_map.keys())}")
        return self.operations_map[op_name](*args, **kwargs)

    def get_processed_df(self) -> pd.DataFrame:
        """获取处理后的数据框"""
        return self.df

    def save(self, path):
        """保存处理后的数据到CSV文件"""
        self.df.to_csv(path, index=False)

    def drop_feature(self, cols: Union[str, List[str]]):
        """删除指定列"""
        if isinstance(cols, str):
            cols = [cols]
        self.df.drop(columns=cols, inplace=True, errors='ignore')

    def fill_mean(self, col: str):
        """用均值填充缺失值"""
        self.df[col] = self.df[col].fillna(self.df[col].mean())

    def fill_median(self, col: str):
        """用中位数填充缺失值"""
        self.df[col] = self.df[col].fillna(self.df[col].median())

    def fill_mode(self, col: str):
        """用众数填充缺失值"""
        mode_val = self.df[col].mode()
        self.df[col] = self.df[col].fillna(mode_val[0] if not mode_val.empty else np.nan)


    def remove_outliers(self, col: str, method: str = 'zscore', threshold: float = 3.0):
        """移除异常值"""
        if method == 'zscore':
            z_scores = (self.df[col] - self.df[col].mean()) / self.df[col].std()
            self.df = self.df[abs(z_scores) <= threshold]
        elif method == 'iqr':
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            self.df = self.df[~((self.df[col] < (Q1 - threshold * IQR)) |
                                (self.df[col] > (Q3 + threshold * IQR)))]

    def one_hot_encode(self, col: str, drop_first: bool = False):
        """对分类变量进行独热编码"""
        encoder = OneHotEncoder(drop='first' if drop_first else None, sparse=False)
        encoded_data = encoder.fit_transform(self.df[[col]])
        encoded_cols = [f"{col}_{val}" for val in encoder.categories_[0]]

        self.df.drop(columns=[col], inplace=True)
        self.df = pd.concat([
            self.df,
            pd.DataFrame(encoded_data, columns=encoded_cols, index=self.df.index)
        ], axis=1)
        self.onehot_encoders[col] = encoder

    def label_encode(self, col: str):
        """对分类变量进行标签编码"""
        le = LabelEncoder()
        self.df[col] = le.fit_transform(self.df[col].astype(str))
        self.label_encoders[col] = le

    def standardize_features(self, cols: Union[str, List[str]]):
        """标准化数值特征(均值0,方差1)"""
        if isinstance(cols, str):
            cols = [cols]
        scaler = StandardScaler()
        self.df[cols] = scaler.fit_transform(self.df[cols])
        self.scalers['standardize'] = scaler

    def normalize_features(self, cols: Union[str, List[str]]):
        """归一化数值特征到[0,1]范围"""
        if isinstance(cols, str):
            cols = [cols]
        scaler = MinMaxScaler()
        self.df[cols] = scaler.fit_transform(self.df[cols])
        self.scalers['normalize'] = scaler

    def robust_scale_features(self, cols: Union[str, List[str]]):
        """鲁棒缩放数值特征(抗异常值)"""
        if isinstance(cols, str):
            cols = [cols]
        scaler = RobustScaler()
        self.df[cols] = scaler.fit_transform(self.df[cols])
        self.scalers['robust_scale'] = scaler

    def log_transform(self, cols: Union[str, List[str]], add_small_constant: bool = True):
        """对数值特征进行对数变换"""
        if isinstance(cols, str):
            cols = [cols]
        for col in cols:
            self.df[col] = np.log1p(self.df[col]) if add_small_constant else np.log(self.df[col])

    def binning(self, col: str, n_bins: int = 5, strategy: str = 'quantile'):
        """将连续变量分箱离散化"""
        binner = KBinsDiscretizer(n_bins=n_bins, encode='ordinal', strategy=strategy)
        self.df[col] = binner.fit_transform(self.df[[col]]).astype(int)

    def apply_pca(self, cols: Union[str, List[str]], n_components: int = 2, prefix: str = 'pca_'):
        """应用PCA降维"""
        if isinstance(cols, str):
            cols = [cols]
        pca = PCA(n_components=n_components)
        pca_features = pca.fit_transform(self.df[cols])
        self.df.drop(columns=cols, inplace=True)
        pca_cols = [f"{prefix}{i + 1}" for i in range(n_components)]
        self.df = pd.concat([
            self.df,
            pd.DataFrame(pca_features, columns=pca_cols, index=self.df.index)
        ], axis=1)

    def handle_skewness(self, cols: Union[str, List[str]], threshold: float = 1.0):
        """处理数值特征的偏态"""
        if isinstance(cols, str):
            cols = [cols]
        for col in cols:
            skewness = self.df[col].skew()
            if abs(skewness) > threshold:
                self.df[col] = np.log1p(self.df[col]) if skewness > 0 else np.square(self.df[col])

    def extract_datetime_features(self, col: str):
        """从日期时间列提取特征"""
        self.df[col] = pd.to_datetime(self.df[col])
        self.df[f"{col}_year"] = self.df[col].dt.year
        self.df[f"{col}_month"] = self.df[col].dt.month
        self.df[f"{col}_day"] = self.df[col].dt.day
        self.df[f"{col}_hour"] = self.df[col].dt.hour
        self.df[f"{col}_dayofweek"] = self.df[col].dt.dayofweek
        self.df[f"{col}_is_weekend"] = self.df[col].dt.dayofweek >= 5
        self.df.drop(columns=[col], inplace=True)

    def extract_text_length(self, col: str):
        """提取文本长度特征"""
        self.df[f"{col}_length"] = self.df[col].astype(str).apply(len)

    def create_interaction_terms(self, cols: List[List[str]]):
        """创建特征交互（乘法）"""
        for group in cols:
            if len(group) < 2:
                continue
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    col1, col2 = group[i], group[j]
                    self.df[f"{col1}_x_{col2}"] = self.df[col1] * self.df[col2]

    def create_polynomial_features(self, cols: Union[str, List[str]], degree: int = 2):
        """转为平方"""
        if isinstance(cols, str):
            cols = [cols]
        for col in cols:
            for d in range(2, degree + 1):
                self.df[f"{col}_power{d}"] = self.df[col] ** d

    def drop_duplicates(self):
        """删除重复行"""
        self.df.drop_duplicates(inplace=True)

    def drop_high_missing(self, threshold: float = 0.5):
        """删除高缺失率列"""
        missing_ratio = self.df.isnull().mean()
        cols_to_drop = missing_ratio[missing_ratio > threshold].index.tolist()
        self.df.drop(columns=cols_to_drop, inplace=True)
        return cols_to_drop

    def drop_low_variance(self, threshold: float = 0.01):
        """删除低方差列"""
        variances = self.df.var(numeric_only=True)
        cols_to_drop = variances[variances < threshold].index.tolist()
        self.df.drop(columns=cols_to_drop, inplace=True)
        return cols_to_drop

    def target_encode(self, col: str, target: str, smooth: float = 20):
        """目标编码分类变量"""
        global_mean = self.df[target].mean()
        stats = self.df.groupby(col)[target].agg(['count', 'mean'])
        stats['smooth'] = (stats['count'] * stats['mean'] + smooth * global_mean) / (stats['count'] + smooth)
        self.df[f"{col}_encoded"] = self.df[col].map(stats['smooth'])
        self.df.drop(columns=[col], inplace=True)
