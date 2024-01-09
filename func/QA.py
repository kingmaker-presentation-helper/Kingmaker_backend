# -*- coding:utf-8 -*-
import os, sys
import re
import urllib3
import json
import settings


#-------------------------------PARAMETER-------------------------------------
openApiURL = "http://aiopen.etri.re.kr:8000/MRCServlet"
accessKey = settings.ETRI_ACCESS_KEY
#-----------------------------------------------------------------------------

def extract_text(passage):
    # 부동 소수점 수를 찾는 정규 표현식
    pattern = re.compile(r'\s+\d+\.\d+$')
    # 정규 표현식을 사용하여 부동 소수점 수를 찾고, 해당 부분을 제거
    text_only = re.sub(pattern, '', passage)
    return text_only

async def QA_Run(session_key, question):
    # question = "test"  # 사용자 입력을 받음
    passage = "test"
    try:
        with open(f"./user/{session_key}/asr.txt", "r", encoding="utf-8") as f:
            passage = f.read()
            passage = extract_text(passage)
    except Exception as e:
        print(e)
        exit()

    requestJson = {
        "argument": {
            "question": question,
            "passage": passage
        }
    }

    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8", "Authorization": accessKey},
        body=json.dumps(requestJson)
    )

    # 응답 데이터를 디코딩하고 JSON으로 파싱
    response_data = response.data.decode('utf-8')  # HTTPResponse 객체의 데이터를 문자열로 변환
    data = json.loads(response_data)  # 문자열 데이터를 JSON으로 파싱

    # 필요한 데이터 추출
    answer = data["return_object"]["MRCInfo"]["answer"]
    confidence = data["return_object"]["MRCInfo"]["confidence"]
    q = data["return_object"]["MRCInfo"]["question"]
    p = data["return_object"]["MRCInfo"]["passage"]
    print(q)
    print(p)
    print("Answer:", answer)
    print("Confidence:", confidence)

    return {
        "statusCode": 200,
        "body": answer + " " + confidence,
        "answer": answer,
        "confidence" : confidence
    }







