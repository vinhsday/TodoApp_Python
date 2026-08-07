
from webbrowser import get

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import Base, SessionLocal, engine
from enums.priority import PriorityEnum
from models.new_task import Task
from models.user import User
from schemas import TaskUpdate
from schemas.CompleteRequest import CompleteRequest
from schemas.TaskResponse import TaskResponse
from schemas.Token import Token
from security import ALGORITHM, SECRET_KEY, create_access_token
from services.todo_app import TodoApp
from schemas.TaskCreate import TaskCreate
from schemas.UserResponse import UserResponse
from services.todo_service import TodoService
from schemas.UserCreate import UserCreate
from schemas.LoginRequest import LoginRequest
from schemas.TaskUpdate import TaskUpdate
from jose import JWTError, jwt
from security import oauth2_scheme
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_todo_service(db: Session = Depends(get_db)):
    return TodoService(db)

def get_current_user(service: TodoService = Depends(get_todo_service), token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )
    return service.get_user_by_username(payload["sub"])

@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(completed: bool | None = None,
               search: str | None = None,
               sort: str | None = None,
               service: TodoService = Depends(get_todo_service), user: User = Depends(get_current_user)):
    return service.get_tasks(user=user,
                              completed=completed,
                              search=search,
                              sort=sort)


        
@app.post("/tasks", response_model=TaskResponse)
def post_tasks(task: TaskCreate, service: TodoService = Depends(get_todo_service), user: User = Depends(get_current_user)):
    return service.add_task(task.title, user, task.deadline)

@app.get("/tasks/{id}", response_model=TaskResponse)
def get_task(id: int, service: TodoService = Depends(get_todo_service), user: User = Depends(get_current_user)):
    try: 
        return service.get_task(id, user)
    except IndexError:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
@app.delete("/tasks/{id}", response_model=TaskResponse)
def delete_task(id: int, service: TodoService = Depends(get_todo_service), user: User = Depends(get_current_user)):
    try: 
        return service.delete_task(id, user)
    except IndexError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

# @app.get("/users/{id}", response_model=UserResponse)
# def get_user(id: int, service: TodoService = Depends(get_todo_service)):
#     try:
#         return service.get_user(id)
#     except IndexError as e:
#         raise HTTPException(
#             status_code=404,
#             detail=str(e)
#         )

# @app.get("/users", response_model=list[UserResponse])
# def get_users(service: TodoService = Depends(get_todo_service)):
#     return service.get_users()

# @app.get("/users/{user_id}/tasks/", response_model=list[TaskResponse])
# def get_user_task(user_id: int,service: TodoService=Depends(get_todo_service)):
#     return service.get_user_tasks(user_id)

@app.post("/users/register", response_model=UserResponse)
def register(user: UserCreate, service: TodoService=Depends(get_todo_service)):
    try:
        return service.register_user(user)
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )

@app.post("/users/login", response_model=Token)
def login(request: OAuth2PasswordRequestForm = Depends(), service: TodoService=Depends(get_todo_service)):
    try:
        user = service.login(request.username, request.password)
        token = create_access_token({
            "sub": user.username
        })
        return {
            "access_token": token,
            "token_type": "bearer"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )
    
@app.patch("/tasks/{task_id}")
def update_task(task_id: int,
                request: TaskUpdate,
                service: TodoService = Depends(get_todo_service), 
                user: User = Depends(get_current_user)
                ):
    try:
        return service.update_task(task_id, request, user)
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )


@app.post("/test-transaction")
def test(title: str, user_id: int):
    task = Task(
        title=title,
        user_id=user_id
    )

    db = SessionLocal()
    db.add(task)
    db.flush()

    print("ID:", task.id)
    db.rollback()
    return {
        "id": task.id
    }

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend") 

