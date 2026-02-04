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


class MutantRandom(Strategy):
    """
    Strategy con gene p (propensione a cooperare) e parametro gamma
    (probabilità che p muti in un nuovo valore uniforme in [0, 1]).
    """
    def __init__(self, p=0.5, gamma=0.1, name=None):
        super().__init__(name or f"Mutant(p={p:.2f},γ={gamma:.2f})")
        self.p = p
        self.gamma = gamma

    def mutate(self):
        """
        Con probabilità gamma, rimpiazza p con un nuovo valore ~ U(0, 1).
        """
        if npr.rand() < self.gamma:
            self.p = npr.uniform(0.0, 1.0)
            # aggiorno anche il nome per riflettere il nuovo gene (opzionale)
            self.name = f"Mutant(p={self.p:.2f},γ={self.gamma:.2f})"

    def decide(self, opponent_history):
        """
        Decide se cooperare o defezionare in base a p.
        La mutazione è pensata come evento "di generazione", quindi
        di solito chiamerai mutate() tra una generazione e la successiva,
        non a ogni mossa. Qui non mutiamo ad ogni decide().
        """
        return npr.choice(['C', 'D'], p=[self.p, 1 - self.p])
    