#-*- coding:utf-8 -*-
    
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.function import function_router
from routes.data import data_router

# FastAPI
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
	"http://localhost:9000",
	"http://127.0.0.1:9000",
	"http://127.0.0.1:8080",
	"http://127.0.0.1",
]


# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

# 라우터 등록
app.include_router(function_router, prefix="/function")
app.include_router(data_router, prefix="/data")

origins =['*']

# app.add_middleware(
# 	CORSMiddleware,
# 	allow_origins=origins,
# 	allow_credentials=True,
# 	allow_methods=['*'],
# 	allow_headers=['*'],
# )


if __name__ == "__main__":
	import uvicorn
	uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)
