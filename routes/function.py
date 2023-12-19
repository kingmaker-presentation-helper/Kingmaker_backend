from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import JSONResponse
from starlette.requests import Request
import boto3
import mediapipe as mp
import cv2
import numpy as np
import sys, os
import datetime
import secrets
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from func.pose import detect_pose
from func.s3 import upload_file_to_s3
from func.asr import run_asr
from func.check_highlight import check_highlight
from func.speech_speed import check_speech_speed
from func.generator import generate
from func.find_fillerword import find_fillerword
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
from starlette.requests import Request
import io
import soundfile as sf

from pydantic import BaseModel

function_router = APIRouter(
	tags=["Function"],
)

@function_router.get("/sessionkey")
async def get_session_key():
    return JSONResponse({"sessionkey": secrets.token_hex(16)})

@function_router.get("/pose/{sessionkey}")
async def pose(sessionkey: str):
    detect_pose(f"{sessionkey}")

@function_router.post("/files/")
async def create_file(request: Request, file: UploadFile = File(...), user_name: str = Form(...)):
    content = await file.read()
    # user_name과 같은 폴더 생성
    if not os.path.exists("user/" + user_name):
        os.makedirs("user/" + user_name)
    # Save the image
    with open("user/" + user_name+"/"+file.filename, "wb") as f:
        f.write(content)
    
    return JSONResponse({"filename": file.filename})

@function_router.post("/audio/")
async def create_file(request: Request, file: UploadFile = Form(...), user_name: str = Form(...), duration: str = Form(...)):
    try:
        # user_name과 같은 폴더 생성
        user_folder = os.path.join("user", user_name)
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
        
        # Save the audio
        file_path = os.path.join(user_folder, file.filename)
        with open(file_path, "wb") as f:
            f.write(file.file.read())

        duration_file_path = os.path.join(user_folder, "duration.txt")
        with open(duration_file_path, "w") as f:
            f.write(duration)

        return JSONResponse({"filename": file.filename, "status": "success"})

    except Exception as e:
        return JSONResponse({"error": str(e), "status": "failed"})
    
@function_router.get("/asr/{sessionKey}")
async def asr(sessionKey: str):
    response = await run_asr(sessionKey)
    return response

@function_router.get("/highlight/{sessionKey}")
async def highlight(sessionKey: str):
    response = await check_highlight(sessionKey)
    return response
    
@function_router.get("/speech_speed/{sessionKey}")
async def speech_speed(sessionKey: str):
    response = await check_speech_speed(sessionKey)
    return response

@function_router.get("/generate/{type}/{sessionKey}")
async def generate_keyword(sessionKey: str, type: str):
    response = await generate(sessionKey, type)
    return response

@function_router.get("/fillerword/{sessionKey}")
async def fillerword(sessionKey: str):
    response = await find_fillerword(sessionKey)
    return response

@function_router.get("/all/{sessionKey}")
async def all(sessionKey: str):
    await run_asr(sessionKey)
    await generate(sessionKey, "keyword")
    await check_highlight(sessionKey)
    await check_speech_speed(sessionKey)
    await find_fillerword(sessionKey)
    await generate(sessionKey, "question")
    await detect_pose(sessionKey)

    return JSONResponse({"status": "success"})

import json

class Info(BaseModel):
    month: str
    day: str
    title: str
    keyword: str
    ppt: str
    sessionKey: str

@function_router.post("/info/")
async def info(user_data: Info):
    try:
        # 받은 데이터 확인
        print("Received data:")
        print(user_data.dict())

        # f"user/{user_data.sessionKey}" 폴더 생성
        if not os.path.exists(f"user/{user_data.sessionKey}"):
            os.makedirs(f"user/{user_data.sessionKey}")
        # session key 폴더에 정보를 txt 파일로 저장
        with open(f"user/{user_data.sessionKey}/info.txt", "w", encoding="utf-8") as f:
            f.write(json.dumps(user_data.dict(), ensure_ascii=False))
        # 응답 데이터 구성
        response_data = {
            "status": "success"
        }

        # 클라이언트에게 JSON 형태로 응답
        return JSONResponse(content=response_data, status_code=200)
    except HTTPException as e:
        # FastAPI의 HTTPException에서 자세한 정보를 출력
        print("Error:", e.detail)
        raise e