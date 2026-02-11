from enregistrement.Enregistrement import Enregistrement
from Montee import Montee
from Descente import Descente
from Croisiere import Croisiere
from atmosphere.Atmosphere import Atmosphere
from constantes.Constantes import Constantes
from inputs.Inputs import Inputs
from avions.Avion import Avion
import numpy as np

class Mission:
    @staticmethod
    def Principal(Avion : Avion, Atmosphere: Atmosphere, Inputs: Inputs):

        
        Descente.Descendre(Avion, Atmosphere, dt = Inputs.dt_descent)
