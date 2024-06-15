import program as pr
import string


def has_alpha(s):
    return any(char.isalpha() for char in s)
def text_to_str(file_path, separator = ' '):
    try:
        text = list(open(file_path,'r').readlines())
        text = [line.rstrip('\n') for line in text]
        text = " ".join(text)
        text = text.split(sep = separator)
        text = [word.lower() for word in text]
        #text = [pr.re.sub(r"\b[.,'\"!?;:-]+|[.,'\"!?;:-]+\b", "", w) for w in text]
        # text = [pr.re.sub(r"\n", "", w) for w in text]
        text = [item for item in text if has_alpha(item)]
        # text = [pr.re.sub(r"\”", "", w) for w in text]
        text = list(set([w for w in text]))

        return text
    except FileNotFoundError:
        print("File not found.")
        return []


def main() -> None:

    args = pr.get_args()
    file_path, target, native, output, sep = args
    

    target_word_list = text_to_str(file_path, sep)
    print(target_word_list)
    #print(" ".join(target_word_list))
    native_word_list = pr.translate_target_words_to_native(target_word_list, target, native)
    pr.create_anki_deck(target_word_list, native_word_list, target, output)


# --------------------------------------------------
if __name__ == '__main__':
    main()