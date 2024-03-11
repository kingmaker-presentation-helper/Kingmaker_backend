# Kingmaker Backend

## Functions
서버에서 제공하는 기능을 설명한다.

### asr.py
etri api를 이용해 사용자가 녹화한 발표 영상을 txt 파일로 만들고 발음의 정확도를 평가한다.

1. reduce_noise(data, sample_rate): return data
input) data: 업로드한 발표영상, sample_rate: 발표영상의 샘플레이트
output) data: 노이즈 제거한 발표영상
역할) 영상파일의 노이즈를 제거

2. preprocess_audio(file_path, local_directory): return segments, sample_rate
input) file_path: 서버에서 사용자의 폴더 위치 local_directory: 업로드한 발표영상 파일 이름
output) segments: 발표영상의 부분 묶음, sample_rate: 발표영상의 샘플레이트
역할) 업로드한 발표영상을 15초 단위로 끊은 묶음 생성

3. evaluate_pronunciation_parallel(segment_paths, segment_texts): return list(results)
input) segments_paths: 세그먼트 위치 묶음, segment_texts: 세그먼트 stt 결과물 리스트
output) list(results): 세그먼트별 발음 정확도 리스트
역할) 스레드를 활용한 evaluate_pronunciation의 병렬실행

4. recognize_speech(audio_path, http_manager, language_code, open_api_url, access_key): return recognized_text
input) audio_path: stt 돌릴 음성파일 주소, http_manager: urllib3.PoolManager(), language_code: 발표영상에 사용된 언어, open_api_url: etri api 주소, access_key: ETRI access key
output) recognized_text: 음성 파일의 stt 결과
역할) etri api를 이용해 음성을 문자로 변환

5. evaluate_pronunciation(audio_path, segment_text): return response_data['return_object'].get('score')
input) audio_path: 세그먼트 위치, segment_text: 세그먼트의 stt 결과
output) response_data['return_object'].get('score'): 세그먼트의 발음 평가 결과
역할) etri api를 이용해 세그먼트별 발음평가 실시

6. run_asr(session_key): return {"status": "success"}
input) session_key: 사용자의 세션키
output) return {"status": "success"}: asr.py가 잘 실행되었음을 알림
역할) 각 세그먼트별로 발음을 평가하고 그 평균을 저장한다.

7. process_segment(segment_path, language_code, open_api_url, access_key): return recognized_text, pronunciation_score
input) segment_path: 세그먼트 주소, language_code: 발표영상에 사용된 언어, open_api_url: etri api 주소
output) recognized_text: 세그먼트의 stt 결과, pronunciation_score: 세그먼트의 발음평가 점수
역할) recognize_speech, evaluate_pronunciation 실행 후 결과 반환

8. process_audio_segments(local_audio_path, segments, sample_rate, language_code, open_api_url, access_key): return results
input) local_audio_path: , segments: 세그먼트 주소 리스트, sample_rate: 세그먼트의 샘플레이트, language_code: 발표영상에 사용된 언어, open_api_url: etri api 주소, access_key: ETRI access key
output) results: 세그먼트, stt, 발음 점수의 리스트
역할) 각 세그먼트의 stt 결과, 발음 점수를 리스트로 만들어 반환

9. reencode_mp4(input_path, output_path): return
input) input_path: 다시 인코딩할 파일 주소, output_path: 인코딩 후 저장할 파일 주소
output) 없음
역할) 발표영상의 형식이 mp4라면 ffmpeg로 다시 인코딩한다.

### check_highlight.py
Kiwi 라이브러리를 이용해 txt화한 발표 내용을 분석한다.

1. count_word_occurrences(input_text, target_word): return count
input) input_text: 특정 단어가 몇 번 쓰였는지 확인할 문자열, target_word: 몇 번 사용되었는지 확인할 특정 단어
output) count: 문자열에서 특정 단어가 쓰인 횟수
역할) 문자열에서 특정 단어가 몇 번 사용되었는지를 반환한다.

2. check_highlight(session_key): return result
input) session_key: 사용자의 세션키
output) result: 강조된 단어별로 그 단어의 개수, em_score를 리스트로 저장한 딕셔너리
역할) 강조된 단어마다의 개수, em_score를 리스트로 반환

### data.py
발표자료 관련하여 요청한 데이터를 제공한다.

1. process_data(session_key, tag): return ~~~
input) session_key: 사용자의 세션키, tag: 발표연습과 관련하여 요청할 데이터
output) ~~~: tag에서 요청한 데이터
역할) tag를 이용해 어떤 데이터를 요청했는지 확인하고 맞는 데이터를 반환한다.

### find_fillerword.py
문자열에서 필러워드를 얼마나 사용했는지에 대해 분석한다.

1. find_fillerword(session_key): return keyword_counts
input) session_key: 사용자의 세션키
output) keyword_counts: 각 필러워드별 사용된 횟수
역할) 사용자의 세션키를 이용해 필러워드를 얼마나 사용했는지 분석한다.

2. count_matching_words(sentence, keywords): return keyword_counts
input) sentence: 사용자의 발표 내용, keywords: fillerword.txt에 입력한 필러워드
output) keyword_counts: 각 필러워드별 사용된 횟수
역할) 분석할 발표에서 필러워드를 얼마나 사용했는지 계산한다.

### generator.py
생성형 AI를 이용해 발표문에 대한 예상 질문, 키워드, 문장 추천을 수행한다.

1. generate(session_key, type): return {"statusCode": 200, "body": answer}
input) session_key: 사용자의 세션키, type: 생성형 AI로 생성할 종류
output) "statusCode": 생성형 AI와의 통신 성공 여부, "body": 생성한 문장이나 에러코드

### pose.py
발표 중 동작을 분석해 캡쳐한다.

1. natural_sort_key(s): return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]
input) s: 정렬할 문자열
output) 자연정렬된 문자열
역할) 문자열을 자연정렬시킨다.

2. calculate_angle(a, b, c): return angle
input) a, b, c: 신체 특정 위치의 좌표
output) angle: 세 좌표를 기준으로 계산한 각도
역할) 세 좌표를 입력받아 좌표를 계산한다.

3. detect_post(session_key):
input) session_key: 사용자의 세션키
output) -
역할) 사용자가 발표 중 정해진 동작을 수행할 때를 캡쳐해 서버에 저장한다.

### ppt2img.py
발표자료로 업로드한 ppt형식의 파일을 이미지로 변환해 저장한다.

1. save_ppt(ppt_bytes, path):
input) ppt_bytes: 사용자가 업로드한 ppt 파일, path: ppt 저장경로
output) -
역할) 사용자가 업로드한 ppt 파일을 저장한다.

2. ppt2pdf(path): return output
input) path: 파일을 저장할 경로
output) output: pdf 형식으로 변환한 ppt 파일
역할) ppt 형식의 발표자료를 pdf 형식으로 저장한다.

3. pdf2img(pdf, path): return image_paths
input) pdf: 저장한 pdf 형식의 발표자료, path: 파일을 저장할 경로
output) image_paths: 이미지로 변환한 pdf 파일
역할) pdf 형식의 발표자료의 각 슬라이드를 이미지로 변환해 저장한다.

### QA.py
ETRI api를 이용해 발표문을 학습한 후 주어진 질문에 답을 한다.

1. extract_text(passage): return text_only
input) passage: 사용자의 발표내용
output) text_only: 발표내용에서 문자를 제외한 부분을 제거한 문자열
역할) 발표내용에서 문자열만 남기고 나머지를 제거한다.

2. QA_Run(session_key, question): return {
        "statusCode": 200,
        "body": answer + " " + confidence,
        "answer": answer,
        "confidence" : confidence
    }
input) session_key: 사용자의 세션키, question: 발표에 대한 질문
output) "statusCode": 통신 성공여부, "body": 답과 신뢰도, "answer": 질문에 대한 답, "confidence": 답에 대한 신뢰도
역할) 발표내용과 질문을 분석해 답과 신뢰도를 계산한다.

### soundwave.py
ETRI api로 발표 음성을 분석해 발화속도를 계산하고 강조된 단어를 찾는다.

1. detect_silence_in_audio(file_path, min_silence_len=1000, silence_thresh=-45): return silence
input) file_path: 파일 위치, min_silence_len: 공백으로 인정할 최소시간, silence_thresh: 공백으로 판단할 threshold
output) silence: 발표 속 모든 공백의 시작시간과 종료시간을 저장한 리스트
역할) 발표에 존재하는 모든 공백의 시작시간과 종료 시간을 저장한다.

2. match_target_amplitude(sound, target_dBFS): return sound.apply_gain(change_in_dBFS)
input) sound: 변환할 음성파일, target_dBFS: 원하는 크기의 최대 음량
output) sound.apply_gain(change_in_dBFS): 음성파일의 최대 음량을 원하는 크기로 조절한다.
역할) 입력한 음성파일의 최대음량을 원하는 크기로 조절해 음성분석을 용이하게 한다.

### speech_speed.py
발표시간과 단어 수를 이용해 시간당 발음한 단어 수를 분석한다.

1. check_speech_speed(session_key): return {
            "grapheme_count": grapheme_count,
            "word_count": word_count,
            "graphemes_per_second": graphemes_per_second,
            "words_per_second": words_per_second
        }
input) session_key: 사용자의 세션키
output) "grapheme_count": 발음한 글자 수, "word_count": 발음한 단어의 수, "graphemes_per_second": 시간당 발음한 글자 수, "words_per_second": 시간당 발음한 단어의 수
역할) 발표 음성 파일을 분석해 시간당 발음한 글자와 단어의 개수를 계산한다.

2. count_graphemes(text): return len(graphemes)
input) text: 발표 중 한 말
output) len(graphemes): 발음한 글자의 수
역할) 발표 중 말한 글자의 수를 반환한다.

3. count_words(text): return len(words)
input) text: 발표 중 한 말
output) len(words): 발음한 단어의 수
역할) 발표 중 말한 단어의 수를 반환한다.

4. calculate_parameter_per_second(count, seconds): return count / seconds
input) count: 발음한 글자나 단어의 수, seconds: 발표한 시간
output) count / seconds: 시간당 발음한 글자나 단어의 수
역할) 글자나 단어를 시간당 얼마나 발음했는지 계산한다.