from collections import Counter
import pickle
import words

def get_pattern(goal, word):
    out = ['⬛' for _ in range(5)]

    for i, (g, o) in enumerate(zip(goal, word)):
        if g == o:
            out[i] = '🟩'

    # Count incorrect chars
    char_counts = Counter([ c for (c, r) in zip(goal, out) if r != '🟩' ])

    for i, rule in enumerate(out):
        if rule == '⬛' and char_counts[word[i]] > 0:
            out[i] = '🟨'
            char_counts[word[i]] -= 1

    return "".join(out)

class Candidate():
    def __init__(self, word):
        self.word = word
        self.patterns = set()

        for other in words.candidates:
            self.patterns.add(get_pattern(word, other))

    def valid(self, line):
        return line in self.patterns

try:
    with open("initial_candidates.pickle", 'rb') as f:
        initial_candidates = pickle.load(f)
except FileNotFoundError:
    print("Building initial_candidates")
    # Maybe it would be a bit more fair to use words.candidates instead of
    # words.solutions
    initial_candidates = [ Candidate(word) for word in words.solutions ]
    print("Done")

    with open("initial_candidates.pickle", 'wb') as f:
        pickle.dump(initial_candidates, f)

    print("Pickled initial_candidates")
