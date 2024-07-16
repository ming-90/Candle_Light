import sounddevice as sd
import wave
from pydub import AudioSegment

# 녹음 설정
duration = 3  # 녹음 시간(초)
sample_rate = 44100  # 샘플링 속도

def record_audio(filename, duration, sample_rate):
    print("녹음 시작...")
    # 오디오 녹음
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()  # 녹음이 끝날 때까지 대기
    print("녹음 종료")

    # 녹음된 데이터를 .wav 파일로 저장
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16비트 오디오
        wf.setframerate(sample_rate)
        wf.writeframes(recording.tobytes())

def convert_wav_to_mp3(wav_filename, mp3_filename):
    wav_audio = AudioSegment.from_wav(wav_filename)
    wav_audio.export(mp3_filename, format='mp3')
    print(f"MP3 파일 {mp3_filename} 저장 완료")

# 오디오 녹음 및 WAV 파일 저장
output_wav = "data/output.wav"
record_audio(output_wav, duration, sample_rate)

# WAV 파일을 MP3로 변환 및 저장
output_mp3 = "data/output.mp3"
convert_wav_to_mp3(output_wav, output_mp3)