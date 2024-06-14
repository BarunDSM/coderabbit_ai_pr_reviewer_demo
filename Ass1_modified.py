import json
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import random
from typing import Dict, Any

FILE_NAME = "test.json"

# Returns dictionary read from the json file
def get_user_data() -> Dict[int, Any]:
    try:
        with open(FILE_NAME, 'r') as j_file:
            return json.load(j_file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

# Saves the dictionary back to the json file
def save_user_data(data: Dict[int, Any]) -> None:
    with open(FILE_NAME, 'w') as out_file:
        json.dump(data, out_file, indent=2)

# Standard response format
def standard_response(status: str, message: str, user_id: int = None, data: Any = None) -> Dict[str, Any]:
    response = {
        "status": status,
        "message": message,
    }
    if user_id is not None:
        response["user_id"] = user_id
    if data is not None:
        response["data"] = data
    return response

# User class defining their attributes
class UserData(BaseModel):
    username: str
    email: str
    password: str

app = FastAPI()

# Create a new user account
@app.post("/create")
async def create(new_user: UserData, data: Dict[int, Any] = Depends(get_user_data)):
    available_ids = [i for i in range(1000, 10000) if i not in data]

    if not available_ids:
        return standard_response("failure", "No more users can be accepted")

    new_id = random.choice(available_ids)
    data[new_id] = new_user.dict()

    save_user_data(data)

    return standard_response("success", "Your account is successfully created", user_id=new_id)

# Get details of an existing user
@app.get("/get/{user_id}")
async def get(user_id: int, data: Dict[int, Any] = Depends(get_user_data)):
    if user_id not in data:
        raise HTTPException(status_code=404, detail=f"No user with user id {user_id}")

    return standard_response("success", "Your account details are", user_id=user_id, data=data[user_id])

# Update details of an existing user
@app.patch("/update/{user_id}")
async def update(user_id: int, user: UserData, data: Dict[int, Any] = Depends(get_user_data)):
    if user_id not in data:
        raise HTTPException(status_code=404, detail=f"No user with user id {user_id}")

    data[user_id] = user.dict()
    save_user_data(data)

    return standard_response("success", "Your details are updated successfully", user_id=user_id)

# Delete an existing user account
@app.delete("/delete/{user_id}")
async def delete(user_id: int, data: Dict[int, Any] = Depends(get_user_data)):
    if user_id not in data:
        raise HTTPException(status_code=404, detail=f"No user with user id {user_id}")

    del data[user_id]
    save_user_data(data)

    return standard_response("success", "Your account is now deleted", user_id=user_id)
