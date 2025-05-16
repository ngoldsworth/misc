from wordle import five_letter_words


if __name__ == "__main__":
    alphabetical = sorted(five_letter_words("./hangman/wordlist.txt"))
    word_count = len(alphabetical)

    lower_bound = "stash"
    upper_bound = "steel"
    lower_proximity = .01
    upper_proximity = .15

    spread = 8

    idx_hi = word_count
    idx_lo = 0

    for j, word in enumerate(alphabetical):
        if word == lower_bound:
            idx_lo = j
            print(f"lower at {j}: {lower_bound}")
        if word == upper_bound:
            idx_hi = j
            print(f"upper at {j}: {upper_bound}")
            break

    bound_range = idx_hi - idx_lo

    # simple average
    idx_bin = (idx_lo + idx_hi) // 2

    guess_0, guess_1 = max(idx_bin - spread, 0), min(idx_bin + spread, word_count)

    print("BY BIN SEARCH")
    for word in alphabetical[guess_0:guess_1]:
        if word == lower_bound or word == upper_bound or word == alphabetical[idx_bin]:
            print(word.upper(), end=" ")
        else:
            print(word, end=" ")

    # using proximity
    idx_prox = int(
        idx_lo
        + lower_proximity * (idx_hi - idx_lo) / (lower_proximity + upper_proximity)
    )

    print(" ")
    print(idx_prox)

    guess_0, guess_1 = max(idx_prox - spread, 0), min(idx_prox + spread, word_count)

    print("BY PROXIMITY")
    for word in alphabetical[guess_0:guess_1]:
        if word == lower_bound or word == upper_bound or word == alphabetical[idx_prox]:
            print(word.upper(), end=" ")
        else:
            print(word, end=" ")

    # proximity matching
    idx_prox_match = 0
    if lower_proximity > upper_proximity:
        idx_prox_match = idx_lo + bound_range * (lower_proximity - upper_proximity) / (
            lower_proximity + upper_proximity
        )

    elif lower_proximity < upper_proximity:
        idx_prox_match = idx_lo + bound_range * (2 * lower_proximity) / (
            lower_proximity + upper_proximity
        )
    idx_prox_match = int(idx_prox_match)

    print(" ")
    print(idx_prox_match)

    guess_0, guess_1 = max(idx_prox_match - spread, 0), min(idx_prox_match + spread, word_count)

    print("PROXIMITY MATCH")
    for word in alphabetical[guess_0:guess_1]:
        if word == lower_bound or word == upper_bound or word == alphabetical[idx_prox]:
            print(word.upper(), end=" ")
        else:
            print(word, end=" ")
