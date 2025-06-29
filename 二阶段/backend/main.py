# main.py
from fastapi import FastAPI, Depends,File,UploadFile,Form, Path
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session,Field,Column
from pydantic import BaseModel
from account import engine,Login,Register,UpdateUser
from manager import All_Users,All_Models
from user_home import All_Projects
from user_experiment import All_Experiments
from user_dataset import All_Datasets
from user_prediction import All_Predictions
from sqlalchemy import JSON
from typing import Dict,List
import os
from fastapi.responses import ORJSONResponse
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

@app.get("/api/all_projects")
async def manager_experiments(session: Session = Depends(get_session)):
    project_manager = All_Projects(session)
    return project_manager.get_all_projects()

class ModelRequest(BaseModel):
    model_name: str

@app.get("/api/all_models")
async def get_models(session: Session = Depends(get_session)):
    models_manager = All_Models(session)
    return models_manager.get_models()

@app.post("/api/user_models")
async def get_models(session: Session = Depends(get_session)):
    models_manager = All_Models(session)
    return models_manager.get_models()

@app.delete("/api/model")
async def manager_models(data:ModelRequest,session: Session = Depends(get_session)):
    models_manager = All_Models(session)
    return models_manager.delete_model(data.model_name)

class IDRequest(BaseModel):
    user_id: int

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
    user_id: int

@app.post("/api/projects")
def get_all_projects(data : IDRequest,session: Session = Depends(get_session)):
    projects_manager = All_Projects(session)
    return projects_manager.get_projects(data.user_id)

@app.post("/api/create_project")
def create_project(data: ProjectNameRequest,session: Session = Depends(get_session)):
    projects_manager = All_Projects(session)
    return projects_manager.create_project(data.name,data.user_id)

@app.delete("/api/delete_project")
def delete_project(data: ProjectNameRequest,session: Session = Depends(get_session)):
    print("received")
    projects_manager = All_Projects(session)
    return projects_manager.delete_project(data.name,data.user_id)

class ExperimentCreate(BaseModel):
    project_name: str
    user_id: int
    name: str

class ExperimentDelete(BaseModel):
    experiment_id: int

@app.get("/api/projects/{name}/experiments")
async def get_all_experiments(name: str, user_id: int, session: Session = Depends(get_session)):
    return All_Experiments(session).get_all(user_id, name)

@app.post("/api/projects/{name}/experiments")
async def create_experiment(data: ExperimentCreate, session: Session = Depends(get_session)):
    return All_Experiments(session).create(data)

@app.delete("/api/projects/{name}/experiments")
async def delete_experiment(data: ExperimentDelete, session: Session = Depends(get_session)):
    return All_Experiments(session).delete(data.experiment_id)

class DatasetGet(BaseModel):
    user_id: int

class DatasetCreate(BaseModel):
    name: str
    user_id: int

class DatasetChange(BaseModel):
    name: str
    user_id: int
    measures: List[Dict] = Field(default=None)

@app.post("/api/projects/{project_name}/datasets")
async def get_all_datasets(
    data: DatasetGet,
    project_name: str = Path(...),
    session: Session = Depends(get_session)
):
    return All_Datasets(session).get_all(data.user_id)

@app.post("/api/datasets/{dataset_name}/show_dataset",response_class=ORJSONResponse)
async def show_dataset(
    data: DatasetCreate,
    dataset_name: str = Path(...),
    session: Session = Depends(get_session)
):
    return All_Datasets(session).show_dataset(data)

@app.post("/api/datasets/{dataset_name}/alter_dataset",response_class=ORJSONResponse)
async def alter_datasets(data: DatasetChange,dataset_name: str = Path(...),
                           session: Session = Depends(get_session)):
    return All_Datasets(session).change(data)

@app.post("/api/projects/{project_name}/create_dataset")
async def create_dataset(name: str = Form(...),user_id: int = Form(...),
file: UploadFile = File(...),project_name: str = Path(...),session: Session = Depends(get_session)):
    print('received')
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    save_path = f"uploads/{file.filename}"
    with open(save_path, "wb") as f:
        f.write(await file.read())
    data = {
        "name": name,
        "user_id": user_id,
        "file_path": save_path,
    }
    return All_Datasets(session).create(data)

@app.delete("/api/projects/{project_name}/datasets")
async def delete_dataset( data: DatasetCreate, session: Session = Depends(get_session)):
    return All_Datasets(session).delete(data.name,data.user_id)

class PredictionCreate(BaseModel):
    experiment_id: int
    model_name: str
    dataset_name: str
    user_id: int
    parameters: Dict = Field(default={}, sa_column=Column(JSON))
    metrics: Dict = Field(default={}, sa_column=Column(JSON))

class Prediction(BaseModel):
    prediction_id: int

@app.post("/api/projects/{project_name}/predictions")
def list_prediction(data: PredictionCreate, session: Session = Depends(get_session)):
    return All_Predictions(session).create(data.experiment_id)

@app.post("/api/projects/{project_name}/get_prediction")
def prediction(data: Prediction,session: Session = Depends(get_session)):
    return All_Predictions(session).get_predictions(data.prediction_id)

@app.post("/api/projects/{project_name}/run_prediction")
def prediction(data: Prediction,session: Session = Depends(get_session)):
    return All_Predictions(session).run_model(data.prediction_id)

@app.post("/api/projects/{project_name}/create_predictions")
def create_prediction(data: PredictionCreate, session: Session = Depends(get_session)):
    return All_Predictions(session).create(data)

@app.delete("/api/projects/{project_name}/predictions/{prediction_id}")
def delete_prediction(data: Prediction, session: Session = Depends(get_session)):
    return All_Predictions(session).delete(data.prediction_id)