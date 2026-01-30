# Refined Implementation Plan: Modular Architecture

> [!NOTE]
> **Obiettivo**: Definire un'architettura essenziale, modulare ed estendibile per il progetto "Prisoner's Dilemma".
> **Focus**: Logica di gioco (`Core`), definizione strategie (`Strategies`) e gestione tornei (`Tournaments`).
> **Esclusioni**: La persistenza dei dati è rimossa per focalizzarsi sul funzionamento logico.

## 1. Perché questa Architettura?

L'approccio proposto separa nettamente **CHI gioca** (Strategia) da **COME si gioca** (Game/Tournament).

### Vantaggi Chiave per il Team
1.  **Parallelismo**: Tizio implementa `TitForTat`, Caio implementa `RoundRobin`, Sempronio lavora sul `Game` engine. Nessuno si calpesta i piedi.
2.  **Isolamento**: Se la strategia `Grudger` esplode, non rompe il motore di gioco.
3.  **Semplicità di Estensione**: Aggiungere una strategia significa scrivere *una sola classe* con un solo metodo. Non bisogna toccare il codice del torneo.

---

## 2. Core Modules: Il Cuore del Sistema

### `core/payoff.py`
Definisce le regole di punteggio. È un oggetto passivo che usa semplici stringhe ('C', 'D').

```python
class PayoffMatrix:
    def __init__(self, T=5, R=3, P=1, S=0):
        self.T, self.R, self.P, self.S = T, R, P, S

    def compute(self, move_a, move_b):
        """Restituisce i payoff (score_a, score_b) da una coppia di mosse."""
        if move_a == move_b:
            if move_a == 'C':
                return (self.R, self.R)
            else:
                return (self.P, self.P)
        else:
            if move_a == 'C':
                return (self.S, self.T)
            else:
                return (self.T, self.S)
```

### `core/match.py` (Ex Game)
Gestisce **una singola partita** tra due giocatori.

```python
class Match:
    def __init__(self, player_a, player_b, payoff_matrix):
        self.player_a = player_a
        self.player_b = player_b
        self.payoff_matrix = payoff_matrix
        self.history_a = []
        self.history_b = []
        self.score_a = 0
        self.score_b = 0

    def play_round(self):
        # 1. Chiede le mosse
        move_a = self.player_a.decide(self.history_b)
        move_b = self.player_b.decide(self.history_a) 

        # 2. Calcola Punteggi
        pa, pb = self.payoff_matrix.compute(move_a, move_b)

        # 3. Aggiorna Stato
        self.history_a.append(move_a)
        self.history_b.append(move_b)
        self.score_a += pa
        self.score_b += pb

        return (move_a, move_b, self.score_a, self.score_b)

    def run(self, rounds=100):
        for _ in range(rounds):
            self.play_round()
        return {
            "agent_a": self.player_a.name,
            "agent_b": self.player_b.name,
            "score_a": self.score_a,
            "score_b": self.score_b,
            "history_a": self.history_a,
            "history_b": self.history_b
        }
```

---

## 3. Strategies: L'Intelligenza

Tutte le strategie derivano da una classe base che gestisce il nome (Polimorfismo).

### `strategies/base.py`
```python
from abc import ABC, abstractmethod

class Strategy(ABC):
    def __init__(self, name=None):
        self.name = name or self.__class__.__name__

    @abstractmethod
    def decide(self, opponent_history):
        pass
```

### Esempio: Quanto è facile creare una strategia?

Vogliamo creare `TitForTat`. Dobbiamo implementare solo `decide`.

```python
# strategies/classic.py
class TitForTat(Strategy):
    def decide(self, opponent_history):
        # Se è il primo turno, collabora
        if not opponent_history:
            return 'C'
        # Altrimenti copia l'ultima mossa dell'avversario
        return opponent_history[-1]
```

Vogliamo creare `Random`?

```python
import random
class Random(Strategy):
    def decide(self, opponent_history):
        return random.choice(['C', 'D'])
```

---

## 4. Tournaments: L'Organizzazione

Il torneo è un livello superiore che orchestra molteplici `Match`.

### `tournaments/round_robin.py`

```python
class RoundRobinTournament:
    def __init__(self, strategies, payoff_matrix):
        self.strategies = strategies
        self.payoff = payoff_matrix
        self.results = []

    def run(self, rounds_per_match=100):
        import itertools
        for strat_a, strat_b in itertools.combinations(self.strategies, 2):
            match = Match(strat_a, strat_b, self.payoff)
            result = match.run(rounds=rounds_per_match)
            self.results.append(result)
```

---

## 5. Esempi di Flusso (Interaction Flow)

### Scenario A: Un Singolo Round (TitForTat vs AlwaysDefect)

Immaginiamo di essere al **Round 2**.
Storia precedente: `TitForTat` ha fatto 'C', `AlwaysDefect` ha fatto 'D'.
`opponent_history` per TitForTat è `['D']`.

1.  **Match** chiama `TitForTat.decide(['D'])`.
2.  **TitForTat** guarda l'ultima mossa ('D') e restituisce **'D'**.
3.  **Match** chiama `AlwaysDefect.decide(...)`.
4.  **AlwaysDefect** se ne frega dell'input e restituisce **'D'**.
5.  **Match** ha `('D', 'D')`. Chiama `PayoffMatrix.compute('D', 'D')`.
6.  **PayoffMatrix** restituisce `(1, 1)`.
7.  **Match** aggiorna i punteggi (`self.score_a += 1`) e le liste delle mosse.

---

## 6. Esempio Pratico: "Sotto il Cofano"

Analisi esatta delle chiamate per il **Round 2** tra `Player A` (TFT) e `Player B` (AllD).

**Stato Iniziale**: `history_a=['C']`, `history_b=['D']`, `score_a=0`, `score_b=5`.

1.  **`Match.play_round()`** inizia.
2.  Chiama **`TitForTat.decide(['D'])`**.
    *   Input: `['D']`
    *   Logica: ultimo elemento è 'D'.
    *   Output: `'D'`
3.  Chiama **`AlwaysDefect.decide(['C'])`**.
    *   Input: `['C']`
    *   Logica: sempre 'D'.
    *   Output: `'D'`
4.  Chiama **`PayoffMatrix.compute('D', 'D')`**.
    *   Input: `'D'`, `'D'`
    *   Logica: Caso `else` del primo if (move_a == move_b). Defezione mutua.
    *   Output: `(1, 1)`
5.  **`Match`** aggiorna:
    *   `self.score_a` = 0 + 1 => **1**
    *   `self.score_b` = 5 + 1 => **6**
    *   `self.history_a` => `['C', 'D']`
