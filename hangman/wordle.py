import re
import collections


def test_yellows(word: str, yellows):
    for k, vi in yellows.items():
        if k not in word:
            return False

        if isinstance(vi, tuple) or isinstance(vi, list):
            for i in vi:
                if word[i] == k:
                    return False
        else:
            if word[vi] == k:
                return False

    return True


def test_greens(word: str, greens):
    for j, letter in enumerate(greens):
        if letter != "_" and word[j] != letter:
            return False

    return True


def test_excluded(word: str, excluded):
    as_set = set(list(word))
    return len(as_set & excluded) == 0


def five_letter_words(file):
    pat = re.compile("^(\w\w\w\w\w)$")

    wordlst = open(file, "r").readlines()
    wordlst.reverse()
    for line in wordlst:
        m = re.search(pat, line.lower())
        if m != None:
            yield m[1]


def guess_compare(guess, answer):
    if len(guess) != 5:
        raise ValueError("guess must be 5 letters long")

    comparison = ""

    for j, letter in enumerate(guess):
        if letter not in answer:
            comparison += "x"
        else:
            if letter in answer and guess[j] != answer[j]:
                comparison += "Y"
            else:
                comparison += "G"

    return comparison


if __name__ == "__main__":
    yellows = {
        # 'n': (0, 3) # n is not in spot 0 or spot 3
        
    }
    # greens = "_a_er"
    greens = "_____"
    excluded_letters = "craneolspuy"

    excluded = set(list(excluded_letters))

    # print(guess_compare('paint', 'yacht'))

    possibles = []
    lettercounter = collections.Counter()
    for word in five_letter_words("./hangman/wordlist2.txt"):
        if (
            test_greens(word, greens)
            and test_excluded(word, excluded)
            and test_yellows(word, yellows)
        ):
            # if len(word) == len(set(word)):
            #     print(word.upper())
            # else:
            #     print(word)
            w = word.lower()
            possibles.append(w)

            lettercounter += collections.Counter(w)

    # give each possible letter a "score" based on frequency of its letters
    scored = {}
    for word in possibles:
        scored[word] = sum(lettercounter[c] for c in word)

    d = dict(sorted(scored.items(), key=lambda item: item[1], reverse=True))
    for k, v in d.items():
        print(k,v)
    print(len(d))
