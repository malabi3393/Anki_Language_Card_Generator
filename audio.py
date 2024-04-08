# Importing necessary modules required  

from googletrans import Translator  
from gtts import gTTS  
import os

list = ['jag', 'inte']
word = 'jag'



def translate_word(word, source_language='sv', target_language='en'):
    translator = Translator()
    translation = translator.translate(word, src=source_language, dest=target_language)
    if translation is not None and translation.text is not None:
        return translation.text
    else:
        print(f"Translation failed for word: {word}")
        return ''  # or return the original word or any other default value

translated_row = []

#--------------

# for w in list:
    # translated_word = translate_word(w, source_language='sv', target_language='en')
    # translated_row.append(translated_word)

# test = translate_word(word, source_language='sv', target_language='en')
speak = gTTS(text=word, lang='sv', slow=False) 
speak.save("captured_voice.mp3")