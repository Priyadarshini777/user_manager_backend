from fastapi import FastAPI, HTTPException
from app.models import User


app = FastAPI(title="User Manager API")


users = {}


@app.get("/")
def root():
    return {"message": "Welcome to User Manager API!"}


@app.post("/users")
def create_user(user: User):
    if user.id in users:
        raise HTTPException(status_code=400, detail="User already exists")
    users[user.id] = user.dict()
    return {"message": "User created successfully", "user": users[user.id]}


@app.get("/users")
def get_all_users():
    return {"users": list(users.values())}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    deleted_user = users.pop(user_id)
    return {"message": "User deleted successfully", "user": deleted_user}
