import csv
from googletrans import Translator

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

# --------------------------------------------------
def main() -> None:
    # Example usage:
    input_file = 'sw.csv'  # Replace 'swedish_words.csv' with the path to your input CSV file
    output_file = 'translated_words.csv'  # Choose the output file name
    translate_swedish_words_to_english(input_file, output_file)

# --------------------------------------------------
if __name__ == '__main__':
    main()