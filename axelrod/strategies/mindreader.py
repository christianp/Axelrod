from axelrod import Player, Axelrod
import copy
import inspect

class MindReader(Player):
    """A player that looks ahead at what the opponent will do and decides what to do."""

    name = 'Mind Reader'

    def strategy(self, opponent):
        """Pretends to play the opponent 50 times before each match.
        The primary purpose is to look far enough ahead to see if a defect will be punished by the opponent.
        If the MindReader attempts to play itself (or another similar strategy), then it will cause a recursion loop, so this is also handeled in this method, by defecting if the method is called by strategy
        """
        
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        calname = calframe[1][3]
        
        if calname == 'strategy':
            return 'D'

        best_strategy = self.look_ahead(opponent)

        return best_strategy

    def simulate_match(self, opponent, strategy, rounds = 10):
        """Simulates a number of matches."""
        for match in range(rounds):
            play_1, play_2 = strategy, opponent.strategy(self)
            self.history.append(play_1)
            opponent.history.append(play_2)

    def look_ahead(self, opponent, rounds = 10):
        """Plays a number of rounds to determine the best strategy."""
        results = []
        tournement = Axelrod()
        strategies = ['C', 'D']

        dummy_history_self = copy.copy(self.history)
        dummy_history_opponent = copy.copy(opponent.history)

        for strategy in strategies:
            self.simulate_match(opponent, strategy, rounds)
            results.append(tournement.calculate_scores(self, opponent)[0])

            self.history = copy.copy(dummy_history_self)
            opponent.history = copy.copy(dummy_history_opponent)

        return strategies[results.index(min(results))]
