# main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from pydantic import BaseModel
from account import engine,Login,Register,UpdateUser
from manager import All_Users,All_Experiments
from user_home import All_Projects
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

@app.get("/api/all_users")
async def manager_users(session: Session = Depends(get_session)):
    users_manager = All_Users(session)
    return users_manager.get_users()

@app.get("/api/all_experiments")
async def manager_experiments(session: Session = Depends(get_session)):
    exp_manager = All_Experiments(session)
    return exp_manager.get_experiments()

class IDRequest(BaseModel):
    user_id: int

class ExperimentIDRequest(BaseModel):
    experiment_id: int

@app.post("/api/user")
async def register(
        data: IDRequest,
        session: Session = Depends(get_session)
):
    users_manager = All_Users(session)
    return users_manager.get_user(data.user_id)

@app.post("/api/promote_user")
async def promote_user(data: IDRequest, session: Session = Depends(get_session)):
    print("received")
    users_manager = All_Users(session)
    return users_manager.promote_user_to_admin(data.user_id)

@app.delete("/api/manager_users")
async def delete_user(data: IDRequest, session: Session = Depends(get_session)):
    users_manager = All_Users(session)
    return users_manager.delete_user(data.user_id)

@app.delete("/api/manager_experiments")
async def delete_experiment(data: ExperimentIDRequest, session: Session = Depends(get_session)):
    exp_manager = All_Experiments(session)
    return exp_manager.delete_experiment(data.experiment_id)

class UpdateUserRequest(BaseModel):
    user_id: int
    new_email: str
    new_password: str

@app.post("/api/update_user")
async def update_user(data: UpdateUserRequest, session: Session = Depends(get_session)):
    updater = UpdateUser(session)
    return updater.update_user(data.user_id, data.new_email, data.new_password)

class ProjectNameRequest(BaseModel):
    name: str

@app.get("/api/projects")
def get_all_projects(session: Session = Depends(get_session)):
    print('get all projects')
    projects_manager = All_Projects(session)
    return projects_manager.get_projects()

@app.post("/api/create_project")
def create_project(data: ProjectNameRequest, session: Session = Depends(get_session)):
    projects_manager = All_Projects(session)
    return projects_manager.create_project(data.name)

@app.delete("/api/delete_project")
def delete_project(data: ProjectNameRequest, session: Session = Depends(get_session)):
    projects_manager = All_Projects(session)
    return projects_manager.delete_project(data.name)