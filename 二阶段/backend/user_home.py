# user_home.py
from sqlmodel import SQLModel, create_engine, select, Field
from typing import Optional
from fastapi import HTTPException
from datetime import datetime
from sqlmodel import Session
from sqlalchemy import text

DATABASE_URL = "mysql+pymysql://root:135790Ab@127.0.0.1:3306/homework"
engine = create_engine(DATABASE_URL)

class Projects(SQLModel, table=True):
    user_id : int
    name: str = Field(primary_key=True, max_length=100)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class All_Projects:
    def __init__(self, session: Session):
        self.session = session

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

    def delete_project(self, project_name: str, user_id: int):
        existing = self.session.exec(
            select(Projects).where(Projects.name == project_name, Projects.user_id == user_id)
        ).first()
        if not existing:
            raise HTTPException(status_code=404, detail="项目不存在")

        # 调用带 user_id 的存储过程
        self.session.connection().execute(
            text("CALL user_delete_project(:p_name, :p_user_id)"),
            {"p_name": project_name, "p_user_id": user_id}
        )
        self.session.commit()

        return {"message": f"Project '{project_name}' and related data deleted successfully"}

    def create_project(self, project_name: str,user_id: int):
        # 检查是否已存在同名项目
        existing = self.session.exec(select(Projects).where(Projects.name == project_name, Projects.user_id == user_id)).first()
        if existing:
            raise HTTPException(status_code=400, detail="项目名称已存在")
        new_project = Projects(user_id=user_id,name=project_name)
        self.session.add(new_project)
        self.session.commit()
        self.session.refresh(new_project)
        return {"message": f"Project '{project_name}' created successfully"}

