
import json
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import random

FILE_NAME = "test.json"


#returns dictionary read from the json file
def get_user_data():
    with open(FILE_NAME) as j_file:
        return json.load(j_file)


# user class defining their attributes
class user_data(BaseModel):
    username:str
    email: str
    password: str


app = FastAPI()


# create a new user account
@app.post("/create")

# using fastapi dependency injections for the dictonary
async def create(new_user:user_data, d : dict=Depends(get_user_data)): 

    l=[i for i in range(1000,10000) if i not in d.keys()]

    # empty list
    if not l:
        return {"status": "failure",
                "message": "no more users accepting"}
    
    new_id = random.choice(l)
    
    d[new_id] = dict(new_user)

    # dump the new user created into our json file
    with open (FILE_NAME,'w+') as out:
        json.dump(d, out, indent=2)

    #json response
    return {"status": "success",
            "user_id": new_id,
            "message": "Your account is succesfully created"
        }



# get/print details of an existing user
@app.get("/get/{user_id}")
async def get(user_id ,d : dict=Depends(get_user_data) ):

    # Underflow check
    if user_id not in d:
        raise HTTPException(status_code=404, detail = f"No user with user id {user_id}")

    
    return {"staus":"success","message":"Your account details are"}, d[user_id]

# updating details of an existing user
@app.patch("/update/{user_id}")
async def update(user_id, user:user_data , d : dict=Depends(get_user_data)):

    # Underflow check
    if user_id not in d:
        raise HTTPException(status_code=404, detail = f"No user with user id {user_id}")
    
    d[user_id] = dict(user)

    # dump the updates in our json file
    with open (FILE_NAME,'w+') as out:
        json.dump(d, out, indent=2)

    return {"status": "success",
            "user_id":user_id,
            "message": "Your details are updated succesfully"
        }


# delete an existing user account
@app.delete("/delete/{user_id}")
async def delete(user_id , d : dict=Depends(get_user_data)):

    # Underflow check
    if user_id not in d:
        raise HTTPException(status_code=404, detail = f"No user with user id {user_id}")
    
    del d[user_id]

    # dump updates in our json file
    with open (FILE_NAME,'w+') as out:
        json.dump(d, out, indent=2)

    return {"status": "success",
            "user_id": user_id,
            "message": "Your account is now deleted"
        }



