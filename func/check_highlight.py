import json
from kiwipiepy import Kiwi

# kiwipiepy 객체 초기화
kiwi = Kiwi(num_workers=4)

import re

def count_word_occurrences(input_text, target_word):
    """
    Count the occurrences of a target word in the given text, including substrings.

    Parameters:
        input_text (str): The input text.
        target_word (str): The word to count occurrences.

    Returns:
        int: The count of occurrences of the target word.
    """
    # Use a regex pattern to find all occurrences of the target word as a whole word or as part of other words
    pattern = re.compile(r'\b(?:' + re.escape(target_word) + r'\w*|' + re.escape(target_word) + r')\b', re.IGNORECASE)
    matches = re.findall(pattern, input_text)
    count = len(matches)
    return count


async def check_highlight(session_key):
    # 입력 데이터와 비교할 단어 목록을 이벤트에서 추출
    # sessionkey/asr.txt 파일을 읽어서 텍스트를 추출
    with open(f"user/{session_key}/asr.txt", "r", encoding="utf-8") as f:
        input_text = f.read()
    # sessionkey/keywords.txt 파일을 읽어서 텍스트를 추출
    with open(f"user/{session_key}/generated_keyword.txt", "r", encoding="utf-8") as f:
        comparison_words = f.read()
    
    # string을 dictionary로 변환
    comparison_words = json.loads(comparison_words)

    # value 값만 list로 저장
    comparison_words = list(comparison_words.values())

    # # Kiwi로 텍스트에서 명사 추출
    # nouns = []
    # for res in kiwi.analyze(input_text):
    #     nouns.extend(token.form for token in res[0] if token.tag in ["NNG", "NNP", "NNB", "NR", "NP"])

    # word 각각에 대한 em_score 계산
    # for i, word in enumerate(comparison_words):
    #     comparison_words[i] = {
    #         'word': word,
    #         'match_count': count_word_occurrences(input_text, word),
    #         'em_score': nouns.count(word) / len(nouns) if nouns else 0
    #     }
    for i, word in enumerate(comparison_words):
        match_count = count_word_occurrences(input_text, word)
        total_words = len(re.findall(r'\b\w+\b', input_text))
        em_score = match_count / total_words if total_words else 0

        comparison_words[i] = {
            'word': word,
            'match_count': match_count,
            'em_score': em_score
        }
    # 결과 로그 출력 및 반환
    result = {
        'comparison_words': comparison_words,
        'extracted_nouns': ""
    }
    print(result)

    # user/{session_key}에 txt 형식으로 저장
    with open(f"user/{session_key}/highlight.txt", "w", encoding="utf-8") as f:
        f.write(json.dumps(result, ensure_ascii=False))

    return result  # JSON 문자열 변환 없이 바로 Python 딕셔너리 반환