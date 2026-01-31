import numpy as np
import pandas as pd
from core.payoff import PayoffMatrix
from core.match import Match
from strategies import *


class RoundRobinTournament:
    def __init__(self, players, N_rounds,M):

        # Attributi per definire un torneo
        self.players = players # Lista di istanze Strategy
        self.N = len(players)
        self.N_rounds = N_rounds # Numero di round per Match
        self.M = M # Payoff Matrix

        # Attributi per statistiche dei risultati
        self.N_wins = np.zeros(self.N) # Come dimensione devono avere il numero di player
        self.N_ties = np.zeros(self.N)
        self.Total_score = np.zeros(self.N)

         # Liste vuote per salvare ogni match giocato
        self.matches = []
        self.results = []
        self.dfs = []

    def create_matches(self):
        for i in range(self.N):
            for j in range(i+1,self.N):
                #Create a Match for the single tournament's round
                m = Match(self.players[i],self.players[j],self.M)
                self.matches.append((i,j,m))
    
    def play_tournament(self,output = True):

        self.create_matches()
        for i,j,match in self.matches:
            
            #Running al matches in the tournament
            result = match.run(rounds = self.N_rounds)
            self.results.append(result)
            
            name1 = result['agent_a']
            name2 = result['agent_b']
            score1 = result['score_a']
            score2 = result['score_b']

            # Evaluating the total number of wins
            if score1 > score2:
                self.N_wins[i] += 1
            elif score1 < score2:
                self.N_wins[j] += 1
            else:
                self.N_ties[i] += 1
                self.N_ties[j] += 1
                

            # Evaluating the total score

            self.Total_score[i] += score1
            self.Total_score[j] += score2
            
            
            if output:
                print(' ')
                print(f"INCONTRO TRA {name1} - {name2}:")
                print(f"{name1}: {score1} punti")
                print(f"{name2}: {score2} punti")
                print(' ')
            
            # Se vuoi vedere il dettaglio round per round:
            df = pd.DataFrame({
                result['agent_a']: result['history_a'], 
                result['agent_b']: result['history_b']
            })
            self.dfs.append(df)