import os
import csv

from moteurs.Reseau_moteur import Reseau_moteur
from .Aero import Aero
from .Masse import Masse
from inputs.Inputs import Inputs

class Avion:
    Name                    = 0.     # Nom du modèle d'avion
    Manufacturer            = 0.     # Nom du constructeur
    MaxTakeoffWeight        = 0.     # MTOW (kg)
    EmptyWeight             = 0.     # Masse à vide (kg)
    MaxFuelWeight           = 0.     # Masse carburant maximale (kg)
    MaxPLWeight             = 0.     # Masse Payload maximale (kg)
    Sref                    = 0.     # Surface de référence (m^2)
    Phi25deg                = 0.     # Angle de twist ou angle de calage (°)
    TtoCref                 = 0.     # Rapport entre l'épaisseur et la corde du profil ()
    Lref                    = 0.     # Longueur de référence (m)
    AspectRatio             = 0.     # Allongement (Envergure^2/Surface alaire)
    TaperRatio              = 0.     # Taux de flèche, rapport corde en bout d'aile sur corde à l'emplenture ()
    Camber                  = 0.     # Cambrure du profil ()
    MaxThicknessPosition    = 0.     # Position de l'épaisseur de profil maximale sur la corde ()
    DFuselage               = 0.     # Diamètre du fuselage (m)
    Envergure               = 0.     # Envergure de l'avion (m)
    KVMO                    = 0.     # Vitesse maximale opérationnelle(kt)
    MMO                     = 0.     # Mach maximal opérationnelle
    PressurisationCeilingFt = 0.     # Altitude maximale atteignable avec une cabine pressurisée (ft)
    Cx0Cruise               = 0.     # Cx0 en croisière ()
    Cx0Climb                = 0.     # Cx0 en montée ()
    Cx0Descent              = 0.     # Cx0 en descente ()
    OswaldClimb             = 0.     # Coefficient d'Oswald en montée ()
    OswaldCruise            = 0.     # Coefficient d'Oswald en croisière ()
    OswaldDescent           = 0.     # Coefficient d'Oswald en descente ()

    l_t                     = 0.     # Distance totale parcourue (m)    
    h_t                     = 0.     # Altitude actuelle (m)

    def __init__(self):
        '''
        Initialise un objet Avion en lisant les paramètres depuis un fichier CSV.
        '''

        full_path = Inputs.getAirplaneFile() #On utilise la méthode statique de la classe Inputs pour obtenir le chemin complet du fichier csv de l'avion
        
        # Si fichier non trouvé
        if not os.path.isfile(full_path):
            raise FileNotFoundError(f"Le fichier {full_path} n'a pas été trouvé. Veuillez vérifier le chemin et le nom du fichier CSV de l'avion.")

        # Lecture CSV
        with open(full_path, mode='r', encoding='utf-8') as f:
            lecteur = csv.reader(f, delimiter=';') #On lit le fichier csv
            for ligne in lecteur: #On lit chaque ligne
                if len(ligne) == 2:
                    cle, valeur = ligne #A chaque ligne on récupère le nom du paramètre qu'on appelle clé et sa valeur
                    # Conversion en float si possible
                    try:
                        valeur = float(valeur)
                    except ValueError:
                        pass

                    # Attribution dynamique des attributs
                    setattr(self, cle, valeur) #On crée les attributs à partir des clés du csv et on leur associe les valeurs du fichiers

        self.Masse = Masse(self)
        self.Aero = Aero(self)
        self.Moteur = Reseau_moteur(self, BPR=6, OPR=1.5)

        self.h_t = 0
        self.l_t = 0


    def Add_dl(self, dl: float):
        '''
        Ajoute une distance dl à la distance totale parcourue par l'avion.
        
        :param self: Instance de la classe Avion
        :param dl: Distance à ajouter (m)
        '''
        self.l_t += dl

    def set_h(self, h: float):
        '''
        Définit l'altitude actuelle de l'avion.
        
        :param self: Instance de la classe Avion
        :param h: Altitude à définir (m)
        '''
        self.h_t = h

    def Add_dh(self, dh: float):
        '''
        Ajoute une variation d'altitude dh à l'altitude actuelle de l'avion.
        
        :param self: Instance de la classe Avion
        :param dh: Variation d'altitude à ajouter (m)
        '''
        self.h_t += dh

    def geth(self):
        return self.h_t
    
    def getl(self):
        return self.l_t

    def __repr__(self):
        return f"<Avion: {getattr(self, 'Name', 'Unknown')}>"
    
    def getName(self):
        return self.Name
    
    def getManufacturer(self):
        return self.Manufacturer
    
    def getMaxTakeoffWeight(self):
        return self.MaxTakeoffWeight
    
    def getEmptyWeight(self):
        return self.EmptyWeight
    
    def getMaxFuelWeight(self):
        return self.MaxFuelWeight
    
    def getMaxPLWeight(self):
        return self.MaxPLWeight
    
    def getSref(self):
        return self.Sref
    
    def getPhi25deg(self):
        return self.Phi25deg
    
    def getTtoCref(self):
        return self.TtoCref
    
    def getLref(self):
        return self.Lref
    
    def getAspectRatio(self):
        return self.AspectRatio
    
    def getTaperRatio(self):
        return self.TaperRatio
    
    def getCamber(self):
        return self.Camber
    
    def getMaxThicknessPosition(self):
        return self.MaxThicknessPosition
    
    def getDFuselage(self):
        return self.DFuselage
    
    def getEnvergure(self):
        return self.Envergure
    
    def getKVMO(self):
        return self.KVMO
    
    def getMMO(self):
        return self.MMO
    
    def getPressurisationCeilingFt(self):
        return self.PressurisationCeilingFt
    
    def getCx0Cruise(self):
        return self.Cx0Cruise
    
    def getCx0Climb(self):
        return self.Cx0Climb
    
    def getCx0Descent(self):
        return self.Cx0Descent
    
    def getOswaldClimb(self):
        return self.OswaldClimb
    
    def getOswaldCruise(self):
        return self.OswaldCruise
    
    def getOswaldDescent(self):
        return self.OswaldDescent
    
    

    
   