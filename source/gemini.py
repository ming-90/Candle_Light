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
        prompt = "버스의 번호만 답변으로 줘. 예를 들어 '100', '200' 와 같이 알려줘.'"
        sample_file = genai.upload_file(path=path,
                                display_name="Jetpack drawing")
        response = model.generate_content([sample_file, prompt])

        return response.text
