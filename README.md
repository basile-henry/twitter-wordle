# Twitter Wordle

Solve the daily [`wordle`](https://www.powerlanguage.co.uk/wordle/) by simply looking at twitter.

Given enough `wordle` win tweets we can recover what the word of the day is. Each line in the pattern lets us refine what words the answer could be.

```
Wordle 213 5/6

⬛⬛⬛🟨⬛
⬛🟩⬛⬛🟨
⬛🟩🟩⬛⬛
🟩🟩🟩⬛⬛
🟩🟩🟩🟩🟩

Day 213: 15 candidates left
Using 892 tweets, and 80 unique lines
```

[Here](https://gist.github.com/0bc62a95def5aa205705af66a0fd5bf8) is an example run of `twitter-wordle` on day 215 (20 Jan 2022) which took around 40 seconds to gather enough tweets (74) and unique lines (61) to narrow in on only 1 candidate.

## Spoilers

It should be obvious but don't run this if you don't want spoilers. Actually, don't even look at `words.py` as it contains an explicit list of past and future solutions.

## Running

This project depends on [`python-twitter-v2`](https://pypi.org/project/python-twitter-v2/) which can be installed manually with `pip` or one of the many other python package managers. Alternatively there is a `shell.nix` which provides all the needed dependencies.

In order to use the Twitter API, you will need to [sign up](https://developer.twitter.com/en/docs/twitter-api) and then set the `BEARER_TOKEN` environment variable.

```sh
nix-shell
export BEARER_TOKEN=...
python twitter_wordle.py
```

## Notes

- Some days it can take quite a while to gather enough unique lines to find a solution.
- This method assumes no adversarial tweets are in the feed. If you end up with 0 candidates someone could be messing with you, just restart the search.

## License

[MIT - Copyright 2022 Basile Henry](./LICENSE)
