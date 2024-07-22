env:
	conda create -n voice_helper python=3.10 -y

setup:
	pip install -r requirements.txt

conda:
	conda activate voice_helper