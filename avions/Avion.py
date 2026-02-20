from moteurs.ReseauMoteur import ReseauMoteur
from constantes.Constantes import Constantes
from inputs.Inputs import Inputs
from .Masse import Masse
from .Aero import Aero

import csv
import os

class Avion:
    Name                    = ""     # Nom du modèle d'avion
    Manufacturer            = ""     # Nom du constructeur
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

    t                       = 0.     # Temps écoulé
    h_t                     = 0.     # Altitude actuelle (m)

    l_t                     = 0.     # Distance totale parcourue (m)    
    l_climb                 = 0.     # Distance nécessaire pour la montée (m)
    l_cruise                = 0.     # Distance nécessaire pour la croisière (m)
    l_descent               = 0.     # Distance nécessaire pour la descente (m)
    l_descent_diversion     = 0.     # Distance de la descente en diversion (m)

    t_climb                 = 0.     # Temps nécessaire à la montée
    t_cruise                = 0.     # Temps nécessaire à la croisière
    t_descent               = 0.     # Temps nécessaire à la descente
    t_diversion             = 0.     # Temps nécessaire à la diversion
    t_holding               = 0.     # Temps nécessaire à la phase de holding

    diversion               = False  # Etat de l'avion (en diversion ou non)
    cruise                  = False  # Etat de l'avion (en croisière ou non)

    def __init__(self, full_path = Inputs.getAirplaneFile(), engine_path = Inputs.getEngineFile(), m_payload = Inputs.m_payload):
        '''
        Initialise un objet Avion en lisant les paramètres depuis un fichier CSV.

        :param m_payload: Masse de la payload (kg)
        '''

        full_path = Inputs.getAirplaneFile() #On utilise la méthode statique de la classe Inputs pour obtenir le chemin complet du fichier csv de l'avion
        
        # Si fichier non trouvé
        if not os.path.isfile(full_path):
            raise FileNotFoundError(f"Le fichier {full_path} n'a pas été trouvé. Veuillez vérifier le chemin et le nom du fichier CSV de l'avion.")

        # Lecture CSV
        with open(full_path, mode='r', encoding='utf-8') as f:
            # Ouverture du fichier
            lecteur = csv.reader(f, delimiter=';')

            # Lecture ligne par ligne
            for ligne in lecteur:

                if len(ligne) == 2:
                    # Récupération des noms de paramètre (clé) et de leur valeur
                    cle, valeur = ligne

                    # Conversion en float si possible
                    try:
                        valeur = float(valeur)
                    except ValueError:
                        pass

                    # Attribution dynamique des attributs
                    setattr(self, cle, valeur)

        # Initialisation des sous-classes
        self.Masse = Masse(self, m_payload)
        self.Aero = Aero(self)
        self.Moteur = ReseauMoteur(self, engine_path)

        # Initialisation des approximations des longueurs de descente
        self.setupDescentes()

    def reset(self):
        '''
        Remet l'avion à ses conditions initiales (altitude, distance, vitesse, masse).
        '''
        self.t         = 0.     # Temps écoulé
        self.l_t       = 0.     # Distance totale parcourue (m)    
        self.h_t       = 0.     # Altitude actuelle (m)
        self.diversion = False  # Etat de l'avion (en diversion ou non)
        self.cruise    = False  # On est pas en croisière
        self.Masse.initializeMission()

    def setupDescentes(self):
        '''
        Initialise les paramètres pour la première estimation de descente à partir des Inputs (règle de 3: il faut ~3 nautiques pour descendre de 1000 pieds).
        '''
        self.l_descent = 3 * Inputs.hCruise_ft / 1000 * Constantes.conv_NM_m
        self.l_descent_diversion = 3 * Inputs.cruiseDiversionAlt_ft / 1000 * Constantes.conv_NM_m

    def setl_descent(self, l_descent: float):
        '''
        Définit la distance nécessaire pour la descente.

        :param l_descent: Distance nécessaire pour la descente (m)
        '''
        self.l_descent = l_descent

    def setl_descent_diversion(self, l_descent_diversion: float):
        '''
        Définit la distance nécessaire pour la descente en diversion.
        
        :param l_descent_diversion: Distance necessaire pour la descente en diversion (m)
        '''
        self.l_descent_diversion = l_descent_diversion

    def Add_l_descent(self, dl_descent: float):
        '''
        Ajoute une distance dl_descent à la distance nécessaire pour la descente.

        :param dl_descent: Distance à ajouter à la distance de descente (m)
        '''
        self.l_descent += dl_descent

    def Add_l_descent_diversion(self, dl_descent_diversion: float):
        '''
        Ajoute une distance dl_descent à la distance nécessaire pour la descente de la diversion.

        :param dl_descent: Distance à ajouter à la distance de descente de la diversion (m)
        '''
        self.l_descent_diversion += dl_descent_diversion

    def Add_dl(self, dl: float):
        '''
        Ajoute une distance dl à la distance totale parcourue par l'avion.
        
        :param dl: Distance à ajouter (m)
        '''
        self.l_t += dl

    def Add_dt(self, dt: float):
        '''
        Ajoute un pas de temps dt au compteur total.

        :param dt: Pas de temps à ajouter
        '''
        self.t += dt

    def set_h(self, h: float):
        '''
        Définit l'altitude actuelle de l'avion.
        
        :param h: Altitude à définir (m)
        '''
        self.h_t = h

    def set_l(self, l: float):
        '''
        Définit la distance parcourue par l'avion.
        
        :param h: Distance à définir (m)
        '''
        self.l_t = l

    def Add_dh(self, dh: float):
        '''
        Ajoute une variation d'altitude dh à l'altitude actuelle de l'avion.
        
        :param dh: Variation d'altitude à ajouter (m)
        '''
        self.h_t += dh

    def geth(self):
        '''
        Renvoie l'altitude actuelle de l'avion (m).
        '''
        return self.h_t
    
    def getl(self):
        '''
        Renvoie la distance parcourue par l'avion (m).
        '''
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
    
    def getl_descent(self):
        '''
        Retourne la valeur actuelle de la distance de la descente.
        '''
        return self.l_descent
    
    def getl_descent_diversion(self):
        '''
        Retourne la valeur actuelle de la distance de la descente en diversion.
        '''
        return self.l_descent_diversion
    
    

    
   