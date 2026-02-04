from strategies.base import Strategy
import numpy.random as npr

# strategies/classic.py
class TitForTat(Strategy):
    def decide(self, opponent_history):
        # Se è il primo turno, collabora
        if not opponent_history:
            return 'C'
        # Altrimenti copia l'ultima mossa dell'avversario
        return opponent_history[-1]

class Random(Strategy):
    def __init__(self, p=0.5, name=None):
        super().__init__(name)
        self.p = p

    def decide(self, opponent_history):
        return npr.choice(['C', 'D'], p=[self.p, 1 - self.p])
    