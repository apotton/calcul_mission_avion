from missions.Croisiere import Croisiere
from missions.Descente import Descente
from missions.Montee import Montee

class Mission:
    def __init__(self):
        self.Montee = Montee()
        self.Croisiere = Croisiere()
        self.Descente = Descente()