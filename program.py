
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



def text_to_word_list(file_path, separator = ' ') -> list:
    try:
        #opens the file for reading
        with open(file_path, 'r') as file:
            text = file.read()
            # Split the text into words using whitespace as separator
            word_list = text.split(sep = separator)
            for n in range(len(word_list)):
                if separator == ' ':
                    new_word = re.sub(r"\W", "", word_list[n])
                elif separator == '.':
                    new_word = re.sub(r"^ |[^\w\s]", "", word_list[n])
                word_list[n] = new_word
            #remove duplicates
            word_list = [i for i in word_list if i != '']
            word_list = [word.lower() for word in word_list]
            word_list = list(dict.fromkeys(word_list))  
            print([word for word in word_list])      
        return word_list
    except FileNotFoundError:
        print("File not found.")
        return []


def list_to_csv(word_list, output_file):
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            #create the header row
            writer.writerow(["Word"])
            for word in word_list:
                writer.writerow([word])
        print(f"List successfully exported to {output_file}")
    except Exception as e:
        print(f"Error occurred while exporting to CSV: {e}")



def translate_word(word, target_language, native_language = 'en'):
    translator = Translator()
    translation = translator.translate(word, src=target_language, dest=native_language)
    if translation is not None and translation.text is not None:
        return translation.text
    else:
        print(f"Translation failed for word: {word}")
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

def create_anki_deck(target_list, native_list, target_lng):

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
        'afmt': '{{FrontSide}}<hr id="answer">{{Target}}{{Target_Audio}}',
        },
    ])

    my_deck= genanki.Deck(
    2059454210,
    'HARRY P APR 10 10:57 PM')

    for word in target_list:
        speak = gTTS(text=word, lang=target_lng, slow=False) 
        #print("Text to be spoken:", w)
        if not word[0].isalpha():
            continue
        else:
            speak.save("sounds/"+word+".mp3")

    my_package = genanki.Package(my_deck)

    missing = 0

    #e = native_word
    #s = target_word

    for native_word, target_word in zip(native_list, target_list):
        if type(native_word) == float or type(target_word) == float:
            continue
        else:
            #print(f"i am in create an ki  where native is : {native_word} and target is {target_word}")
            #check to see if the sound file exists
            if os.path.isfile('sounds/'+target_word+'.mp3'):
                #print (f"YES-{s}.mp3 does exist")
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
            
            
    # print(my_deck)
    warnings.filterwarnings('ignore', module='genanki', message='^Field contained the following invalid HTML tags')
    
    
    
    my_package = genanki.Package(my_deck)

    file_path = 'sounds/'
    med = []
    for file in target_list:
        full_file = file_path + file +".mp3"
        if os.path.isfile(full_file): 
            print("file name is: ", full_file)
            med.append(full_file)
        else:
            print(f"{full_file} not found")
            continue
    
    #print(med)
    my_package.media_files = med


    try:
        my_package.write_to_file('sentences/swe_eng.apkg')
    except FileNotFoundError as fe:
        print(f"file not found when trying to write: '{fe}' ")

# --------------------------------------------------

class Args(NamedTuple):
    """ Command-line arguments """
    txt: str
    target_lng: str
    native_lng: str

# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Anki Card Generator',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    #because there is no default, then it must have a value
    parser.add_argument('txt', metavar='txt', help='Input text file of target language',
                        type=str)
    parser.add_argument('target',
                        metavar='trg',
                        help='The target language (the language of the text file).' \
                        ' Note: must be written in ISO 639 format. For example:\nArabic: ar\n' \
                        'English: en\nSwedish: sv\nMore can be found at https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes',
                        type=str)
    parser.add_argument('-n',
                    '--nat',
                    metavar='nat',
                    help='The native language (the language that the text file will be translated into).' \
                    ' Note: must be written in ISO 639 format. For example:\nArabic: ar\n' \
                    'English: en\nSwedish: sv\nMore can be found at https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes\n' \
                    'Default is English',
                    type=str,
                    default='en')

    args = parser.parse_args()
    print(args)

    # if os.path.isfile(args.txt):
    #     args.txt = open(args.txt).read().rstrip()

    #the name comes from the metavar
    return Args(args.txt, args.target, args.nat)
# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """
    


    args = get_args()
    file_path = args.txt
    target = args.target_lng
    native = args.native_lng

    print(f'file path = "{file_path}"')
    print(f'target = "{target}"')
    print(f'native = "{native}"')

    
    #2. convert the txt to a list based on separator (where the default is ' ')
    target_word_list = text_to_word_list(file_path)
    #3. put the word list to csv 
    #4. Translate swed words to engl
    native_word_list = translate_target_words_to_native(target_word_list, target, native)
    #5.combine the csv files to one 
    # deck_as_csv = combine_csv(target_word_list, native_word_list)
    #6. Create an anki deck 
    create_anki_deck(target_word_list, native_word_list, target)
        


# --------------------------------------------------
if __name__ == '__main__':
    main()

