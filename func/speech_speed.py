import re
import os 

async def check_speech_speed(session_key):

    text_file_path = f"user/{session_key}/asr.txt"
    
    for file in os.listdir(f"user/{session_key}"):
        if file.endswith(".mp4"):
            video_file_path = f"user/{session_key}/{file}"

    # duration.txt 열어서 숫자가져오기
    with open(f"user/{session_key}/duration.txt", "r") as f:
        file_duration_in_seconds = float(f.read())
    
    with open(text_file_path, "r", encoding="utf-8") as f:
        text = f.read()

    if text is not None and file_duration_in_seconds is not None:
        grapheme_count = count_graphemes(text)
        word_count = count_words(text)
        graphemes_per_second = calculate_parameter_per_second(grapheme_count, file_duration_in_seconds)
        words_per_second = calculate_parameter_per_second(word_count, file_duration_in_seconds)

        # 결과 txt 파일로 저장
        with open(f"user/{session_key}/speech_speed.txt", "w", encoding="utf-8") as f:
            f.write(f"grapheme_count: {grapheme_count}\n")
            f.write(f"word_count: {word_count}\n")
            f.write(f"graphemes_per_second: {graphemes_per_second}\n")
            f.write(f"words_per_second: {words_per_second}\n")
        # 결과 출력
        return {
            "grapheme_count": grapheme_count,
            "word_count": word_count,
            "graphemes_per_second": graphemes_per_second,
            "words_per_second": words_per_second
        }


def count_graphemes(text):
    graphemes = re.findall(r'[\w가-힣]', text)
    return len(graphemes)

def count_words(text):
    words = re.findall(r'\b\w+\b', text)
    return len(words)

def calculate_parameter_per_second(count, seconds):
    if seconds == 0:
        return 0
    return count / seconds

