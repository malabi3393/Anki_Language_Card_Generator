import argparse

def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Anki Card Generator',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # because there is no default, then it must have a value
    parser.add_argument('file',
                        metavar='FILE', 
                        help='Input text file(s)',
                        nargs = '+',
                        type=argparse.FileType('rt'))
    parser.add_argument('target',
                        metavar='TARGET',
                        help='The target language (the language of the text file).'
                        ' Note: must be written in ISO 639 format. For example:\nArabic: ar\n'
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
