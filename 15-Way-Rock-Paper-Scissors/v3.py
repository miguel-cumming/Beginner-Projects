import csv
import random
from getpass import getpass


def get_battle_directory():
    battle_directory = dict()
    with open("battle_data.csv") as f:
        dict_reader = csv.DictReader(f)
        for row in dict_reader:
            row_copy = row.copy()
            del row_copy['Attacker']
            battle_directory[row['Attacker']] = row_copy
        return battle_directory


def face_off(battle_directory, contestants, contender1, contender2=None):
    """Return whether contender1 wins, loses, or draws against contender2."""
    if not contender2:
        contender2 = random.choice(contestants)
    return contender2, battle_directory[contender1][contender2]


class Player:
    def __init__(self, id_, input_):
        self.id_ = id_
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.input_ = input_


def message():
    grammar_wins = lambda player: player.wins == 1 and 'win' or 'wins'
    grammar_losses = lambda \
            player: player.losses == 1 and 'loss' or 'losses'
    grammar_draws = lambda player: player.draws == 1 and 'draw' or 'draws'
    return lambda \
            player: f"Player {player.id_} has {player.wins} {grammar_wins(player)}, " \
                    f"{player.losses} {grammar_losses(player)}, and " \
                    f"{player.draws} {grammar_draws(player)}. "


def one_player_game():
    battle_directory = get_battle_directory()
    contestants = [contestant for contestant, stats in
                   battle_directory.items()]
    player1 = Player(1, None)
    message_ = message()
    while True:
        print(f"Input <quit> to exit game at any point. Contestants: {contestants}")
        player1.input_ = input('Enter contender:').lower().capitalize()
        if player1.input_ == 'Quit':
            print("Game ended. " + message_(player1))
            return
        if player1.input_ not in contestants:
            print('Invalid contender')
            continue

        result = face_off(battle_directory, contestants, player1.input_)
        if result[1] == 'win':
            player1.wins += 1
        elif result[1] == 'lose':
            player1.losses += 1
        else:
            player1.draws += 1

        print(
            f"({player1.input_}) {result[1]}s against ({result[0]}). " +
            message_(player1))


def two_player_game():
    battle_directory = get_battle_directory()
    contestants = [contestant for contestant, stats in
                   battle_directory.items()]
    player1 = Player(1, None)
    player2 = Player(2, None)
    message_ = message()
    while True:
        print(f"Input <quit> to exit game at any point. Contestants: {contestants}")
        player1.input_ = getpass('Player 1, enter contender:').lower().capitalize()
        if player1.input_ == 'Quit':
            print("Game ended. " + message_(player1) + message_(player2))
            return
        if player1.input_ not in contestants:
            print('Invalid contender')
            continue
        player2.input_ = getpass('Player 2, enter contender:').lower().capitalize()
        if player2.input_ == 'Quit':
            print("Game ended. " + message_(player1) + message_(player2))
            return
        if player2.input_ not in contestants:
            print('Invalid contender')
            continue

        result = face_off(battle_directory, contestants, player1.input_,
                          player2.input_)
        if result[1] == 'win':
            player1.wins += 1
            player2.losses += 1
        elif result[1] == 'lose':
            player1.losses += 1
            player2.wins += 1
        else:
            player1.draws += 1
            player2.draws += 1
        print(
            f"Player 1 ({player1.input_}) {result[1]}s against Player 2 ({result[0]}). " +
            message_(player1) + message_(player2))


if __name__ == '__main__':
    # one_player_game()
    two_player_game()  # On Pycharm requires: run --> edit configurations -->
    # execution --> emulate terminal in output console
