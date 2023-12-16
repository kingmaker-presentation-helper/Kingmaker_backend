from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from dynamoDB import scan_table, get_item

db_router = APIRouter(
	tags=["db"],
)


# # 모든 데이터를 조회하는 API 엔드포인트
# @db_router.get("/items")
# def read_items():
#     items = scan_table()
    
#     # items.headers["Access-Control-Allow-Origin"] = str(ORIGIN)
#     return {"items": items}

# 모든 데이터를 조회하는 API 엔드포인트
@db_router.get("/items")
def read_items():
    items = scan_table()
    
    response = {"items": items}
    response["headers"] = {"Access-Control-Allow-Origin": "*"}

    return response

# # 특정 키에 해당하는 항목을 조회하는 API 엔드포인트
# @db_router.get("/items/{item_id}")
# def read_item(item_id: str):
#     item = get_item({"id": item_id})
#     # item.headers["Access-Control-Allow-Origin"] = str(ORIGIN)
#     if item:
#         return {"item": item}
#     return {"error": "Item not found"}


# 특정 키에 해당하는 항목을 조회하는 API 엔드포인트
@db_router.get("/items/{item_id}")
def read_item(item_id: str):
    item = get_item(item_id)
    
    # CORS headers를 response에 추가
    response = {"item": item}
    response["headers"] = {"Access-Control-Allow-Origin": "*"}
    
    if item:
        return response
    return {"error": "Item not found"}