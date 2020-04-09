import csv
import random


def get_battle_directory():
    battle_directory = dict()
    with open("battle_data.csv") as f:
        dict_reader = csv.DictReader(f)
        for row in dict_reader:
            row_copy = row.copy()
            del row_copy['Attacker']
            battle_directory[row['Attacker']] = row_copy
        return battle_directory


def face_off(battle_directory, contestants, contender):
    """contestants must be in battle_directory"""
    r_opponent = random.choice(contestants)
    return r_opponent, battle_directory[contender][r_opponent]


class Game:
    """Make callable"""

    def __init__(self):
        self.wins = 0
        self.losses = 0
        self.draws = 0

    def __call__(self):
        battle_directory = get_battle_directory()
        contestants = [contestant for contestant, stats in
                       battle_directory.items()]
        print("Input <quit> to exit game at any point")
        while True:
            print(f"Contestants: {contestants}")
            user_input = input('Enter contender:').lower().capitalize()
            grammar_wins = lambda: self.wins == 1 and 'win' or 'wins'
            grammar_losses = lambda: self.losses == 1 and 'loss' or 'losses'
            grammar_draws = lambda: self.draws == 1 and 'draw' or 'draws'
            message = lambda: f"You have {self.wins} {grammar_wins()}, " \
                              f"{self.losses} {grammar_losses()}, and " \
                              f"{self.draws} {grammar_draws()}"
            if user_input == 'Quit':
                print("Game ended. " + message())
                return
            elif user_input not in contestants:
                print('Invalid contender')
                continue
            else:
                result = face_off(battle_directory, contestants, user_input)
                if result[1] == 'win':
                    self.wins += 1
                elif result[1] == 'lose':
                    self.losses += 1
                else:
                    self.draws += 1
                print(f"{user_input} {result[1]}s against {result[0]}. " +
                      message())


if __name__ == '__main__':
    game = Game()
    game()
