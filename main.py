from fastapi import FastAPI,Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
todos = [
    {"id": 0, "title": "Помыть полы", "complite": False},
    {"id": 1, "title": "Написать пз", "complite": False},
    {"id": 2, "title": "Запушить на гитхаб", "complite": False},
    {"id": 4, "title": "Улыбнуться", "complite": False},
    {"id": 5, "title": "Потянуться", "complite": False}
]

def find_item_by_id(items, target_id):
    
    return None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/todo")
def todos_get():
    return todos

@app.get("/todo/{id}")
def get_todo(id: int):
    for item in todos:
        if item["id"] == id:
            return item  
    raise HTTPException(status_code=404, detail=f"Item with id {id} not found")


@app.post("/todo")
async def todos_create(request: Request):
    new_todo = await request.json()  
    todo_item = {
        "id": len(todos),  
        "title": new_todo.get("title", ""),
        "complite": False
    }
    todos.append(todo_item)  
    return {"success": True, "new_item": todo_item}  

@app.delete("/todo")
async def delete_todo(request: Request):
    id = await request.json()
    for i, item in enumerate(todos):
        if item["id"] == id.get("id", ""):
            removed_item = todos.pop(i)  
            return {"message": f"Item with id {id} deleted", "removed_item": removed_item}
    
    raise HTTPException(status_code=404, detail=f"Item with id {id} not found")


@app.put("/todo")
async def set_complite(request: Request):
    body = await request.json()
    for item in todos:
        if item["id"] == body.get('id', ''):
            item["complite"] = True
            return {"success": True, "item":item}
    raise HTTPException(status_code=404, detail=f"Item with id {id} not found")