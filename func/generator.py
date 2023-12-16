import boto3
import openai
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import settings

# AWS Lambda 환경 변수에서 OpenAI API 키 가져오기
OPENAI_API_KEY = settings.OPENAI_ACCESS_KEY

# 발급받은 API 키 설정
openai.api_key = OPENAI_API_KEY

# 모델 - GPT 3.5 Turbo 선택
model = "gpt-3.5-turbo"

async def generate(session_key, type):

    try:
        # func/{session_key}/asr.txt 파일 열어서 문장 가져오기
        with open(f"func/{session_key}/asr.txt", "r", encoding="utf-8") as f:
            statement = f.read()

    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }
    
    if type == "question":
        query = "다음은 발표문이야. 발표문을 잘 이해하고 예상되는 질문 15개를 생성해봐. 형식: {\"1\": \"질문1 내용\", \"2\": \"질문2 내용\"}. [발표문]"
    elif type == "keyword":
        query = "다음은 발표문이야. 발표문을 잘 이해하고 키워드 15개를 생성해봐. 형식: {\"1\": \"마약\", \"2\": \"검거\"}. [발표문]"
    else:
        return {
            "statusCode": 500,
            "body": "type을 question 또는 keyword로 설정해주세요."
        }
    
    # 메시지 설정하기
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": query + " " + statement
        }
    ]

    # ChatGPT API 호출하기
    response = openai.ChatCompletion.create(model=model, messages=messages)
    answer = response['choices'][0]['message']['content']
    
    # 결과 저장하기
    with open(f"func/{session_key}/{type}.txt", "w", encoding="utf-8") as f:
        f.write(answer)

    return {
        "statusCode": 200,
        "body": answer
    }