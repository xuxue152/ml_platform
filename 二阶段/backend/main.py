# main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from pydantic import BaseModel
from account import engine,Login,Register #注册与登录功能的
from manager import All_Users,All_Experiments
app = FastAPI()

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserLogin(BaseModel):
    email: str
    password: str

def get_session():
    with Session(engine) as session:
        yield session

@app.post("/api/login")
async def login(
        user: UserLogin,
        session: Session = Depends(get_session)
):
    return Login(user=user, session=session).login()

@app.post("/api/register")
async def register(
        user: UserLogin,
        session: Session = Depends(get_session)
):
    return Register(user=user, session=session).register()

@app.post("/api/all_users")
async def manager_users(session: Session = Depends(get_session)):
    users_manager = All_Users(session)
    return users_manager.get_users()

@app.delete("/api/manager_users")
async def delete_user(user_id: int, session: Session = Depends(get_session)):
    users_manager = All_Users(session)
    return users_manager.delete_user(user_id)

@app.post("/api/all_experiments")
async def manager_experiments(session: Session = Depends(get_session)):
    exp_manager = All_Experiments(session)
    return exp_manager.get_experiments()

@app.delete("/api/manager_experiments")
async def delete_experiment(experiment_id: int, session: Session = Depends(get_session)):
    exp_manager = All_Experiments(session)
    return exp_manager.delete_experiment(experiment_id)

@app.post("/api/promote_user")
async def promote_user(user_id: int, session: Session = Depends(get_session)):
    users_manager = All_Users(session)
    return users_manager.promote_user_to_admin(user_id)
