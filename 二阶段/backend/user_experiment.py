# user_experiment.py
from datetime import datetime
from sqlmodel import select
import random
import string
from fastapi import HTTPException
from sqlmodel import SQLModel, Field, Session
from sqlalchemy import text

def generate_id():
    date_str = datetime.now().strftime("%Y%m%d")[2:]  # 获取当前日期，格式为 YYYYMMDD 去掉20
    random_str = ''.join(random.choices(string.digits, k=3))  # 生成指定长度的随机数字字符串
    return int(date_str + random_str)

class Experiments(SQLModel, table=True):
    experiment_id: int = Field(primary_key=True)  # 注意：取消 default=None
    project_id: int = Field(nullable=False)
    user_id: int = Field(foreign_key="users.user_id", nullable=False)
    name: str = Field(max_length=100, nullable=False)

class All_Experiments:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, user_id: int, project_name: str):
        result = self.session.connection().execute(
            text("CALL get_user_experiments(:uid, :pname)"),{"uid": user_id, "pname": project_name})
        return result.fetchall()

    def create(self, data):
        exp = Experiments(
            experiment_id=generate_id(),
            project_id=data.project_id,
            user_id=data.user_id,
            name=data.name
        )
        self.session.add(exp)
        self.session.commit()
        self.session.refresh(exp)
        return exp

    def delete(self, experiment_id: int):
        # 先检查实验是否存在
        existing = self.session.exec(
            select(Experiments).where(Experiments.experiment_id == experiment_id)
        ).first()
        if not existing:
            raise HTTPException(status_code=404, detail="实验不存在")

        self.session.connection().execute(
            text("CALL user_delete_experiment(:eid)"),
            {"eid": experiment_id}
        )
        self.session.commit()
        return {"message": f"实验 {experiment_id} 已成功删除"}
