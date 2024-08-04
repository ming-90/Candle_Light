env:
	conda create -n candle_light python=3.10 -y

setup:
	pip install -r requirements.txt

run:
	streamlit run app.py