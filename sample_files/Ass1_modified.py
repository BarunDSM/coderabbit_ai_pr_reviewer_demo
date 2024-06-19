import json
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import random

FILE_NAME = "test.json"


def get_user_data():
    with open(FILE_NAME) as j_file:
        return json.load(j_file)


class UserData(BaseModel):
    username: str
    email: str
    password: str


app = FastAPI()


def create_response(status: str, user_id: int = None, message: str = None):
    response = {"status": status}
    if user_id is not None:
        response["user_id"] = user_id
    if message is not None:
        response["message"] = message
    return response


@app.post("/create")
async def create(new_user: UserData, d: dict = Depends(get_user_data)):
    l = [i for i in range(1000, 10000) if i not in d.keys()]

    if not l:
        return create_response("failure", message="No more users accepting")

    new_id = random.choice(l)
    d[new_id] = dict(new_user)

    with open(FILE_NAME, 'w+') as out:
        json.dump(d, out, indent=2)

    return create_response("success", new_id, "Your account is successfully created")


@app.get("/get/{user_id}")
async def get_user(user_id: int, d: dict = Depends(get_user_data)):
    if user_id not in d:
        raise HTTPException(status_code=404, detail=f"No user with user id {user_id}")

    return create_response("success", message="Your account details are", user_data=d[user_id])


@app.patch("/update/{user_id}")
async def update_user(user_id: int, user: UserData, d: dict = Depends(get_user_data)):
    if user_id not in d:
        raise HTTPException(status_code=404, detail=f"No user with user id {user_id}")

    d[user_id] = dict(user)

    with open(FILE_NAME, 'w+') as out:
        json.dump(d, out, indent=2)

    return create_response("success", user_id, "Your details are updated successfully")


@app.delete("/delete/{user_id}")
async def delete_user(user_id: int, d: dict = None):
    if d is None:
        d = get_user_data()
    if user_id not in d:
        raise HTTPException(status_code=404, detail=f"No user with user id {user_id}")

    del d[user_id]

    with open(FILE_NAME, 'w+') as out:
        json.dump(d, out, indent=2)

    return create_response("success", user_id, "Your account is now deleted")
