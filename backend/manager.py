# manager.py
from sqlmodel import create_engine, Session ,text,select,SQLModel,JSON,Column,Field
from fastapi import HTTPException
from sqlalchemy import CheckConstraint
from account import Users
from typing import Dict
from models_map import model_name_map

DATABASE_URL = "mysql+pymysql://root:135790Ab@127.0.0.1:3306/homework"
engine = create_engine(DATABASE_URL)

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

class Models(SQLModel, table=True):
    __table_args__ = (
        CheckConstraint("model_type IN ('classify', 'regression')", name="model_type_check"),
    )

    name: str = Field(primary_key=True, max_length=100)
    model_type: str = Field(nullable=False, max_length=50)
    parameters: Dict = Field(default=None, sa_column=Column(JSON))

class All_Models:
    def __init__(self, session: Session):
        self.session = session

    def get_models(self):
        result = self.session.exec(text("CALL get_all_models()")).all()

        # 每条记录加上对应的中文名
        models_with_chinese = []
        for row in result:
            model_dict = dict(row._mapping)  # SQLAlchemy Row -> dict
            name = model_dict.get("name")
            model_dict["chinese_name"] = model_name_map.get(name, f"未知模型（{name}）")
            models_with_chinese.append(model_dict)
        return models_with_chinese

    def delete_model(self, model_name: str):
        self.session.connection().execute(text("CALL admin_delete_model(:model_name)"),{"model_name": model_name})
        self.session.commit()
        return {"message": f"Model '{model_name}' deleted successfully"}