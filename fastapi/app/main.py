from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from database import ( get_user_info, hash_password, verify_password )
from data_models import UserLoginSchema

app = FastAPI()


# CORS 설정
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # can alter with time
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )



@app.post("/user/login", description="사용자 로그인 API 입니다.",
         responses={
             200: {
                 "content": {
                     "application/json": {
                         "example": {
                             "message": "사용자 로그인에 성공했습니다.",
                             "data": {
                                "access_token": "token",
                                "user_info": {
                                    "user_name": "user",
                                    "profile_image": "",
                                    "role": "user"
                                }
                             }
                         }
                     }
                 }
             }
         })
async def user_login(user:UserLoginSchema = Body(default=None)):
    user_entered = jsonable_encoder(user)
    user_info =  await get_user_info(user_entered["email"])
    
    if await check_user(user_entered):
        return {
            "message" : "Successfully Logged In!",
            "data": {    
                "access_token" :signJWT(user.email),
                "user_info": {
                    "user_name": user_info["email"].split("@")[0],
                    "profile_image": user_info["profile_image"],
                    "role": user_info["role"]
                }
            }
        }
    else:
        raise HTTPException(status_code=400, detail="Incorrect password")


async def check_user(user_entered):
    try:
        user_info = await get_user_info(user_entered["email"])
        hashed_password = user_info["password"]
        
        if verify_password(user_entered['password'], hashed_password):
            return True
        else:
            return False
    except:
        raise HTTPException(status_code=400, detail="Incorrect email")