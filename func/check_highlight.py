import json
from kiwipiepy import Kiwi

# kiwipiepy 객체 초기화
kiwi = Kiwi(num_workers=4)

async def check_highlight(session_key):
    # 입력 데이터와 비교할 단어 목록을 이벤트에서 추출
    # sessionkey/asr.txt 파일을 읽어서 텍스트를 추출
    with open(f"func/{session_key}/asr.txt", "r", encoding="utf-8") as f:
        input_text = f.read()
    # sessionkey/keywords.txt 파일을 읽어서 텍스트를 추출
    with open(f"func/{session_key}/keywords.txt", "r", encoding="utf-8") as f:
        comparison_words = f.read()
    
    comparison_words = comparison_words.split()

    # Kiwi로 텍스트에서 명사 추출
    nouns = []
    for res in kiwi.analyze(input_text):
        nouns.extend(token.form for token in res[0] if token.tag in ["NNG", "NNP", "NNB", "NR", "NP"])

    # word 각각에 대한 em_score 계산
    for i, word in enumerate(comparison_words):
        comparison_words[i] = {
            'word': word,
            'match_count': nouns.count(word),
            'em_score': nouns.count(word) / len(nouns) if nouns else 0
        }
    
    # 결과 로그 출력 및 반환
    result = {
        'comparison_words': comparison_words,
        'extracted_nouns': nouns
    }
    print(result)

    return result  # JSON 문자열 변환 없이 바로 Python 딕셔너리 반환