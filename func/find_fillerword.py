import re

async def find_fillerword(session_key):

    with open("fillerword.txt", "r", encoding="utf-8") as f:
        input_keywords = f.read().split(",")
    with open(f"func/{session_key}/asr.txt", "r", encoding="utf-8") as f:
        input_sentence = f.read()

    # 함수 호출하여 각 키워드별 검출 수 얻기
    keyword_counts = count_matching_words(input_sentence, input_keywords)

    # 결과 출력 - 많이 검출된 키워드 순서대로 내림차순 정렬하여 출력
    print("1. 각 키워드별 검출 수 (많이 검출된 순):")
    sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
    for keyword, count in sorted_keywords:
        print(f"{keyword}: {count} 번")

    # 문장 속 모든 단어의 갯수 구하기
    word_count = len(re.findall(r'\w+', input_sentence))
    print(f"\n2. 문장 속 모든 단어의 갯수: {word_count} 개")

    return keyword_counts

def count_matching_words(sentence, keywords):
    # 문장에서 특수문자 제거
    sentence = re.sub(r'[^\w\s]', '', sentence)
    words = sentence.split()

    # 각 키워드별로 검출된 수를 저장할 딕셔너리
    keyword_counts = {}
    for keyword in keywords:
        keyword_count = words.count(keyword)
        if keyword_count > 0:
            keyword_counts[keyword] = keyword_count

    return keyword_counts
