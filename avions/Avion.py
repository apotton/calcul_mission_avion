import os
import csv

from moteurs.Moteur import Moteur
from .Aero import Aero
from .Masse import Masse

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
        self.Moteur = Moteur(6, 40, 1) # À initialiser plus tard avec un objet Moteur

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
    
   