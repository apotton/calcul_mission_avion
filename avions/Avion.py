from moteurs.ReseauMoteur import ReseauMoteur
from constantes.Constantes import Constantes
from inputs.Inputs import Inputs
from .Masse import Masse
from .Aero import Aero

import csv
import os

class Avion:
    Name                    = ""     # Nom du modèle d'avion
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
    l_diversion             = 0.     # Distance de la diversion (m)
    l_holding               = 0.     # Distance de la holding

    t_climb                 = 0.     # Temps nécessaire à la montée
    t_cruise                = 0.     # Temps nécessaire à la croisière
    t_descent               = 0.     # Temps nécessaire à la descente
    t_diversion             = 0.     # Temps nécessaire à la diversion
    t_holding               = 0.     # Temps nécessaire à la phase de holding

    cruise                  = False  # Etat de l'avion (en croisière ou non)

    saveAvion               = {}     # Dictionnaire des variables avion
    saveAero                = {}     # Dictionnaire des variables aéro
    saveMoteur              = {}     # Dictionnaire des variables moteur

    def __init__(self, Inputs: Inputs):
        '''
        Initialise un objet Avion en lisant les paramètres depuis un fichier CSV.

        :param m_payload: Masse de la payload (kg)
        '''
        plane_path = Inputs.getAirplaneFile()
        engine_path = Inputs.getEngineFile()
        
        # Si fichier non trouvé
        if not os.path.isfile(plane_path):
            raise FileNotFoundError(f"Le fichier {plane_path} n'a pas été trouvé. Veuillez vérifier le chemin et le nom du fichier CSV de l'avion.")

        # Lecture CSV
        with open(plane_path, mode='r', encoding='utf-8') as f:
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

        # Variables qu'il est plus pratique d'avoir ici (unités SI)
        self.Vw = Inputs.Vw_kt * Constantes.conv_kt_mps # Passage de kt à m/s
        self.CI = Inputs.CI_kg_min / 60 # Passage de kg/min à kg/s

        # Initialisation des sous-classes
        self.Inputs = Inputs
        self.Masse = Masse(self)
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
        self.l_descent = 3 * self.Inputs.hCruise_ft / 1000 * Constantes.conv_NM_m
        self.l_descent_diversion = 3 * self.Inputs.cruiseDiversionAlt_ft / 1000 * Constantes.conv_NM_m


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
    
    def get_t(self):
        ''' Renvoie le temps interne de l'avion. '''
        return self.t

    # Montée
    def set_t_climb(self, t_climb):
        self.t_climb = t_climb

    def get_t_climb(self):
        return self.t_climb
    
    def set_l_climb(self, l_climb):
        self.l_climb = l_climb
        
    def get_l_climb(self):
        return self.l_climb
    

    # Croisière
    def set_t_cruise(self, t_cruise):
        self.t_cruise = t_cruise

    def get_t_cruise(self):
        return self.t_cruise
    
    def set_l_cruise(self, l_cruise):
        self.l_cruise = l_cruise

    def get_l_cruise(self):
        return self.l_cruise

    # Descente
    def set_t_descent(self, t_descent):
        self.t_descent = t_descent
    
    def get_t_descent(self):
        return self.t_descent

    def get_l_descent(self):
        return self.l_descent
    
    def setl_descent(self, l_descent: float):
        '''
        Définit la distance nécessaire pour la descente.

        :param l_descent: Distance nécessaire pour la descente (m)
        '''
        self.l_descent = l_descent

    # Diversion
    def set_t_diversion(self, t_diversion):
        self.t_diversion = t_diversion

    def get_t_diversion(self):
        return self.t_diversion
    
    def set_l_diversion(self, l_diversion):
        self.l_diversion = l_diversion

    def get_l_diversion(self):
        return self.l_diversion

    def getl_descent_diversion(self):
        '''
        Retourne la valeur actuelle de la distance de la descente en diversion.
        '''
        return self.l_descent_diversion
    
    def setl_descent_diversion(self, l_descent_diversion: float):
        '''
        Définit la distance nécessaire pour la descente en diversion.
        
        :param l_descent_diversion: Distance necessaire pour la descente en diversion (m)
        '''
        self.l_descent_diversion = l_descent_diversion
    
    # Holding
    def set_t_holding(self, t_holding):
        self.t_holding = t_holding
    
    def get_t_holding(self):
        return self.t_holding
    
    def set_l_holding(self, l_holding):
        self.l_holding = l_holding

    def get_l_holding(self):
        return self.l_holding
    
    # Enregistrement de l'état actuel
    def save(self):
        '''
        Enregistre dans la classe avion les variables instantannées afin de 
        les récupérer plus tard.
        '''
        self.saveAvion = {
            "h_t": self.h_t,
            "l_t": self.l_t,
            "t"  : self.t
        }

        self.saveAero = {
            "Cx_t"  : self.Aero.Cx_t,
            "Cz_t"  : self.Aero.Cz_t,
            "Mach_t": self.Aero.Mach_t,
            "CAS_t" : self.Aero.CAS_t,
            "TAS_t" : self.Aero.TAS_t,
            "SGR_t" : self.Aero.SGR_t ,
            "SAR_t" : self.Aero.SAR_t ,
            "ECCF_t": self.Aero.ECCF_t
        }

        self.saveMoteur = {
            "F_t"   : self.Moteur.F_t,
            "FF_t"  : self.Moteur.FF_t,
            "SFC_t" : self.Moteur.SFC_t
        }
    
    def loadSave(self):
        '''
        Remet les variables instantannées à leur valeur sauvegardée.
        '''
        # Données Avion
        for key, value in self.saveAvion.items():
            setattr(self, key, value)

        # Données Aero
        for key, value in self.saveAero.items():
            setattr(self.Aero, key, value)

        # Données moteur
        for key, value in self.saveMoteur.items():
            setattr(self.Moteur, key, value)