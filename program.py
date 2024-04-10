import csv
from googletrans import Translator
import pandas as pd 
import genanki 
import os.path
import glob
import warnings
from gtts import gTTS 
import re



def text_to_word_list(file_path, separator = ' '):
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



def translate_word(word, source_language='sv', target_language='en'):
    translator = Translator()
    translation = translator.translate(word, src=source_language, dest=target_language)
    if translation is not None and translation.text is not None:
        return translation.text
    else:
        print(f"Translation failed for word: {word}")
        return ''  # or return the original word or any other default value


# def translate_swedish_words_to_english(input_file, output_file):
#     try:
#         with open(input_file, 'r', newline='') as csv_in, open(output_file, 'w', newline='') as csv_out:
#             reader = csv.reader(csv_in)
#             writer = csv.writer(csv_out)
#             for row in reader:
#                 translated_row = []
#                 for word in row:
#                     try:
#                         translated_word = translate_word(word, source_language='sv', target_language='en')
#                         translated_row.append(translated_word)
#                     except Exception as e:
#                         print(f"Translation failed for word: {word}. Error: {e}")
#                         translated_row.append('')  # Append an empty string as translation
#                 writer.writerow(translated_row)
#         print(f"Translations successfully exported to {output_file}")
#     except Exception as e:
#         print(f"Error occurred while translating and exporting CSV: {e}")

def translate_swedish_words_to_english(source_list):
    translated_list = []
    for word in source_list:
        try:
            translated_word = translate_word(word, source_language= 'sv', target_language='en')
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



def combine_csv(file1, file2) -> str:
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    df_append = pd.DataFrame()
    csv_files = [df1, df2]
    for file in csv_files:
        df_append = pd.concat([df_append, file], ignore_index= True, axis = 1)
    
    deck_name = 'sentences/sentence_deck.csv'
    df_append.to_csv(deck_name, index = False)
    return deck_name

def create_anki_deck(filename):

    #import files
    data = pd.read_csv(filename)
    df = pd.DataFrame(data)
    sw = df['0'].tolist()
    eng = df['1'].tolist()

    my_model_1 = genanki.Model(
    1380120064,
    'Example',
    fields=[
        {'name': 'English'},
        {'name': 'Swedish'},
        {'name': 'Swedish_Audio'}
    ],
    templates=[
        {
        'name': 'Card 1',
        'qfmt': '{{English}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Swedish}}{{Swedish_Audio}}',
        },
    ])

    my_model_2 = genanki.Model(
    1380120164,
    'Example',
    fields=[
        {'name': 'English'},
        {'name': 'Swedish'},
    ],
    templates=[
        {
        'name': 'Card 1',
        'qfmt': '{{English}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Swedish}}',
        },
    ])
    

    my_deck= genanki.Deck(
    2059400210,
    'Anki sound deck TWISTED APR 10 2:26 PM')

    for w in sw:
        speak = gTTS(text=w, lang='sv', slow=False) 
        #print("Text to be spoken:", w)
        if not w[0].isalpha():
            continue
        else:
            speak.save("sounds/"+w+".mp3")

    my_package = genanki.Package(my_deck)

    missing = 0

    for e, s in zip(eng, sw):
        if type(e) == float or type(s) == float:
            continue
        else:
            #check to see if the sound file exists
            if os.path.isfile('sounds/'+s+'.mp3'):
                #print (f"YES-{s}.mp3 does exist")
                my_note = genanki.Note(
                    model = my_model_1,
                    fields=[e, s, '[sound:' +s +'.mp3' ']'])
                my_deck.add_note(my_note)
            else:
                print (f"NO-{s}.mp3 does NOT exist")
                missing += 1
                my_note = genanki.Note(
                    model = my_model_1,
                    fields=[e, s, 'audio does not exist'])
                my_deck.add_note(my_note)
    print(f"{missing} files missing")
            
            
    # print(my_deck)
    warnings.filterwarnings('ignore', module='genanki', message='^Field contained the following invalid HTML tags')
    
    
    
    my_package = genanki.Package(my_deck)

    file_path = 'sounds/'
    med = []
    for file in sw:
        if os.path.isfile(file):
            full_file = file_path + file +".mp3" 
            #print("file name is: ", full_file)
            med.append(full_file)
        else:
            continue
    
    #print(med)
    my_package.media_files = med


    try:
        my_package.write_to_file('sentences/iiiitwisted_love_sentences.apkg')
    except FileNotFoundError as fe:
        print(f"file not found when trying to write: '{fe}' ")


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """
    

    #1. import the file - txt 
    file_path = 'twisted_ch1.txt'
    
    #2. convert the txt to a list based on separator (where the default is ' ')
    words = text_to_word_list(file_path)
    #3. put the word list to csv 
    list_to_csv(words, 'sentences/twisted_sentences_swed.csv')
    #4. Translate swed words to engl
    translate_swedish_words_to_english('sentences/twisted_sentences_swed.csv', 'sentences/twisted_sentences_eng.csv')
    #5.combine the csv files to one 
    deck_as_csv = combine_csv('sentences/twisted_sentences_swed.csv', 'sentences/twisted_sentences_eng.csv')
    #6. Create an anki deck 
    create_anki_deck(deck_as_csv)
        


# --------------------------------------------------
if __name__ == '__main__':
    main()

