default:
	rm -r sounds/*
	rm -r src/*.apkg
clean_sounds:
	rm -r src/*.mp3
clean_apkg:
	rm -r src/*.apkg

install:
	python3 -m pip install -r src/requirements.txt
