#-*- coding:utf-8 -*-

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.connetion import conn
from routes.users import user_router
from routes.events import event_router

# FastAPI
app = FastAPI()

# 라우터 등록
app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/events")

#애플리케이션이 시작 될 때 데이터베이스를 생성하도록 만듬
@app.on_event("startup")
def on_startup():
	conn()

origins =['*']

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=['*'],
	allow_headers=['*'],
)

if __name__ == "__main__":
	import uvicorn
	uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)
