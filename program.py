""" Anki Card Generator """

from googletrans import Translator
import genanki 
import os.path
import warnings
from gtts import gTTS 
import re
import argparse
from typing import NamedTuple
import time
import random
import parser


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
    # def handle_separator(self, sep):
    #     match sep:
    #         case '.':
    #             print('x')

    
def text_to_word_list(file_path, separator = ' '):
    try:
        word_list = parser.perform_split(file_path, separator)
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
        print(translated_list)
        return translated_list
    except Exception as e:
        print("Error in translating your list. An empty list is returned.")
        return []

# --------------------------------------------------

def create_anki_deck(target_list, native_list, target_lng, output_filename):

    
    r1 = random.randint(10, 1000000)
    r2 = random.randint(10, 1000000)
    my_model_1 = genanki.Model(
    r1,
    'Example',
    fields=[
        {'name': 'Native Language'},
        {'name': 'Target'},
        {'name': 'Target_Audio'}
    ],
    templates=[
        {
        'name': 'Card 1',
        'qfmt': '<span style="font-size: 40px;">{{Native Language}}',
        'afmt': '<span style="font-size: 40px;">{{FrontSide}}<hr id="answer">{{Target}}<br>{{Target_Audio}}',
        },
    ])

    my_model_reversed = genanki.Model(
    r2,
    'Reversed',
    fields=[
        {'name': 'Target'},
        {'name': 'Target_Audio'},
        {'name': 'Native Language'}
    ],
    templates=[
        {
        'name': 'Card 1',
        'qfmt': '<span style="font-size: 40px;">{{Target}} <br> {{Target_Audio}}',
        'afmt': '<span style="font-size: 40px;">{{FrontSide}}<hr id="answer">{{Native Language}}',
        },
    ])

    my_deck= genanki.Deck(
    r2+1,
    output_filename)

    my_deck_2= genanki.Deck(
        r2+2,
        f"{output_filename}_reversed")

    for word in target_list:
        speak = gTTS(text=word, lang=target_lng, slow=False) 
        print("Text to be spoken:", word)
        if not word[0].isalpha():
            continue
        else:
            speak.save("src/"+word+".mp3")

    my_package = genanki.Package(my_deck)
    my_package2 = genanki.Package(my_deck_2)

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
                my_note2 = genanki.Note(
                    model = my_model_reversed,
                    fields=[target_word, '[sound:' +target_word +'.mp3' ']', native_word])
                my_deck.add_note(my_note)
                my_deck_2.add_note(my_note2)
            else:
                print (f"NO-{target_word}.mp3 does NOT exist")
                missing += 1
                continue
    print(f"{missing} files missing")
            
            
    warnings.filterwarnings('ignore', module='genanki', message='^Field contained the following invalid HTML tags')
    
    
    
    my_package = genanki.Package(my_deck)
    my_package2 = genanki.Package(my_deck_2)

    file_path = 'src/'
    med = []
    for file in target_list:
        full_file = file_path + file +".mp3"
        if os.path.isfile(full_file):
            try:
                med.append(full_file)
            except FileNotFoundError as fe:
                print(f"{full_file} not found")
                continue
    
    my_package.media_files = med
    my_package2.media_files = med


    try:
        my_package.write_to_file(f"{output_filename}.apkg")
        my_package2.write_to_file(f"{output_filename}_reversed.apkg")
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
    #--- CHANGE TO THIS---#
    # parser.add_argument('file',
    #                     metavar='FILE', 
    #                     help='Input text file(s)',
    #                     nargs = '+',
    #                     type=argparse.FileType('rt'))
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