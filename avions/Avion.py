import os
import csv
import numpy as np
from .Aero import Aero
from .Masse import Masse
from constantes.Constantes import Constantes
from atmosphere.Atmosphere import Atmosphere

class Avion:
    def __init__(self, nom_fichier_csv):

        # Dossier de ce fichier Avion.py
        base_dir = os.path.dirname(os.path.abspath(__file__)) #Renvoie le Directory du fichier actuel et remonte d'un cran
        csv_folder = os.path.join(base_dir, "csv_avions") #Ajoute le terme "csv_avions" au Directory précédent pour se rendre dans le Directory des fichiers csv à lire
        full_path = os.path.join(csv_folder, nom_fichier_csv) #Ajoute le nom du fichier csv au Directory afin de le compléter

        # Si fichier non trouvé
        if not os.path.isfile(full_path):
            raise FileNotFoundError(f"Fichier CSV non trouvé : {full_path}")

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
        self.Aero = Aero(self) #AJOUTER LE SELF.MOTEUR
        self.Moteur = None # À initialiser plus tard avec un objet Moteur

        self.Mach_t = 0
        self.CAS_t = 0
        self.TAS_t = 0
        self.h_t = 0
        self.l_t = 0


    ##Calcul des vitesses

    def Convert_Mach_to_CAS(self, Atmosphere):
        gamma = Constantes.gamma
        r_gp = Constantes.r
        T0 = Constantes.T0_K
        p0 = Constantes.p0_Pa

        # Delta pression compressible
        Delta_p = Atmosphere.getP_t() * (
            ((gamma - 1) / 2 * self.Mach_t**2 + 1) ** (gamma / (gamma - 1)) - 1
        )

        # CAS
        self.CAS_t = np.sqrt(
            2 * gamma * r_gp * T0 / (gamma - 1)
            * ((1 + Delta_p / p0) ** (0.4 / gamma) - 1)
        )
    

    def Convert_CAS_to_Mach(self, Atmosphere):
        gamma = Constantes.gamma
        r_gp = Constantes.r
        T0 = Constantes.T0_K
        p0 = Constantes.p0_Pa

        delta_p = p0 * (
            (1 + (gamma - 1) / 2 * self.CAS_t**2 / (gamma * r_gp * T0))**(gamma / (gamma - 1)) - 1
        )

        self.Mach_t = np.sqrt(
            2 / (gamma - 1)
            * ((1 + delta_p / Atmosphere.getP_t())**((gamma - 1) / gamma) - 1)
        )

    def Convert_TAS_to_Mach(self, Atmosphere):
        self.Mach_t = self.TAS_t / np.sqrt(Constantes.gamma * Constantes.r * Atmosphere.getT_t())

    def Convert_Mach_to_TAS(self, Atmosphere):
        self.TAS_t = self.Mach_t * np.sqrt(Constantes.gamma * Constantes.r * Atmosphere.getT_t())

    def Add_dl(self, dl):
        self.l += dl

    def Add_dh(self, dh):
        self.h += dh



#LISTE DES ATTRIBUTS :
# Name : Nom du modèle d'avion
# Manufacturer : Nom du constructeur
# Wingspan : Envergure de l'avion (m)
# Length : Longueur de l'avion (m)
# Height : Hauteur de l'avion (m)
# MaxTakeoffWeight : MTOW (kg)
# EmptyWeight : Masse à vide (kg)
# WingArea : Surface alaire (m^2)
# MaxPassengers : Nombre de passager 
# MaxFuelWeight : Masse carburant maximale (kg)
# MaxPLWeight : Masse Payload maximale (kg)
# Sref : Surface de référence (m^2)
# Phi25deg : Angle de twist ou angle de calage (°)
# TtoCref : Rapport entre l'épaisseur et la corde du profil ()
# Lref : Longueur de référence (m)
# AspectRatio : Allongement (Envergure^2/Surface alaire)
# TaperRatio : Taux de flèche, rapport corde en bout d'aile sur corde à l'emplenture ()
# Camber : Cambrure du profil ()
# MaxThicknessPosition : Position de l'épaisseur de profil maximale sur la corde ()
# DFuselage : Diamètre du fuselage (m)
# Envergure : Envergure de l'avion (m)
# KVMO : Vitesse maximale opérationnelle(kt)
# MMO : Mach maximal opérationnelle 
# PressurisationCeilingFt : Altitude maximale atteignable avec une cabine pressurisée (ft)
# Cx0Cruise : Cx0 en croisière () 
# Cx0Climb : Cx0 en montée ()
# Cx0Descent : Cx0 en descente ()
# OswaldClimb : Coefficient d'Oswald en montée ()
# OswaldCruise : Coefficient d'Oswald en croisière ()
# OswaldDescent : Coefficient d'Oswald en montée ()

    def __repr__(self):
        return f"<Avion: {getattr(self, 'Name', 'Unknown')}>"
    
    def getName(self):
        return self.Name
    
    def getManufacturer(self):
        return self.Manufacturer
    
    def getWingspan(self):
        return self.Wingspan

    def getLength(self):
        return self.Length

    def getHeight(self):
        return self.Height 
    
    def getMaxPassengers(self):
        return self.MaxPassengers
    
    def getMaxTakeoffWeight(self):
        return self.MaxTakeoffWeight
    
    def getEmptyWeight(self):
        return self.EmptyWeight
    
    def getMaxFuelWeight(self):
        return self.MaxFuelWeight
    
    def getMaxPLWeight(self):
        return self.MaxPLWeight
    
    def getWingAera(self):
        return self.WingAera
    
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
    
    def geth(self):
        return self.h_t
    
    def getl(self):
        return self.l_t
    
    def getMach(self):
        return self.Mach_t
    
    def getCAS(self):
        return self.CAS_t
    
    def getTAS(self):
        return self.TAS_t
    
   