
import random
import time
import argparse

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def add_score(self, turn_score):
        self.score += turn_score


class ComputerPlayer(Player):
    def make_decision(self, turn_score):
        threshold = min(25, 100 - self.score)
        if turn_score >= threshold:
            return 'h'
        else:
            return 'r'


class Die:
    def __init__(self, sides=6):
        self.sides = sides
        random.seed(0)
    
    def roll(self):
        return random.randint(1, self.sides)


class Game:
    def __init__(self, players):
        self.players = players
        self.die = Die()
        self.current_player_index = 0

    def switch_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def play_turn(self):
        current_player = self.players[self.current_player_index]
        turn_score = 0
        
        while True:
            if isinstance(current_player, ComputerPlayer):
                decision = current_player.make_decision(turn_score)
            else:
                decision = input(f"{current_player.name}, do you want to roll or hold? (r/h): ").strip().lower()
            
            if decision == 'r':
                roll = self.die.roll()
                if roll == 1:
                    print(f"Sorry, {current_player.name}, you rolled a 1. No points for this turn.")
                    turn_score = 0
                    break
                else:
                    turn_score += roll
                    print(f"{current_player.name}, you rolled a {roll}. Turn score: {turn_score}, Total score: {current_player.score + turn_score}")
            elif decision == 'h':
                break
        
        current_player.add_score(turn_score)
        self.switch_player()

    def check_winner(self):
        for player in self.players:
            if player.score >= 100:
                return player
        return None


class TimedGameProxy:
    def __init__(self, game):
        self.game = game
        self.start_time = time.time()

    def play_turn(self):
        if time.time() - self.start_time > 60:
            print("Time's up!")
            self.end_game_due_to_time()
        else:
            self.game.play_turn()

    def end_game_due_to_time(self):
        scores = [(player.name, player.score) for player in self.game.players]
        winner = max(scores, key=lambda x: x[1])
        print(f"The winner is {winner[0]} with a score of {winner[1]}.")

    def check_winner(self):
        return self.game.check_winner()


def play_game(player1_type='human', player2_type='human', timed=False):
    player_types = {'human': Player, 'computer': ComputerPlayer}
    
    players = [player_types[player1_type](f"Player 1"), player_types[player2_type](f"Player 2")]
    game = Game(players)
    
    if timed:
        game = TimedGameProxy(game)
    
    while True:
        game.play_turn()
        winner = game.check_winner()
        if winner:
            print(f"Congratulations, {winner.name}! You won with a score of {winner.score}.")
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--player1', type=str, default='human')
    parser.add_argument('--player2', type=str, default='human')
    parser.add_argument('--timed', action='store_true')
    
    args = parser.parse_args()
    play_game(args.player1, args.player2, args.timed)
