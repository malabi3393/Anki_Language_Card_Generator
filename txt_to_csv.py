import csv
from googletrans import Translator


#takes a text fiel and turns it into a list of words 
def text_to_word_list(file_path):
    ch = [',', '.', '"', '”']
    try:
        with open(file_path, 'r') as file:
            text = file.read()
            # Split the text into words using whitespace as separator
            word_list = text.split()
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

# Example usage:
file_path = 'twisted_ch1.txt'  # Replace 'example.txt' with your file path
words = text_to_word_list(file_path)
swed_list = 'swed_list.txt' 
eng_list = 'eng_list.csv'
print(words)
list_to_csv(words, 'sw.csv')

# translator = Translator()
# translations = translator.translate(words)
# print(translations)

# for t in translations:
#     print(t.origin, '->', t.text)