#!python3
# Code Challenge 02 - Word Values Part II - a simple game
# http://pybit.es/codechallenge02.html

from data import DICTIONARY, LETTER_SCORES, POUCH
import random
import itertools

NUM_LETTERS = 7


def calc_word_value(word):
    """Calc a given word value based on Scrabble LETTER_SCORES mapping"""
    return sum(LETTER_SCORES.get(char.upper(), 0) for char in word)


def max_word_value(word_lst=None):
    """Calculate the word with the max value, can receive a list
    of words as arg, if none provided uses default DICTIONARY"""
    return max(word_lst, key=calc_word_value)


DRAW = list(random.sample(POUCH, NUM_LETTERS))


def _validate(word, draw):
    """assumes draw is uppercase list of letters"""
    draw_copy = draw[:]
    for letter in word.upper():
        if letter in draw:
            draw_copy.remove(letter)
        else:
            return False
    return word.lower() in DICTIONARY


def input_word():
    while True:
        print(f"Draw: {','.join(DRAW)}")
        user_word = input('Form Word:')
        if user_word.lower() == 'quit_':  # bewaring case of valid word 'quit'
            return
        elif not _validate(user_word, DRAW):
            print(f"Invalid word: {user_word}")
            continue
        else:
            return user_word


def _draw_permutations(draw):
    for i in range(1, 8):
        yield from list(itertools.permutations(draw, i))


def possible_words(draw):
    return {"".join(permutation).lower()
            for permutation in _draw_permutations(draw)}


def main():
    user_word = input_word()
    if not user_word:
        return
    possible_w = possible_words(DRAW) & set(DICTIONARY)
    optimal_word = max_word_value(list(possible_w))
    optimal_word_score = calc_word_value(optimal_word)
    user_word_score = calc_word_value(user_word)
    user_score = user_word_score / optimal_word_score
    print(f"Word formed: {user_word} (value: {user_word_score})")
    print(f"Optimal word: {optimal_word} (value: {optimal_word_score})")
    print(f"Your score: {user_score} (optimal word value / user word value)")


if __name__ == '__main__':
    main()
