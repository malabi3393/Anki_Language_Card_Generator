""" Anki Card Generator """

import csv
from googletrans import Translator
import genanki 
import os.path
import warnings
from gtts import gTTS 
import re
import argparse
from typing import NamedTuple


Cards = set()

class Card:
    def __init__(self, source, native = '', audio = '', name = ''):
        self.source = source
        self.native = native
        self.audio = audio
        self.name = name
    
    def set_filename(self, filename):
        self.name = filename
        return
    def get_filename(self):
        return self.name
    
    def translate_word(self, language):
        translator = Translator()
        translation = translator.translate(self.source, src=language, dest='en')
        #print(translation)
        if translation.text is not None:
            return translation.text
        else:
            return ''  # or return the original word or any other default value
    def handle_separator(self, sep):
        match sep:
            case '.':
                print('x')


    
    
def text_to_word_list(file_path, separator = ' ') -> list:
    try:
        word_list = []
        if separator == "n":
            text = open(file_path,'r').read().splitlines()
            word_list = set(text)
            #print(word_list)
        else:
            with open(file_path, 'r') as file:
                text = file.read()
                # Split the text into words using whitespace as separator
                word_list = text.split(sep = separator)
        
            print(len(word_list))
            if separator != '.':
                word_list = [word.lower() for word in word_list]
            #removes doubles
            word_list = list(set([word for word in word_list]))
            #remove duplicates
            #remove white space character at the beginning of a line 
        word_list = [(re.sub(r"^\s*", "", w), re.sub(r"^\W*", "", w)) for w in word_list]
            #removes any non word characters
        #word_list = [re.sub(r"^\W*", "", w) for w in word_list]
            #removes empty strings
        word_list = [i for i in word_list if i != '']

        word_list = list(set([word for word in word_list]))
        print(len(word_list))
              
            #print([word for word in word_list]) 
        return word_list
    except FileNotFoundError:
        print("File not found.")
        return []


def translate_word(word, target_language, native_language = 'en'):
    translator = Translator()
    translation = translator.translate(word, src=target_language, dest=native_language)
    #print(translation)
    
    if translation.text is not None:
        return translation.text
    else:
        return ''  # or return the original word or any other default value

def translate_target_words_to_native(source_list, target, native) -> list:
    translated_list = []
    for word in source_list:
        try:
            translated_word = translate_word(word, target_language= target, native_language=native)
            translated_list.append(translated_word)
        except Exception as e:
            print(f"Translation failed for word: {word}. Error: {e}")
            translated_list.append('')  # Append an empty string as translation
    try:
        print(f"Translations successfully exported to list")
        return translated_list
    except Exception as e:
        print("Error in translating your list. An empty list is returned.")
        return []

# --------------------------------------------------

def create_anki_deck(target_list, native_list, target_lng, output_filename):

    my_model_1 = genanki.Model(
    13110120064,
    'Example',
    fields=[
        {'name': 'Native Language'},
        {'name': 'Target'},
        {'name': 'Target_Audio'}
    ],
    templates=[
        {
        'name': 'Card 1',
        'qfmt': '{{Native Language}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Target}}<br>{{Target_Audio}}',
        },
    ])

    my_deck= genanki.Deck(
    2059454210,
    output_filename)

    for word in target_list:
        speak = gTTS(text=word, lang=target_lng, slow=False) 
        #print("Text to be spoken:", w)
        if not word[0].isalpha():
            continue
        else:
            speak.save("src/"+word+".mp3")

    my_package = genanki.Package(my_deck)

    missing = 0


    for native_word, target_word in zip(native_list, target_list):
        if type(native_word) == float or type(target_word) == float:
            continue
        else:
            #check to see if the sound file exists
            if os.path.isfile('src/'+target_word+'.mp3'):
                my_note = genanki.Note(
                    model = my_model_1,
                    fields=[native_word, target_word, '[sound:' +target_word +'.mp3' ']'])
                my_deck.add_note(my_note)
            else:
                print (f"NO-{target_word}.mp3 does NOT exist")
                missing += 1
                my_note = genanki.Note(
                    model = my_model_1,
                    fields=[native_word, target_word, 'audio does not exist'])
                my_deck.add_note(my_note)
    print(f"{missing} files missing")
            
            
    warnings.filterwarnings('ignore', module='genanki', message='^Field contained the following invalid HTML tags')
    
    
    
    my_package = genanki.Package(my_deck)

    file_path = 'src/'
    med = []
    for file in target_list:
        full_file = file_path + file +".mp3"
        try:
            med.append(full_file)
        except FileNotFoundError as fe:
            print(f"{full_file} not found")
            continue
    
    my_package.media_files = med


    try:
        my_package.write_to_file(f"{output_filename}.apkg")
    except FileNotFoundError as fe:
        print(f"file not found when trying to write: '{fe}' ")

# --------------------------------------------------

class Args(NamedTuple):
    """ Command-line arguments """
    txt: str
    target_lng: str
    native_lng: str
    output:str
    separator: str

# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Anki Card Generator',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # because there is no default, then it must have a value
    parser.add_argument('txt', metavar='txt', help='Input text file of target language',
                        type=str)
    parser.add_argument('target',
                        metavar='TARGET',
                        help='The target language (the language of the text file).' \
                        ' Note: must be written in ISO 639 format. For example:\nArabic: ar\n' \
                        'English: en\nSwedish: sv\nMore can be found at https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes',
                        type=str)
    parser.add_argument(
        "-n",
        "--nat",
        metavar="NATIVE",
        help="help='The native language (the language that the text file will be translated into).\n"
        "Note: must be written in ISO 639 format. For example:\n"
        "Arabic: ar\n"
        "English: en\n"
        "Swedish: sv\n"
        "More can be found at https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes\n"
        "Default is English'",
        type=str,
        default="en",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="OUTPUT",
        help="Name of the output file. Default is output.apkg",
        type=str,
        default="output",
    )
    parser.add_argument(
        "-s",
        "--sep",
        metavar="SEPARATOR",
        help="The character by which the text file is delimited. By default, the delimiter is whitespace ' '",
        type=str,
        default=' ',
    )

    args = parser.parse_args()
    print(args)

    return Args(args.txt, args.target, args.nat, args.output, args.sep)
# --------------------------------------------------
def main() -> None:

    args = get_args()
    file_path, target, native, output, sep = args

    print(f'file path = "{file_path}"')
    print(f'target = "{target}"')
    print(f'native = "{native}"')
    print(f'output = "{output}"')
    print(f'sep = "{sep}"')

    

    target_word_list = text_to_word_list(file_path, sep)
    native_word_list = translate_target_words_to_native(target_word_list, target, native)
    create_anki_deck(target_word_list, native_word_list, target, output)


# --------------------------------------------------
if __name__ == '__main__':
    main()