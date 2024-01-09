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
        # user/{session_key}/asr.txt 파일 열어서 문장 가져오기
        with open(f"user/{session_key}/asr.txt", "r", encoding="utf-8") as f:
            statement = f.read()
        with open(f"user/{session_key}/info.txt", "r", encoding="utf-8") as f:
            # json 형식으로 저장되어 있는데, 그 중 "keyword"키에 해당하는 것을 가져와줘
            import json
            data = json.load(f)
            words = data["keyword"]
            
    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }
    
    if type == "question":
        query = "다음은 발표문이야. 발표문을 잘 이해하고 예상되는 질문 15개를 생성해봐. 형식: {\"1\": \"질문1 내용\", \"2\": \"질문2 내용\"}. [발표문]"
    elif type == "keyword":
        query = "다음은 발표문이야. 발표문을 잘 이해하고 키워드 15개를 생성해봐. 키워드는 명사 한 개여야 돼. 형식: {\"1\": \"마약\", \"2\": \"검거\"}. [발표문]"
    elif type == "paragraph":
        query = "다음은 발표문이야. 발표문을 잘 이해하고 서론 본론 결론으로 나누어봐. 어느 하나 빠지지 않고, 서론 본론 결론이 반드시 있어야 해. 형식: {{\"서론\": \"서론 내용\", \"본론\": \"본론 내용\", \"결론\": \"결론 내용\"}의 형식으로된 json을 만들어. [발표문]}"
    else:
        return {
            "statusCode": 500,
            "body": "type을 question, keyword, paragraph로 설정해주세요."
        }
    
    # 메시지 설정하기
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": query + " " + statement + "다음과 같은 전문 용어들이 등장할 수 있어. 발표문에서 전문 용어에 오타가 있어도 참고해서 생성해줘. [전문 용어]" + words
        }
    ]

    # ChatGPT API 호출하기
    response = openai.ChatCompletion.create(model=model, messages=messages)
    answer = response['choices'][0]['message']['content']
    
    # 결과 저장하기
    with open(f"user/{session_key}/generated_{type}.txt", "w", encoding="utf-8") as f:
        f.write(answer)

    return {
        "statusCode": 200,
        "body": answer 
    }