# account.py
from sqlmodel import SQLModel, select, create_engine,Field
from typing import Optional
from fastapi import HTTPException
from datetime import datetime
import random
import string

DATABASE_URL = "mysql+pymysql://root:135790Ab@127.0.0.1:3306/homework" # 数据库配置
engine = create_engine(DATABASE_URL)

class Users(SQLModel, table=True):
    user_id: Optional[int] = Field(
        default=None,
        primary_key=True,
        # sa_column_kwargs={"name": "user_id"}  # 明确指定列名
    )
    email: str = Field(index=True, unique=True)
    password: str
    role: str = "user"
    registered_at: Optional[datetime] = None

class Login:
    def __init__(self, user, session):
        self.user = user
        self.session = session

    def login(self):
        db_user = self.session.exec(select(Users).where(Users.email == self.user.email)).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="用户不存在") #若邮箱不匹配

        if not self.user.password == db_user.password:
            raise HTTPException(status_code=401, detail="密码不正确")

        return {
            "user_id": db_user.user_id,
            "email": db_user.email,
            "role": db_user.role
        }

class Register:
    def __init__(self, user, session):
        self.user = user
        self.session = session

    def generate_id(self):
        date_str = datetime.now().strftime("%Y%m%d")[2:]  # 获取当前日期，格式为 YYYYMMDD 去掉20
        random_str = ''.join(random.choices(string.digits, k=3))  # 生成指定长度的随机数字字符串
        return int(date_str + random_str)

    def register(self):
        existing_user = self.session.exec(select(Users).where(Users.email == self.user.email)).first() # 检查用户是否已存在
        if existing_user:
            raise HTTPException(status_code=400, detail="账户已经存在")
        hashed_password = self.user.password
        new_user = Users(email=self.user.email, password=hashed_password,user_id=self.generate_id()) #创建新用户

        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)

        return {"message": "User created", "user_id": new_user.user_id}

class UpdateUser:
    def __init__(self, session):
        self.session = session

    def update_user(self, user_id: int, new_email: str, new_password: str):
        db_user = self.session.exec(select(Users).where(Users.user_id == user_id)).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="用户不存在")

        # 检查新的邮箱是否被其他用户使用
        if db_user.email != new_email:
            email_check = self.session.exec(select(Users).where(Users.email == new_email)).first()
            if email_check:
                raise HTTPException(status_code=400, detail="新的邮箱已被使用")

        # 更新信息
        db_user.email = new_email
        db_user.password = new_password
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)

        return {"message": "用户信息已更新", "user_id": db_user.user_id}

