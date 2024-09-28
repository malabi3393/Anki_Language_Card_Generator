from num2words import num2words




FORBIDDEN = '#%&{}\\<>*?/ $!\'\":@`|='



class Card():

    def __init__(self, original_word, language):
        self.from_word = original_word
        self.from_lg = language

        if isinstance(self.from_word, int):
            self.fn = num2words(self.from_word, to = 'ordinal')
        else:
            for char in FORBIDDEN:
                self.fn = self.from_word.replace(char, '-') 
        self.soundtag = f'[sound:{self.fn}.mp3]'

    def set_translated_word(self, translated_word):
        self.translated_word = translated_word

    

