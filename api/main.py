from fastapi import FastAPI, HTTPException
from api.models import Todo, TodoCreate, TodoUpdate

app = FastAPI(title="Todo API")

todos: list[Todo] = []
next_id: int = 1


@app.get("/todos", response_model=list[Todo])
def get_todos():
    return todos


@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    todo = next((t for t in todos if t.id == todo_id), None)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo ikke fundet")
    return todo


@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(payload: TodoCreate):
    global next_id
    todo = Todo(id=next_id, **payload.model_dump())
    todos.append(todo)
    next_id += 1
    return todo


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, payload: TodoUpdate):
    todo = next((t for t in todos if t.id == todo_id), None)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo ikke fundet")
    updated = todo.model_dump()
    if payload.title is not None:
        updated["title"] = payload.title
    if payload.completed is not None:
        updated["completed"] = payload.completed
    todos[todos.index(todo)] = Todo(**updated)
    return todos[todos.index(Todo(**updated))]


@app.delete("/todos/{todo_id}", status_code=200)
def delete_todo(todo_id: int):
    todo = next((t for t in todos if t.id == todo_id), None)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo ikke fundet")
    todos.remove(todo)
    return {}
