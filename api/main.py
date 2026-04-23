from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from sqlalchemy import inspect
from sqlalchemy.orm import Session

from api.database import engine, get_db
from api.models import Todo, TodoCreate, TodoUpdate
from api.models_db import TodoDB, Base
from api.models_db_auth import UserDB  # registrerer User tabel med Base
from api.routes_auth import get_current_user, router as auth_router

Base.metadata.create_all(bind=engine)


def _auto_migrate():
    """
    Tjekker om todos tabellen har user_id kolonnen.
    Hvis ikke: drop og genskab tabellen med den opdaterede skema.
    """
    insp = inspect(engine)
    if insp.has_table("todos"):
        kolonner = [col["name"] for col in insp.get_columns("todos")]
        if "user_id" not in kolonner:
            print("Auto-migration: user_id kolonne mangler — dropper og genskaber todos tabel...")
            TodoDB.__table__.drop(bind=engine, checkfirst=True)
            TodoDB.__table__.create(bind=engine)
            print("Auto-migration fuldfoert.")
        else:
            print("Auto-migration: todos tabel er opdateret, ingen migration nødvendig.")
    else:
        print("Auto-migration: todos tabel eksisterer ikke — oprettes via create_all.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    _auto_migrate()
    yield


app = FastAPI(title="Todo API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response

app.add_middleware(SecurityHeadersMiddleware)

app.include_router(auth_router)


@app.get("/health")
def health_check():
    return {"status": "ok", "version": "1.0.0"}


@app.get("/todos", response_model=list[Todo])
def get_todos(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    return db.query(TodoDB).filter(TodoDB.user_id == current_user.id).all()


@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo ikke fundet")
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Ingen adgang til denne todo")
    return todo


@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(
    payload: TodoCreate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    todo = TodoDB(**payload.model_dump(), user_id=current_user.id)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(
    todo_id: int,
    payload: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo ikke fundet")
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Ingen adgang til denne todo")
    if payload.title is not None:
        todo.title = payload.title
    if payload.completed is not None:
        todo.completed = payload.completed
    db.commit()
    db.refresh(todo)
    return todo


@app.delete("/todos/{todo_id}", status_code=200)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo ikke fundet")
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Ingen adgang til denne todo")
    db.delete(todo)
    db.commit()
    return {}
