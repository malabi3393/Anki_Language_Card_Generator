default:
	rm -r sounds/*
	rm -r sentences/*.apkg
clean_sounds:
	rm -r sounds/*
clean_apkg:
	rm -r sentences/*.apkg

install:
	python3 -m pip install -r requirements.txt
