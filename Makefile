default:
	rm -r sounds/*
	
clean_sounds:
	rm -r media/*.mp3


install:
	python3 -m pip install -r src/requirements.txt
