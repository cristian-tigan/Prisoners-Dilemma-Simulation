from strategies.base import Strategy

class AlwaysCooperate(Strategy):
    def decide(self, opponent_history):
        return 'C'

class AlwaysDefect(Strategy):
    def decide(self, opponent_history):
        return 'D'
