import sounddevice as sd
import wave
from pydub import AudioSegment

class Audio():
    def __init__(self):
        # 녹음 설정
        self.duration = 5  # 녹음 시간(초)
        self.sample_rate = 44100  # 샘플링 속도

        self.output_wav = "data/output.wav"
        self.output_mp3 = "data/output.mp3"

    def __record_audio(self, output_wav):
        # 오디오 녹음
        recording = sd.rec(
            int(self.duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype='int16'
        )
        sd.wait()  # 녹음이 끝날 때까지 대기

        # 녹음된 데이터를 .wav 파일로 저장
        with wave.open(output_wav, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16비트 오디오
            wf.setframerate(self.sample_rate)
            wf.writeframes(recording.tobytes())

    def __convert_wav_to_mp3(self, output_wav, output_mp3):
        wav_audio = AudioSegment.from_wav(output_wav)
        wav_audio.export(output_mp3, format='mp3')

    def recorde(self, output_wav, output_mp3):
        self.__record_audio(output_wav)
        self.__convert_wav_to_mp3(output_wav, output_mp3)

# 오디오 녹음 및 WAV 파일 저장
# output_wav = "data/output.wav"
# record_audio(output_wav, duration, sample_rate)

# # WAV 파일을 MP3로 변환 및 저장
# output_mp3 = "data/output.mp3"
# convert_wav_to_mp3(output_wav, output_mp3)