# user_prediction.py
from sqlmodel import Column
from datetime import datetime
from sqlmodel import select
from sqlalchemy import JSON,CheckConstraint
import random
import string
from fastapi import HTTPException
from sqlmodel import SQLModel, Field, Session
from typing import Optional
from sqlalchemy import text
import pandas as pd
import os, json
from typing import Dict
from sklearn.model_selection import train_test_split
from models_map import params_map, sklearn_model_map
from sklearn.metrics import (
    accuracy_score, f1_score, precision_score, recall_score,
    roc_auc_score, log_loss, confusion_matrix, classification_report,
    mean_squared_error, mean_absolute_error, r2_score,
    explained_variance_score, median_absolute_error
)

def generate_id():
    date_str = datetime.now().strftime("%Y%m%d")[2:]  # 获取当前日期，格式为 YYYYMMDD 去掉20
    random_str = ''.join(random.choices(string.digits, k=3))  # 生成指定长度的随机数字字符串
    return int(date_str + random_str)

class ModelRunner:
    @staticmethod
    def validate_params(model_name: str, given_params: Dict) -> Dict:
        """检查传入的模型参数是否合法，并返回经过验证的参数字典"""
        if model_name not in params_map:
            raise ValueError(f"模型参数未定义: {model_name}")

        valid_params = params_map[model_name]
        validated = {}

        for key, val in given_params.items():
            if key not in valid_params:
                raise ValueError(f"无效参数: {key} 不属于模型 {model_name}")
            # 检查值是否在备选项中（支持范围[最小值, 最大值]）
            allowed = valid_params[key]
            if isinstance(allowed, list) and len(allowed) == 2 and isinstance(allowed[0], (int, float)):
                # 范围型数值参数
                if not (allowed[0] <= val <= allowed[1]):
                    raise ValueError(f"参数 {key}={val} 不在有效范围 {allowed} 内")
            elif isinstance(allowed, list) and val not in allowed:
                raise ValueError(f"参数 {key} 的值 {val} 不在允许值 {allowed} 中")
            validated[key] = val

        return validated

    @staticmethod
    def run_model(model_name, params, metrics, file_path: str,user_id):
        # 读取数据
        df = pd.read_csv(file_path)
        X = df.iloc[:, :-1]
        y = df.iloc[:, -1]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # 验证模型存在与参数合法性
        if model_name not in sklearn_model_map:
            raise ValueError(f"模型名称无效: {model_name}")

        validated_params = ModelRunner.validate_params(model_name, params)

        # 实例化模型
        model_cls = sklearn_model_map[model_name]
        model = model_cls(**validated_params)

        # 模型训练与预测
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        # 评估指标
        metric_funcs = {
            # 分类指标
            "accuracy": accuracy_score,  # 准确率
            "f1": f1_score,  # F1 值
            "precision": precision_score,  # 精确率
            "recall": recall_score,  # 召回率
            "roc_auc": roc_auc_score,  # AUC（仅二分类或需要 y_proba）
            "log_loss": log_loss,  # 对数损失
            "confusion_matrix": confusion_matrix,  # 混淆矩阵（用于可视化）
            "classification_report": classification_report,  # 文本报告（通常用于打印）

            # 回归指标
            "mse": mean_squared_error,  # 均方误差
            "mae": mean_absolute_error,  # 平均绝对误差
            "r2": r2_score,  # R² 决定系数
            "explained_variance": explained_variance_score,  # 可解释方差
            "median_absolute_error": median_absolute_error  # 中位绝对误差
        }

        computed_metrics = {}
        for metric_name, enabled in metrics.items():
            if enabled and metric_name in metric_funcs:
                try:
                    if metric_name == "f1":
                        computed_metrics[metric_name] = f1_score(y_test, y_pred, average='weighted')
                    else:
                        computed_metrics[metric_name] = metric_funcs[metric_name](y_test, y_pred)
                except Exception as e:
                    computed_metrics[metric_name] = f"Error: {str(e)}"

        # 保存结果
        uid = user_id
        base_dir = "results"
        os.makedirs(base_dir, exist_ok=True)

        result_path = os.path.join(base_dir, f"{uid}_result.csv")
        report_path = os.path.join(base_dir, f"{uid}_report.json")

        pd.DataFrame({
            "true": y_test,
            "predicted": y_pred
        }).to_csv(result_path, index=False)

        # 保存指标
        full_metrics = {}
        for metric_name, enabled in metrics.items():
            if enabled:
                full_metrics[metric_name] = computed_metrics.get(metric_name, "未计算")
            else:
                full_metrics[metric_name] = False

        with open(report_path, "w", encoding='utf-8') as f:
            json.dump(full_metrics, f, ensure_ascii=False, indent=2)

        return {
            "result_path": result_path,
            "report_path": report_path,
            "metrics": full_metrics
        }

class Prediction(SQLModel, table=True):
    prediction_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    experiment_id: Optional[int] = Field(default=None, foreign_key="experiments.experiment_id")
    model_name: str = Field(max_length=100, foreign_key="models.name")
    dataset_name: str = Field(max_length=100, foreign_key="datasets.name")
    user_id: int = Field(foreign_key="users.user_id")
    parameters: Optional[Dict] = Field(default={}, sa_column=Column(JSON))
    status: str = Field(nullable=False, max_length=20)
    metrics: Dict = Field(default={}, sa_column=Column(JSON))
    predicted_at: Optional[datetime] = Field(default=None)

class All_Predictions:
    def __init__(self, session: Session):
        self.session = session

    def return_address(self, dataset_name: str, user_id: int) -> str:
        conn = self.session.connection()
        conn.execute(text("CALL get_dataset_path(:p_dataset_name, :p_user_id, @file_path)"),
                     {"p_dataset_name": dataset_name, "p_user_id": user_id})
        return conn.execute(text("SELECT @file_path")).scalar()

    def run_model(self, prediction_id: int):
        try:
            prediction = self.session.exec(select(Prediction).where(Prediction.prediction_id == prediction_id)).first()
            if not prediction:
                raise HTTPException(status_code=404, detail="预测记录不存在")
            prediction.status = "training"
            self.session.add(prediction)
            self.session.commit()
            dataset_name = prediction.dataset_name
            user_id = prediction.user_id
            address = self.return_address(dataset_name, user_id)
            result = ModelRunner.run_model(prediction.model_name, prediction.parameters,
                                                   prediction.metrics, address,prediction.user_id)
            result_metrics=result["metrics"]
            result_path=result["result_path"]
            report_path=result["report_path"]
            prediction.status = "completed"
            prediction.metrics = result_metrics
            prediction.predicted_at = datetime.now()
            self.session.add(prediction)
            self.session.commit()
            return {"message": "模型执行成功", "metrics": result_metrics}

        except Exception as e:
            # 设置失败状态
            try:
                prediction.status = "failed"
                self.session.add(prediction)
                self.session.commit()
            except:
                pass
            raise HTTPException(status_code=500, detail=f"模型运行失败: {str(e)}")

    def create(self, data):
        try:
            New_Prediction = Prediction(prediction_id=generate_id(),experiment_id=data.experiment_id,
            model_name=data.model_name,dataset_name=data.dataset_name,user_id=data.user_id,
            parameters=data.parameters,status='pending',metrics=data.metrics,name=data.name)
            self.session.add(New_Prediction)
            self.session.commit()
            self.session.refresh(New_Prediction)
            return {"message": "预测记录添加成功"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"添加预测失败: {str(e)}")

    def delete(self, prediction_id: int):
        try:
            conn = self.session.connection()
            conn.execute(text("CALL user_delete_prediction(:p_prediction_id)"),{"p_prediction_id": prediction_id})
            self.session.commit()
            return {"message": f"预测记录 {prediction_id} 删除成功"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"删除失败: {str(e)}")

    def get_predictions(self, experiment_id: int):
        try:
            conn = self.session.connection()
            result = conn.execute(text("CALL get_predictions(:p_experiment_id)"),{"p_experiment_id": experiment_id})
            rows = result.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取失败: {str(e)}")