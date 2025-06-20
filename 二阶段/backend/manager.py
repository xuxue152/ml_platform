# manager.py

from sqlmodel import SQLModel, select, create_engine, Session, Field
from typing import Optional, List
from fastapi import HTTPException
from datetime import datetime, date

DATABASE_URL = "mysql+pymysql://root:135790Ab@127.0.0.1:3306/homework"
engine = create_engine(DATABASE_URL)

class Users(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True, sa_column_kwargs={"name": "user_id"})
    email: str = Field(index=True, unique=True)
    password: str
    role: str = "user"
    registered_at: Optional[datetime] = None

class Experiments(SQLModel, table=True):
    experiment_id: Optional[int] = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True, "name": "experiment_id"})
    user_id: int = Field(foreign_key="users.user_id", nullable=False, sa_column_kwargs={"ondelete": "CASCADE"})
    name: str = Field(max_length=100, nullable=False)
    date: date = Field(nullable=False)
    status: str = Field(nullable=False, sa_column_kwargs={"check": "status IN ('completed','training','failed')"})
    parameters: Optional[str] = None
    result: Optional[str] = None

class All_Users:
    def __init__(self, session: Session):
        self.session = session

    def get_users(self):
        return self.session.exec(select(Users)).all()

    def delete_user(self, user_id: int):
        user = self.session.get(Users, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        self.session.delete(user)
        self.session.commit()
        return {"message": f"User {user_id} deleted successfully"}

    def promote_user_to_admin(self, user_id: int):
        user = self.session.get(Users, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.role = "admin"
        self.session.add(user)
        self.session.commit()
        return {"message": f"User {user_id} promoted to admin"}


class All_Experiments:
    def __init__(self, session: Session):
        self.session = session

    def get_experiments(self):
        return self.session.exec(select(Experiments)).all()

    def delete_experiment(self, experiment_id: int):
        exp = self.session.get(Experiments, experiment_id)
        if not exp:
            raise HTTPException(status_code=404, detail="Experiment not found")
        self.session.delete(exp)
        self.session.commit()
        return {"message": f"Experiment {experiment_id} deleted successfully"}
