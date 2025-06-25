# manager.py

from sqlmodel import SQLModel, create_engine, Session, Field, text,select
from typing import Optional
from fastapi import HTTPException
from datetime import date
from account import Users

DATABASE_URL = "mysql+pymysql://root:135790Ab@127.0.0.1:3306/homework"
engine = create_engine(DATABASE_URL)


class Experiments(SQLModel, table=True):
    __tablename__ = "experiments"
    experiment_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    name: str
    date: date
    status: str
    parameters: Optional[str] = None
    result: Optional[str] = None

class All_Users:
    def __init__(self, session: Session):
        self.session = session

    def get_users(self):
        # Using the admin_user_view instead of direct table query
        result = self.session.exec(text("SELECT * FROM admin_user_view"))
        return result.all()

    def get_user(self,user_id:int):
        db_user = self.session.exec(select(Users).where(Users.user_id == user_id)).first()
        return db_user

    def delete_user(self, user_id: int):
        # Using the stored procedure instead of direct deletion
        self.session.exec(text(f"CALL admin_delete_user({user_id})"))
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
        # Using the admin_experiment_view instead of direct table query
        result = self.session.exec(text("SELECT * FROM admin_experiment_view"))
        return result.all()

    def delete_experiment(self, experiment_id: int):
        exp = self.session.get(Experiments, experiment_id)
        if not exp:
            raise HTTPException(status_code=404, detail="Experiment not found")
        self.session.delete(exp)
        self.session.commit()
        return {"message": f"Experiment {experiment_id} deleted successfully"}

    def get_experiment_stats(self):
        # Using the user_experiment_stats view
        result = self.session.exec(text("SELECT * FROM user_experiment_stats"))
        return result.all()