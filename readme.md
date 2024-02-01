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

### data
발표자료 관련하여 요청한 데이터를 제공한다.

1. process_data(session_key, tag): return ~~~
input) session_key: 사용자의 세션키, tag: 발표연습과 관련하여 요청할 데이터
output) ~~~: tag에서 요청한 데이터
역할) 