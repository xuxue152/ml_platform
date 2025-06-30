# user_home.py
from sqlmodel import SQLModel, create_engine, select, Field
from typing import Optional
from fastapi import HTTPException
from datetime import datetime
from sqlmodel import Session
from sqlalchemy import text
import random
import string

DATABASE_URL = "mysql+pymysql://root:135790Ab@127.0.0.1:3306/homework"
engine = create_engine(DATABASE_URL)

class Projects(SQLModel, table=True):
    project_id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )
    user_id : int
    name: str = Field(primary_key=True, max_length=100)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class All_Projects:
    def __init__(self, session: Session):
        self.session = session

    def generate_id(self):
        date_str = datetime.now().strftime("%Y%m%d")[2:]  # 获取当前日期，格式为 YYYYMMDD 去掉20
        random_str = ''.join(random.choices(string.digits, k=3))  # 生成指定长度的随机数字字符串
        return int(date_str + random_str)

    def get_all_projects(self):
        result = self.session.connection().execute(
            text("CALL get_all_projects()")
        )
        return result.fetchall()

    def get_projects(self, user_id: int):
        result = self.session.connection().execute(
            text("CALL get_user_projects(:user_id)"),
            {"user_id": user_id}
        )
        return result.fetchall()

    def delete_project(self, project_id: int):
        existing = self.session.exec(
            select(Projects).where(Projects.project_id == project_id)
        ).first()
        if not existing:
            raise HTTPException(status_code=404, detail="项目不存在")
        # 调用带 user_id 的存储过程
        self.session.connection().execute(
            text("CALL user_delete_project(:p_project_id)"),
            {"p_project_id": project_id}
        )
        self.session.commit()

        return {"message": f"Project '{project_id}' and related data deleted successfully"}

    def create_project(self, project_name: str,user_id: int):
        new_project = Projects(project_id = self.generate_id(),user_id=user_id,name=project_name)
        self.session.add(new_project)
        self.session.commit()
        self.session.refresh(new_project)
        return {"message": f"Project '{project_name}' created successfully"}

