""" Anki Card Generator """

from googletrans import Translator
import genanki 
import os.path
import os
import warnings
from gtts import gTTS 
import re
import argparse
from typing import NamedTuple
import time
import random
from parser import perform_split
import concurrent.futures
import logging 
from card import Card
from anki_models import my_model_1, my_model_reversed
from args import get_args





card_deck = []

def text_to_word_list(file_path, target, separator = ' '):
    try:
        word_list = perform_split(file_path, separator)
        for word in word_list:
            new_card(word, target)
        
    except FileNotFoundError:
        print("File not found.")
        return []

def new_card(word, target, card_deck = card_deck):
    card = Card(word, target)
    card_deck.append(card)

def translate_word(card: Card, to_lg = 'en'):
    translator = Translator()
    translation = translator.translate(card.from_word, src=card.from_lg, dest=to_lg)
    
    if translation.text is not None:
        return translation.text
    else:
        return ''  # or return the original word or any other default value

def translate_target_words_to_native(card_deck = card_deck):



    def get_translation(card: Card):
        try:
            translated_word = translate_word(card)
            card.set_translated_word(translated_word)
        except Exception as e:
            print(f"Translation failed for word: {card.from_word}. Error: {e}")
    try:
        with concurrent.futures.ThreadPoolExecutor() as e:
            e.map(get_translation, card_deck)
        print(f"Translations successfully exported to list...")
        return card_deck
    except Exception as e:
        print("Error in translating your list. An empty list is returned.")
        return []

# --------------------------------------------------

def create_anki_deck(output_filename, card_deck = card_deck):

    
    r1 = random.randint(10, 1000000)
    r2 = random.randint(10, 1000000)


    my_deck= genanki.Deck(
    r2+1,
    output_filename)

    my_deck_2= genanki.Deck(
        r2+2,
        f"{output_filename}_reversed")
    
    file_path = 'media'
    if not os.path.exists(file_path): os.makedirs(file_path)

    def get_pronounciation(card:Card):
        speak = gTTS(text=card.from_word, lang=card.from_lg, slow=False)
        print("Text to be spoken:", card.from_word)
        speak.save(os.path.join(file_path, f'{card.fn}.mp3'))

    with concurrent.futures.ThreadPoolExecutor() as e:
        e.map(get_pronounciation, card_deck)
    
    print('Got all the sounds ...')
    my_package = genanki.Package(my_deck)
    my_package2 = genanki.Package(my_deck_2)

    
    def make_card(card: Card):
        missing = 0
        #check to see if the sound file exists
        if os.path.isfile('media/'+card.fn+'.mp3'):
            if hasattr(card, 'translated_word'):
                my_note = genanki.Note(
                    model = my_model_1,
                    fields=[card.translated_word, card.from_word, card.soundtag])
                my_note2 = genanki.Note(
                    model = my_model_reversed,
                    fields=[card.from_word, card.soundtag, card.translated_word])
                my_deck.add_note(my_note)
                my_deck_2.add_note(my_note2)
        else:
            print (f"NO: {card.fn}.mp3 does NOT exist")
            missing += 1
    
    for card in card_deck:
        make_card(card)

    #print(f"{missing} files missing")
            
            
    warnings.filterwarnings('ignore', module='genanki', message='^Field contained the following invalid HTML tags')
    
    
    
    my_package = genanki.Package(my_deck)
    my_package2 = genanki.Package(my_deck_2)

    
    media = []

    for card in card_deck:
        full_file = os.path.join(file_path, f'{card.fn}.mp3')
        if os.path.isfile(full_file):
            try:
                media.append(full_file)
            except FileNotFoundError as fe:
                print(f"{full_file} not found")
                continue
    
    
    my_package.media_files = media
    my_package2.media_files = media


    try:
        filename1 = f"{output_filename}.apkg"
        filename2 = f"{output_filename}_reversed.apkg"
        my_package.write_to_file(f"{output_filename}.apkg")
        my_package2.write_to_file(f"{output_filename}_reversed.apkg")
        return [filename1, filename2]
    except FileNotFoundError as fe:
        print(f"file not found when trying to write: '{fe}' ")

# --------------------------------------------------



# --------------------------------------------------

# --------------------------------------------------
def main() -> None:

    args = get_args()
    
    file_path, target, native, output, sep, *rest = args
    print(f' the seperator is {sep}')
    if sep == 'line':
        sep = '\n'


    
    t0 = time.perf_counter()
    text_to_word_list(file_path, target, sep)
    print('got the text and made it to a word list')
    translate_target_words_to_native()
    print('translated the words...making cards now')
    create_anki_deck(output)
    t1 = time.perf_counter()

    print(f"the program took {round(t1-t0, 2)} second(s)")


#--------------------------------------------------
if __name__ == '__main__':
    main()