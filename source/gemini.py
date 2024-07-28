import os
import google.generativeai as genai
import PIL.Image
from dotenv import load_dotenv

load_dotenv()

google_secret=os.environ.get('GOOGLE_SECRET')

genai.configure(api_key=google_secret)
model = genai.GenerativeModel('models/gemini-1.5-pro')

class Gemini:

    def text(self, text):
        response = model.generate_content(text)

        print(response.text)

    def audio(self, audio_path):
        prompt = "말하는 내용 그대로 알려줘"

        audio_file = genai.upload_file(path=audio_path)
        response = model.generate_content([prompt, audio_file])

        return response.text

    def image(self, path):
        prompt = "버스의 번호를 알려줘"
        sample_file = genai.upload_file(path="data/bus.jpeg",
                                display_name="Jetpack drawing")
        response = model.generate_content([sample_file, prompt])

        print(response.text)


# GOOGLE_API_KEY="AIzaSyBUviRQ_hIoFSLKx-K6opZf_CueU9wuNW0"
# genai.configure(api_key=GOOGLE_API_KEY)
# model = genai.GenerativeModel('models/gemini-1.5-pro')
# text = "넌 누구야"
# response = model.generate_content(text)

# print(response.text)
# gemini_audio('asd')
# gemini_image('asd')
# text = '''
# 출발지 : 126.8463,37.313393
# 도착지 : 126.838745,37.316147
# '''
# gemini_text(text + "내가 보내준 위경도로 길 안내 해 줄수 있어?")

