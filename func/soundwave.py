from pydub import AudioSegment
from pydub.silence import detect_silence, detect_nonsilent
import noisereduce as nr
import librosa
import soundfile as sf
import os
import urllib3
import json
import base64
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import settings
openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
accessKey = settings.ETRI_ACCESS_KEY
languageCode = "korean"


# 노이즈 감소 함수 정의
# def reduce_noise(audio_data, sample_rate=16000):
#     # 오디오 데이터에서 노이즈를 감소시킵니다.
#     reduced_data = nr.reduce_noise(y=audio_data, sr=sample_rate)
#     return reduced_data

def detect_silence_in_audio(file_path, min_silence_len=1000, silence_thresh=-45):
    """
    Detects silence in an audio file.

    :param file_path: Path to the audio file.
    :param min_silence_len: Minimum length of a silence to be detected in milliseconds.
    :param silence_thresh: The upper bound for what is considered silence in dBFS.
    :return: List of tuples with start and end times of silence.
    """

    # Load the audio file
    audio = AudioSegment.from_file(file_path)

    # Detect silence
    silence = detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

    # Convert silence times to milliseconds
    silence = [(start, end) for start, end in silence]

    return silence

non_silence_list = detect_silence_in_audio("C:\\turtlebot\\test-autorace\\Kingmaker_backend\\user\\9faf486182044e5d11d27c5d4d68b86b\\2023-12-19 13-52-48.wav")

print(non_silence_list)
audio = AudioSegment.from_file("C:\\turtlebot\\test-autorace\\Kingmaker_backend\\user\\9faf486182044e5d11d27c5d4d68b86b\\2023-12-19 13-52-48.wav")

def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

# audio = match_target_amplitude(audio, -20.0)

# 침묵 사이 부분을 10초 단위로 저장
segments = []
segments_time_stamp = []
segment_length = 10000

for non_slience in non_silence_list:
    # non_silence에 적힌 start와 end 부분 만큼의 오디오를 가져오기
    non_slience_segment = audio[non_slience[0]:non_slience[1]]
    start = non_slience[0]
    end = non_slience[1]

    # non_silence를 10초씩 나누어 리스트에 저장.
    for i in range(0, len(non_slience_segment), 10000):
        if i + segment_length > len(non_slience_segment):
            segment = non_slience_segment[i:]
            segments_time_stamp.append((start+i, end))
        else:
            segment = non_slience_segment[i:i+segment_length]
            segments_time_stamp.append((start+i, start+i+segment_length))
        segments.append(segment)
        

print(len(segments))
print(segments_time_stamp)
# 오디오 세그먼트 처리
processed_segments = []

for i, segment in enumerate(segments):
    segment_file_path_tmp = f"a_segment_{i}.wav"
    
    # AudioSegment 객체를 wav 파일로 저장
    segment.export(segment_file_path_tmp, format="wav")

    data, sample_rate = librosa.load(segment_file_path_tmp, sr=None)
    
    # 노이즈 감소 적용
    # data = reduce_noise(data, sample_rate=16000)

    file_path = segment_file_path_tmp.rsplit('.', 1)[0] + '.pcm'
    
    if sample_rate != 16000:
        data = librosa.resample(data, orig_sr=sample_rate, target_sr=16000)
        sample_rate = 16000

    sf.write(file_path, data, sample_rate, format='RAW', subtype='PCM_16')
    processed_segments.append(file_path)

print(processed_segments)
print(len(processed_segments))
# segment들을 etri api에 전송

result = []
for audioFilePath in processed_segments:
    print(audioFilePath)
    file = open(audioFilePath, "rb")
    audioContents = base64.b64encode(file.read()).decode("utf8")
    file.close()

    requestJson = {    
        "argument": {
            "language_code": languageCode,
            "audio": audioContents
        }
    }

    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8","Authorization": accessKey},
        body=json.dumps(requestJson)
    )

    print("[responseCode] " + str(response.status))
    # print("[responBody]")
    print(str(response.data,"utf-8"))

    response_data = json.loads(str(response.data,"utf-8"))
    recognized_text = response_data['return_object']['recognized']

    # 만약 response.data['return_object']['recognized']에 'reason'이라는 키가 있다면
    if 'reason' in recognized_text:
        result.append(" ")
    else:
        result.append(recognized_text)

print("\n------------------------")
print(result)
print("------------------------\n")

# result와 segments_time_stamp를 사용하여 시간 대비 음절 수 계산
for text, (start, end) in zip(result, segments_time_stamp):
    print("Text:", text)
    print("Time Stamp:", (start, end))

    # 공백 제거
    text_without_spaces = text.replace(" ", "")

    # 시간 계산 (밀리초 단위에서 초 단위로 변환)
    duration = (end - start) / 1000  # Duration in seconds

    # 음절 수 계산 (공백 제외)
    syllable_count = len(text_without_spaces)

    # 시간 당 음절 수 계산
    if duration > 0:
        syllables_per_second = syllable_count / duration
        print("Syllables per second:", syllables_per_second)
    else:
        print("Duration is too short to calculate syllables per second.")

    print("\n")

    # syllabers per second에 따라 글자 색을 다르게 표시(plot으로 시각화)
    if syllables_per_second > 4 and syllables_per_second < 5:
        color = "green"
    elif syllables_per_second <= 4:
        color = "orange"
    else:
        color = "red"
    
    # plot으로 텍스트 시각화
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np

    fig, ax = plt.subplots(figsize=(10, 1))
    ax.set_xlim(0, duration)
    ax.set_ylim(0, 1)
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.set_xticks(np.arange(0, duration, 0.1))
    ax.set_yticks(np.arange(0, 1, 1))
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Syllables per second")
    ax.text(0, 0.5, text, fontsize=20, color=color)
    ax.add_patch(mpatches.Rectangle((0, 0), duration, 1, color=color, alpha=0.2))
    plt.show()


