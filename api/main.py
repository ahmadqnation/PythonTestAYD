from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from api.database import engine, get_db
from api.models import Todo, TodoCreate, TodoUpdate
from api.models_db import TodoDB, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo API")


@app.get("/health")
def health_check():
    return {"status": "ok", "version": "1.0.0"}


@app.get("/todos", response_model=list[Todo])
def get_todos(db: Session = Depends(get_db)):
    return db.query(TodoDB).all()


@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo ikke fundet")
    return todo


@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(payload: TodoCreate, db: Session = Depends(get_db)):
    todo = TodoDB(**payload.model_dump())
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, payload: TodoUpdate, db: Session = Depends(get_db)):
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo ikke fundet")
    if payload.title is not None:
        todo.title = payload.title
    if payload.completed is not None:
        todo.completed = payload.completed
    db.commit()
    db.refresh(todo)
    return todo


@app.delete("/todos/{todo_id}", status_code=200)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo ikke fundet")
    db.delete(todo)
    db.commit()
    return {}
