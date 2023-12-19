from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from  func.data import process_data

data_router = APIRouter(
	tags=["Data"],
)

@data_router.get("/statement/{sessionkey}")
async def get_statement(session_key: str):
    data = await process_data(session_key, "statement")
    print(data)
    # return JSONResponse(status_code=status.HTTP_200_OK, content=data)
    return data

@data_router.get("/keyword/{sessionkey}")
async def get_keyword(session_key: str):
    data = await process_data(session_key, "keyword")
    return data

@data_router.get("/question/{sessionkey}")
async def get_question(session_key: str):
    data = await process_data(session_key, "question")
    return data

@data_router.get("/duration/{sessionkey}")
async def get_duration(session_key: str):
    data = await process_data(session_key, "duration")
    return data

@data_router.get("/count_of_pose/{sessionkey}")
async def get_count_of_pose(session_key: str):
    data = await process_data(session_key, "count_of_pose")
    return data

@data_router.get("/pose/{sessionkey}")
async def get_pose(session_key: str):
    data = await process_data(session_key, "pose")
    return data

@data_router.get("/highlight/{sessionkey}")
async def get_highlight(session_key: str):
    data = await process_data(session_key, "highlight")
    return data

@data_router.get("/pronunciation/{sessionkey}")
async def get_highlight(session_key: str):
    data = await process_data(session_key, "pronunciation")
    return data

@data_router.get("/download/pose/{sessionKey}/{file_name}")
async def download_photo(sessionKey: str, file_name: str):
    return FileResponse(f"user/{sessionKey}/capture/{file_name}")

@data_router.get("/download/video/{sessionKey}")
async def download_video(sessionKey: str):
    # user/{sessionKey} 폴더에서 mp4 파일 찾기
    for file in os.listdir(f"user/{sessionKey}"):
        if file.endswith(".mp4"):
            return FileResponse(f"user/{sessionKey}/{file}")
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "mp4 파일을 찾을 수 없습니다."})

# {sessionKey}/info.txt에 저장되어있는 json 형식의 데이터를 읽어서 반환
@data_router.get("/info/{sessionKey}")
async def get_info(sessionKey: str):
    try:
        with open(f"user/{sessionKey}/info.txt", "r", encoding="utf-8") as f:
            data = f.read()
            return JSONResponse(status_code=status.HTTP_200_OK, content=data)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": str(e)})