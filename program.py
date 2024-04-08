import csv
from googletrans import Translator
import pandas as pd 
import genanki 
import os
import glob

def text_to_word_list(file_path, sepa = ' '):
    ch = [',', '.', '"', '”']
    try:
        with open(file_path, 'r') as file:
            text = file.read()
            # Split the text into words using whitespace as separator
            word_list = text.split(sep = sepa)
            word_list = [w.lower() for w in word_list]
            word_list = [w.replace('.', '') for w in word_list]
            word_list = [w.replace('"', '') for w in word_list]
            word_list = [w.replace(',', '') for w in word_list]
            word_list = [w.replace('”', '') for w in word_list]
            word_list = list(dict.fromkeys(word_list))
        return word_list
    except FileNotFoundError:
        print("File not found.")
        return []


def list_to_csv(word_list, output_file):
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
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


def translate_swedish_words_to_english(input_file, output_file):
    try:
        with open(input_file, 'r', newline='') as csv_in, open(output_file, 'w', newline='') as csv_out:
            reader = csv.reader(csv_in)
            writer = csv.writer(csv_out)
            for row in reader:
                translated_row = []
                for word in row:
                    try:
                        translated_word = translate_word(word, source_language='sv', target_language='en')
                        translated_row.append(translated_word)
                    except Exception as e:
                        print(f"Translation failed for word: {word}. Error: {e}")
                        translated_row.append('')  # Append an empty string as translation
                writer.writerow(translated_row)
        print(f"Translations successfully exported to {output_file}")
    except Exception as e:
        print(f"Error occurred while translating and exporting CSV: {e}")


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
    eng = df['0'].tolist()
    sw = df['1'].tolist()

    

    my_deck = genanki.Deck(
    2059400110,
    'Twisted Love Chapter 1 Sentences')

    for e, s in zip(eng, sw):
        my_note = genanki.Note(
            model = genanki.BASIC_MODEL,
            fields=[e, s])
        my_deck.add_note(my_note)
    print("we are fine hereiojhiojios")
    genanki.Package(my_deck).write_to_file('sentences/twisted_love_sentences.apkg')

# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    #1. import the file - txt 
    file_path = 'twisted_ch1.txt'
    text_to_words = text_to_word_list(file_path)
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

