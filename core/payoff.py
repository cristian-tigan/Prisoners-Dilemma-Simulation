class PayoffMatrix:
    def __init__(self, T=5, R=3, P=1, S=0):

        if not (T > R > P > S):
            raise ValueError(
            f"Use values to satisfy T > R > P > S. "
            f"Ricevuto: T={T}, R={R}, P={P}, S={S}"
        )

        if not (2 * R > T + S):
            raise ValueError(
                f"Use values to satisfy : 2R > T + S. "
                f"Ricevuto: 2R={2*R}, T+S={T+S} (T={T}, R={R}, S={S})"
            )
        self.T = T
        self.R = R
        self.P = P
        self.S = S
    
    def compute(self,move_a,move_b):

        if move_a == move_b: # Se entrambi i giocatori scelgono la stessa mossa
            if move_a == 'C': # Se entrambi cooperano hanno R
                payoff_a = self.R
                payoff_b = self.R
            else: # Se entrambi defezionano hanno P
                payoff_a = self.P
                payoff_b = self.P
        else:
            if move_a == 'C': # Se A coopera e B defeziona A ha Sucker e B ha Temptation
                payoff_a = self.S
                payoff_b = self.T
            else: # Se A defeziona e B coopera A ha Temptation e B ha Sucker
                payoff_a = self.T
                payoff_b = self.S
        
        return (payoff_a,payoff_b)
    

    
        