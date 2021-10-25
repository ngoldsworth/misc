import pathlib as pl
import re
from string import ascii_lowercase

def possible_words(
        file: pl.Path,
        word: str,
        excluded: str
):

    word = '^' + word.replace('_', '[^'+excluded+']') + '$'
    for line in open(file, "r").readlines():
        m = re.search(word,  line)
        if m != None:
            print(m.group(0))

def best_next_word(
        file: pl.Path,
        word: str,
        excluded: str
):
    alphabet = dict()
    for char in ascii_lowercase:
        alphabet = {**alphabet, char:0}

    print(alphabet['z'])





if __name__ == '__main__':
    possible_words(pl.Path('./wordlist.txt'), '_____e', 'zr')
    #best_next_word(pl.Path('./wordlist.txt'), 'word', 'zr')

