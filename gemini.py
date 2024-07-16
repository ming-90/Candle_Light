import google.generativeai as genai
import PIL.Image

GOOGLE_API_KEY="AIzaSyBQVgx4TNpNoVrTeBSQINND-JKZYmdYHEk"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-pro')

def gemini_text(text):
    response = model.generate_content(text)

    print(response.text)

def gemini_audio(audio):
    prompt = "말하는 내용 그대로 알려줘"

    audio_file = genai.upload_file(path='data/output.mp3')
    response = model.generate_content([prompt, audio_file])

    print(response.text)

def gemini_image(path):
    prompt = "버스의 번호를 알려줘"
    sample_file = genai.upload_file(path="data/bus.jpeg",
                            display_name="Jetpack drawing")
    response = model.generate_content([sample_file, prompt])

    print(response.text)

# gemini_audio('asd')
gemini_image('asd')