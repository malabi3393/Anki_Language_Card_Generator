import unittest
import parser
import os

test_word_files = []
test_line_files = []



for file in os.listdir("./test_files/words"):
    test_word_files.append(f"test_files/words/{file}")
test_word_files = sorted(test_word_files)

for file in os.listdir("./test_files/lines"):
    test_line_files.append(f"test_files/lines/{file}")
test_line_files = sorted(test_line_files)
print(test_line_files)

class TestParser(unittest.TestCase):
    def test_word(self):
        self.assertEqual(parser.word(test_word_files[0]), {'the', 'cat', 'jumped'})

    def test_word_puncuations_beginning(self):
        self.assertEqual(parser.word(test_word_files[1]), {'the', 'cat', 'jumped'})

    def test_word_puncuations_end(self):
        self.assertEqual(parser.word(test_word_files[2]), {'the', 'cat', 'jumped'})

    def test_word_unique(self):
        self.assertEqual(parser.word(test_word_files[3]), {'the', 'cat', 'jumped', 'not'})
    
    def test_word_numbers(self):
        self.assertEqual(parser.word(test_word_files[4]), {'the', 'cat', 'jumped', '200', 'feet'})

    def test_word_many_lines(self):
        self.assertEqual(parser.word(test_word_files[5]), {'there', 'are', 'many', 'lines', 'in', 'this', 'doc'})

    def test_no_words(self):
        self.assertRaises(ValueError, parser.word, test_word_files[6])

    def test_empty_doc(self):
        self.assertRaises(ValueError, parser.word, test_word_files[7])

    #@unittest.SkipTest
    def test_other_sep(self):
        self.assertEqual(parser.other(test_word_files[8], ';'), {'the cat','the', 'jumped over', 'empty', 'dog', 'empty dog'})
    
    #@unittest.SkipTest
    def test_punctuated_words(self):
        self.assertEqual(parser.word(test_word_files[9]), {'m\'appelle', 'i\'m', 'the', 'je'})





  
    def test_line(self):
        self.assertEqual(parser.line(test_line_files[0]), {'juMPed !The \\\"cat cAt, CAT! jumped', 'The cat jumped'})
    def test_line_end(self):
        self.assertEqual(parser.line(test_line_files[1]), {'There are 7 lines and then text, then more lines'})
    
    
    



if __name__ == '__main__':
    unittest.main()