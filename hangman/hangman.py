import pathlib as pl
import re
from string import ascii_lowercase

def possible_words(
        file: pl.Path,
        word: str,
        excluded: str
):
    big_collection = ''

    for c in word:
        if(c!='_'):
            excluded+=c

    word = '^' + word.replace('_', '[^'+excluded+']') + '$'
    for line in open(file, "r").readlines():
        m = re.search(word,  line.lower())
        if m != None:
            print(m.group(0))
            big_collection += m.group(0)

    lst = list(big_collection) 

    for c in excluded:
        for item in lst:
            if(item==c):
                lst.remove(c)

    print(max(set(lst), key=lst.count))


def best_next_word(
        file: pl.Path,
        word: str,
        excluded: str
):
    alphabet = dict()
    for char in ascii_lowercase:
        alphabet = {**alphabet, char:0}

    





if __name__ == '__main__':
    main_word = 'cr___'
    excludes =  'sotlirp'
    possible_words(pl.Path('./hangman/wordlist.txt'), main_word, excludes)
    # best_next_word(pl.Path('./wordlist.txt'), 'word', 'zr')

