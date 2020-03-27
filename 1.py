import random

with open('sowpods.txt') as file:
    w_list = file.readlines()
r_word = random.choice(w_list).rstrip().lower()

no_lives = int(input('no_lives:')) # must be positive int
word_letters = set(r_word)
guessed_letters = []
correct_guessed_letters = []
curr_guess = ''

while no_lives > 0:
    if curr_guess == r_word:
        print(f"{curr_guess}")
        print('You win!')
        break
    else:
        print(f"no_lives: {no_lives}")
        print(f"guessed letters: {guessed_letters}")
        print(f"current guess: {curr_guess}")
        guess = input('Guess:').lower()
        if guess in guessed_letters:
            print('You already guessed that letter')
        else:
            guessed_letters.append(guess)
            if guess in word_letters:
                correct_guessed_letters.append(guess)
                curr_guess = r_word
                for letter in word_letters:  # remove all letters except those
                    # correctly guessed
                    if letter not in correct_guessed_letters:
                        curr_guess = curr_guess.replace(letter, '-')
            else:
                no_lives -= 1

if no_lives == 0:
    print('You lose')

