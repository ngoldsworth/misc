import itertools
import collections
from math import comb


class card:
    def __init__(
        self,
        value: str or int,
        suit: str,
    ):
        self._v = value
        self._s = suit

    def __str__(self):
        return "{}{}".format(self._v, self._s)

    @property
    def value(self):
        return self._v

    @property
    def suit(self):
        return self._s

    @property
    def points(self) -> int:
        if self._v in ["J", "Q", "K"]:
            return 10
        elif self._v == "A":
            return 1
        else:
            return int(self._v)

    @property
    def seq(self) -> int:
        if self._v == "J":
            return 11
        elif self._v == "Q":
            return 12
        elif self._v == "K":
            return 13
        elif self._v == "A":
            return 1
        else:
            return int(self._v)


def hand_points(
    cut: card,
    hand: list,
):
    h = hand + [cut]
    p = 0

    # s = ''
    # s += str(cut)
    # s += '|'
    # for c in hand:
    #     s+=str(c)
    #     s+=', '
    # print(s)

    # counter is useful for runs and pairs
    counter = collections.Counter([c.value for c in h])

    # detect runs
    if len(counter) <= 2:
        # a run is at least 3 cards
        pass
    else:
        pass

    # find 15's
    for r in range(2, 6):
        vals = [c.points for c in h]
        for cm in itertools.combinations(vals, r):
            if sum(cm) == 15:
                p += 2

    # check for a full flush
    # a full flush means no multiples
    if len(set([c.suit for c in h])) == 1:
        p += 5

    else:
        # check for pairs
        for k in counter:
            v = counter[k]
            if v > 1:
                p += 2 * comb(v, 2)

        # check for flush in just the hand
        if len(set(c.suit for c in hand)) == 1:
            p += 4

    return p


if __name__ == "__main__":
    deck = []
    suits = ["D", "S", "H", "C"]
    values = list(range(2, 11)) + ["A", "J", "Q", "K"]
    for s in suits:
        for v in values:
            deck.append(card(v, s))

    four = [card("K", "H"), card("K", "S"), card("K", "D"), card(5, "C")]
    c = card(5, "D")

    p = hand_points(c, four)
    print(p)
