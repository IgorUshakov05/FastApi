from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создаем экземпляр приложения FastAPI
app = FastAPI()

# Настройки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все источники
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "mysql+mysqlconnector://root:Qwerty@localhost/todos"  # Замените на свои данные
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Модель Todo
class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    complite = Column(Boolean, default=False)

# Создание таблицы в базе данных
Base.metadata.create_all(bind=engine)

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD-операции

@app.get("/todo")
def todos_get():
    db = next(get_db())
    todos = db.query(Todo).all()
    return todos

@app.get("/todo/{id}")
def get_todo(id: int):
    db = next(get_db())
    todo = db.query(Todo).filter(Todo.id == id).first()
    if not todo:
        raise HTTPException(status_code=404, detail=f"Item with id {id} not found")
    return todo

@app.post("/todo")
async def todos_create(request: Request):
    new_todo = await request.json()
    db = next(get_db())
    todo_item = Todo(title=new_todo.get("title", ""), complite=False)
    db.add(todo_item)
    db.commit()
    db.refresh(todo_item)
    return {"success": True, "new_item": todo_item}

@app.delete("/todo")
async def delete_todo(request: Request):
    id = await request.json()
    db = next(get_db())
    todo = db.query(Todo).filter(Todo.id == id.get("id", "")).first()
    if not todo:
        raise HTTPException(status_code=404, detail=f"Item with id {id} not found")
    db.delete(todo)
    db.commit()
    return {"message": f"Item with id {id} deleted", "removed_item": todo}

@app.put("/todo")
async def set_complite(request: Request):
    body = await request.json()
    db = next(get_db())
    todo = db.query(Todo).filter(Todo.id == body.get('id', '')).first()
    if not todo:
        raise HTTPException(status_code=404, detail=f"Item with id {body.get('id')} not found")
    todo.complite = True
    db.commit()
    db.refresh(todo)
    return {"success": True, "item": todo}