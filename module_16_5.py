from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Annotated
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


# CRUD запросы
# get запрос по маршруту '/'
@app.get("/")
async def main_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


# get запрос по маршруту '/users'
@app.get("/user/{user_id}")
async def get_users(
        request: Request,
        user_id: Annotated[int, Path(ge=1, le=100, description="Enter User ID", example="1")]
) -> HTMLResponse:
    for user in users:
        if int(user.id) == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": user})
    raise HTTPException(status_code=404, detail="User was not found")


# post запрос по маршруту '/user/{username}/{age}'
@app.post("/user/{username}/{age}")
async def create_users(
        username: Annotated[str, Path(min_length=5, max_length=20,
                                      description="Enter username", example="UrbanUser")],
        age: Annotated[int, Path(ge=18, le=120, description="Enter age", example="24")]) -> User:
    user_id = str(len(users) + 1)
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user


# put запрос по маршруту '/user/{user_id}/{username}/{age}'
@app.put("/user/{user_id}/{username}/{age}")
async def update_users(
        user_id: Annotated[int, Path(ge=1, le=100, description="Enter User ID", example="1")],
        username: Annotated[str, Path(min_length=5, max_length=20,
                                      description="Enter username", example="UrbanUser")],
        age: Annotated[int, Path(ge=18, le=120, description="Enter age", example="24")]) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")


# delete запрос по маршруту '/user/{user_id}'
@app.delete("/user/{user_id}")
async def delete_user(
        user_id: Annotated[int, Path(ge=1, le=100, description="Enter User ID", example="1")]):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User was not found")
