#!/usr/bin/env python

import os
from pytwitter import StreamApi
import re
import words

regex = re.compile(".*Wordle (?P<day>\d+) \d/6\n\n(?P<grid>([🟩🟧🟨🟦⬛⬜]{5}\n)+).*")

# normalize colour scheme
def normalize_char(c):
    # Colorblind mode correct
    if c == '🟧':
        return '🟩'
    # Colorblind mode wrong spot
    if c == '🟦':
        return '🟨'
    # Light theme
    if c == '⬜':
        return '⬛'
    return c

def normalize(line):
    return list(map(normalize_char, line))

def valid_candidate(candidate, line):
    # Characters that are not right and in the correct spot
    wrong_chars_in_candidate = [c for c, rule in zip(candidate, line) if rule != '🟩']

    # At least one of all the valid words needs to match, otherwise the
    # candidate cannot be the solution
    for other in words.candidates:
        match = True

        for c, o, rule in zip(candidate, other, line):
            # Correct letter in the correct spot
            if rule == '🟩':
                if c != o:
                    match = False
                    break
            # Correct letter in the wrong spot
            elif rule == '🟨':
                if c == o or o not in wrong_chars_in_candidate:
                    match = False
                    break
            # Incorrect letter
            else:
                if o in wrong_chars_in_candidate:
                    match = False
                    break

        # There was a match, no need to continue
        if match:
            return True

    return False

class DaySolver():
    def __init__(self):
        # Maybe more fair? But takes even longer
        # self.candidates = words.candidates

        self.candidates = words.solutions

    def refine(self, line):
        self.candidates = list(filter(lambda c: valid_candidate(c, line), self.candidates))

    def print_summary(self):
        l = len(self.candidates)
        print(f"{l} candidates left")
        if l < 10:
            for candidate in self.candidates:
                print(candidate)

class WordleSolver(StreamApi):
    def __init__(self, bearer_token):
        super().__init__(bearer_token)
        self.solvers = {}

    def on_tweet(self, tweet):
        o = regex.match(tweet.text)
        if o is not None:
            day = o.group("day")
            grid = o.group("grid")

            if day not in self.solvers:
                self.solvers[day] = {
                    "solver": DaySolver(),
                    "line_cache": [],
                    "tweet_count": 0,
                }

            lines = [normalize(line) for line in grid.splitlines()]

            if len(lines) > 6:
                # Not a tweet we want to use
                return

            print(tweet.text)
            self.solvers[day]["tweet_count"] += 1

            for line in lines:
                # No need to refine with a line seen before
                if line not in self.solvers[day]["line_cache"]:
                    self.solvers[day]["solver"].refine(line)
                    self.solvers[day]["line_cache"].append(line)

            print()
            print(f"Day {day}:", end=' ')
            self.solvers[day]["solver"].print_summary()

            tweets = self.solvers[day]["tweet_count"]
            unique_lines = len(self.solvers[day]["line_cache"])
            print(f"Using {tweets} tweets, and {unique_lines} unique lines")

            print()
            print("================")
            print()

if __name__ == "__main__":
    bearer_token = os.getenv("BEARER_TOKEN")

    stream = WordleSolver(bearer_token)

    # Cleanup existing rules
    rules = stream.get_rules().data
    ids = [rule.id for rule in rules]

    if ids != []:
        stream.manage_rules(rules={
            "delete": {
                "ids": ids,
            }
        })

    stream.manage_rules(rules={
        "add": [
            # Match on Wordle related tweets and attempt to reduce invalid clues
            {"value": 'Wordle 6 (🟩 OR 🟧) -is:retweet -fake -clone'}
        ],
    })

    stream.search_stream()
