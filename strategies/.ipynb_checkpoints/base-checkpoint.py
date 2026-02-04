from abc import ABC, abstractmethod
# Punto chiave: POLIMORFISMO
# Questo e' lo schema base per le strategie *(Interfaccia comune)
class Strategy(ABC):
    def __init__(self, name=None):
        # Assegna un nome alla strategia. Se non fornito, usa il nome della classe.
        self.name = name or self.__class__.__name__

    @abstractmethod
    def decide(self, opponent_history): # Abbastanza esplicativo da solo
        pass

