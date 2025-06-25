# user_home.py
from sqlmodel import SQLModel, create_engine, select, Field
from typing import Optional
from fastapi import HTTPException
from datetime import datetime
from sqlalchemy import text

DATABASE_URL = "mysql+pymysql://root:135790Ab@127.0.0.1:3306/homework"
engine = create_engine(DATABASE_URL)

class Projects(SQLModel, table=True):
    __tablename__ = "projects"
    name: str = Field(primary_key=True, max_length=100)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

from sqlmodel import Session
from sqlalchemy import text

class All_Projects:
    def __init__(self, session: Session):
        self.session = session

    def get_projects(self):
        result = self.session.exec(text("SELECT * FROM projects"))
        return result.all()

    def delete_project(self, project_name: str):
        existing = self.session.exec(select(Projects).where(Projects.name == project_name)).first()
        if not existing:
            raise HTTPException(status_code=404, detail="项目不存在")

        # 改为 SQLAlchemy Core 写法
        self.session.connection().execute(
            text("CALL user_delete_project(:p_name)"),
            {"p_name": project_name}
        )
        self.session.commit()

        return {"message": f"Project '{project_name}' and related data deleted successfully"}

    def create_project(self, project_name: str):
        # 检查是否已存在同名项目
        existing = self.session.exec(select(Projects).where(Projects.name == project_name)).first()
        if existing:
            raise HTTPException(status_code=400, detail="项目名称已存在")
        new_project = Projects(name=project_name)
        self.session.add(new_project)
        self.session.commit()
        self.session.refresh(new_project)
        return {"message": f"Project '{project_name}' created successfully"}