class Match:
    def __init__(self,player_a,player_b,payoff_matrix):   
       
        #Inizializza i giocatori e i parametri del match
       
        self.player_a = player_a  #Istanza sottoclasse di Strategy
        self.player_b = player_b
        self.payoff_matrix = payoff_matrix #Istanza di classe PayoffMatrix
        self.history_a = []  # Lista di mosse (Servono per le strategie)
        self.history_b = []
        self.score_a = 0
        self.score_b = 0

        # Liste per l'analisi dettagliata del match
        self.payoffs_a = []
        self.payoffs_b = []
        self.cumulative_scores_a = []
        self.cumulative_scores_b = []
    
    def play_round(self):

        # Si chiamano i metodi move() dei giocatori
        move_a = self.player_a.decide(self.history_b)
        move_b = self.player_b.decide(self.history_a)
        
        # Si calcolano i payoff
        payoff_a,payoff_b = self.payoff_matrix.compute(move_a,move_b)
        
     
        # Aggiorna le liste di mosse per le istanze di Strategy
        self.history_a.append(move_a)
        self.history_b.append(move_b)
        
        # Aggiorna i parametri del match
        self.score_a += payoff_a
        self.score_b += payoff_b

        # Aggiorna le liste per l'analisi dettagliata
        self.payoffs_a.append(payoff_a)
        self.payoffs_b.append(payoff_b)
        self.cumulative_scores_a.append(self.score_a)
        self.cumulative_scores_b.append(self.score_b)
        
        return (move_a,move_b,self.score_a,self.score_b)

    def run(self, rounds):
        for i in range(rounds):
            self.play_round()
            
        return {
            "agent_a": self.player_a.name, # Assumendo che le strategie abbiano un attributo .name
            "agent_b": self.player_b.name,
            "score_a": self.score_a,
            "score_b": self.score_b,
            "history_a": self.history_a,
            "history_b": self.history_b,
            "payoffs_a": self.payoffs_a,
            "payoffs_b": self.payoffs_b,
            "cumulative_scores_a": self.cumulative_scores_a,
            "cumulative_scores_b": self.cumulative_scores_b
        }