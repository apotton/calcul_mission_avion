from moteurs.CalculEmissions import getAllEmissions
from atmosphere.Atmosphere import Atmosphere
from constantes.Constantes import Constantes
from itertools import zip_longest
from avions.Avion import Avion

import numpy as np
import csv


class Enregistrement:
    def __init__(self):
        self.default_size = 10000  # Taille par défaut des tableaux numpy

        # Compteur (pour la taille à chaque changement)
        self.counter = 0

        # Données tabulaires à chaque pas de temps
        self.data = {
            # Phase de la mission
            "phase": np.zeros(self.default_size, dtype = np.float32),

            # Cinématique
            "t" : np.zeros(self.default_size, dtype=np.float32),
            "h" : np.zeros(self.default_size, dtype=np.float32),
            "l" : np.zeros(self.default_size, dtype=np.float32),

            # Vitesses
            "CAS" : np.zeros(self.default_size, dtype=np.float32),
            "TAS" : np.zeros(self.default_size, dtype=np.float32),
            "Mach" : np.zeros(self.default_size, dtype=np.float32),

            # Aérodynamique
            "Cz" : np.zeros(self.default_size, dtype=np.float32),
            "Cx" : np.zeros(self.default_size, dtype=np.float32),
            "finesse"  : np.zeros(self.default_size, dtype=np.float32),

            # Propulsion
            "F" : np.zeros(self.default_size, dtype=np.float32),
            "FF" : np.zeros(self.default_size, dtype=np.float32),
            "SFC" : np.zeros(self.default_size, dtype=np.float32),

            # Masse / carburant
            "FB" : np.zeros(self.default_size, dtype=np.float32),
            "m" : np.zeros(self.default_size, dtype=np.float32),

            # Atmosphere
            "P" : np.zeros(self.default_size, dtype=np.float32),
            "T" : np.zeros(self.default_size, dtype=np.float32),
            "rho" : np.zeros(self.default_size, dtype=np.float32),

            # Paramètres économiques croisière
            "SGR" : np.zeros(self.default_size, dtype = np.float32),
            "SAR" : np.zeros(self.default_size, dtype = np.float32),
            "ECCF": np.zeros(self.default_size, dtype = np.float32),

            # Emissions polluantes
            "eHC"  : np.zeros(self.default_size, dtype = np.float32),
            "eCO"  : np.zeros(self.default_size, dtype = np.float32),
            "eNOx" : np.zeros(self.default_size, dtype = np.float32),
            "envPM": np.zeros(self.default_size, dtype = np.float32),
        }

        # Unités des données tabulaires
        self.units = {
            # Phase de la mission
            "phase" : "-",

            # Cinématique
            "t" : "s",
            "h" : "m",
            "l" : "m",

            # Vitesses
            "CAS"  : "m/s",
            "TAS"  : "m/s",
            "Mach" : "-",

            # Aérodynamique
            "Cz"       : "-",
            "Cx"       : "-",
            "finesse"  : "-",

            # Propulsion
            "F" : "N",
            "FF"  : "kg/s",
            "SFC" : "kg/(N.s)",

            # Masse / carburant
            "FB" : "kg",
            "m"  : "kg",

            # Atmosphere
            "P" : "Pa",
            "T" : "K",
            "rho" : "kg/m^3",

            # Paramètres économiques croisière
            "SGR" : "m/kg",
            "SAR" : "m/kg",
            "ECCF": "kg/m",

            # Emissions polluantes
            "eHC"  : "kg/s",
            "eCO"  : "kg/s",
            "eNOx" : "kg/s",
            "envPM": "kg/s",
        }

        # Données de convergence simu
        self.data_simu = {
            # Précision
            "precision" : [],

            # Longueur descentes
            "l_descent" : [],
            "l_descent_diversion" : [],

            # Masse fuel mission
            "FB_mission" : []
        }

        # Données ponctuelles à remplir en fin de mission
        self.mission_data = {
            # Fuel burn
            "FB_mission": 0.0,
            "FB_climb": 0.0,
            "FB_cruise": 0.0,
            "FB_descent": 0.0,
            "FB_reserve": 0.0,
            "FB_diversion": 0.0,
            "FB_holding": 0.0,
            "mF_contingency": 0.0,
            # Distances
            "l_climb": 0.0,
            "l_cruise": 0.0,
            "l_descent": 0.0,
            "l_diversion": 0.0,
            "l_holding": 0.0,
            # Temps
            "t_climb": 0.0,
            "t_cruise": 0.0,
            "t_descent": 0.0,
            "t_diversion": 0.0,
            "t_holding": 0.0,
            ## Emissions
            # Montée
            "eHC_climb": 0.0,
            "eCO_climb": 0.0,
            "eNOx_climb": 0.0,
            "envPM_climb": 0.0,
            # Croisière
            "eHC_cruise": 0.0,
            "eCO_cruise": 0.0,
            "eNOx_cruise": 0.0,
            "envPM_cruise": 0.0,
            # Descente
            "eHC_descent": 0.0,
            "eCO_descent": 0.0,
            "eNOx_descent": 0.0,
            "envPM_descent": 0.0,
            # Diversion
            "eHC_diversion": 0.0,
            "eCO_diversion": 0.0,
            "eNOx_diversion": 0.0,
            "envPM_diversion": 0.0,
            # Holding
            "eHC_holding": 0.0,
            "eCO_holding": 0.0,
            "eNOx_holding": 0.0,
            "envPM_holding": 0.0,
        }

        # Données discontinues entre deux phases (essentiellement moteur)
        self.discontinuous_data = ["F", "FF", "SFC", "SGR", "SAR", "ECCF"]

    
    def save(self, Avion: Avion, Atmosphere: Atmosphere, dt):
        '''
        Enregistre toutes les variables dynamiques contenues dans les deux classes.
        
        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param dt: Pas de temps (s)
        '''
        # Gestion de la discontinuité des valeurs en changement de phase
        if self.counter > 0:
            if self.data["phase"][self.counter - 1] != Avion.getPhase():
                # La plupart des variables sont continues
                for key in self.data:
                    self.data[key][self.counter] = self.data[key][self.counter-1]

                # Celles-là ne le sont pas
                self.data["phase"][self.counter] = Avion.getPhase()
                self.data["F"][self.counter] = Avion.Moteur.getF()
                self.data["FF"][self.counter] = Avion.Moteur.getFF()
                self.data["SFC"][self.counter] = Avion.Moteur.getSFC()

                if Avion.getPhase() == 1:
                    self.data["SAR"][self.counter] = Avion.Aero.getSAR()
                    self.data["SGR"][self.counter] = Avion.Aero.getSGR()
                    self.data["ECCF"][self.counter] = Avion.Aero.getECCF()

                self.counter += 1


        self.data["t"][self.counter] = self.data["t"][self.counter - 1] + dt if self.counter > 1 else 0

        self.data["h"][self.counter] = Avion.get_h()
        self.data["l"][self.counter] = Avion.get_l()

        self.data["CAS"][self.counter] = Avion.Aero.getCAS()
        self.data["TAS"][self.counter] = Avion.Aero.getTAS()
        self.data["Mach"][self.counter] = Avion.Aero.getMach()

        self.data["Cz"][self.counter] = Avion.Aero.getCz()
        self.data["Cx"][self.counter] = Avion.Aero.getCx()
        self.data["finesse"][self.counter]  = Avion.Aero.getCz() / Avion.Aero.getCx()

        self.data["F"][self.counter] = Avion.Moteur.getF()
        self.data["FF"][self.counter] = Avion.Moteur.getFF()
        self.data["SFC"][self.counter] = Avion.Moteur.getSFC()

        self.data["FB"][self.counter] = Avion.Masse.getFuelBurned()
        self.data["m"][self.counter] = Avion.Masse.getCurrentMass()

        self.data["P"][self.counter] = Atmosphere.getP()
        self.data["T"][self.counter] = Atmosphere.getT()
        self.data["rho"][self.counter] = Atmosphere.getRho()

        self.data["phase"][self.counter] = Avion.getPhase()

        # On ne calcule les paramètres économiques qu'en croisière
        if (Avion.getPhase() == 1):
            self.data["SGR"][self.counter] = Avion.Aero.getSGR()
            self.data["SAR"][self.counter] = Avion.Aero.getSAR()
            self.data["ECCF"][self.counter] = Avion.Aero.getECCF()
        else :
            self.data["SGR"][self.counter] = float('nan')
            self.data["SAR"][self.counter] = float('nan')
            self.data["ECCF"][self.counter] = float('nan')

        self.counter += 1
        
        if self.counter >= len(self.data["t"]):
            self.extend()


    def saveSimu(self, Avion: Avion, precision):
        '''
        Enregistre les données de performance de la boucle (l'écart de précision,
        les longueurs de descente et la masse de fuel brulée pour la mission).
        
        :param Avion: Instance de la classe Avion
        :param precision: Précision relative atteinte (%)
        '''
        self.data_simu["precision"].append(precision)
        self.data_simu["l_descent"].append(Avion.get_l_descent())
        self.data_simu["FB_mission"].append(Avion.Masse.getFuelMission())
        self.data_simu["l_descent_diversion"].append(Avion.get_l_descent_diversion())

    def saveFinal(self, Avion: Avion, Atmosphere: Atmosphere):
        '''
        Enregistre et affiche les valeurs finales des caractéristiques de la mission 
        (masses, distances, temps, émissions...);

        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        '''
        # On coupe les arrays
        self.cut()
        
        # Masses mission
        self.mission_data["FB_mission"] = Avion.Masse.getFuelMission()
        self.mission_data["FB_climb"] = Avion.Masse.getFuelClimb()
        self.mission_data["FB_cruise"] = Avion.Masse.getFuelCruise()
        self.mission_data["FB_descent"] = Avion.Masse.getFuelDescent()

        # Masses réserve
        self.mission_data["FB_reserve"] = Avion.Masse.getFuelReserve()
        self.mission_data["FB_diversion"] = Avion.Masse.getFuelDiversion()
        self.mission_data["FB_holding"] = Avion.Masse.getFuelHolding()
        self.mission_data["mF_contingency"] = Avion.Masse.getFuelContingency()

        # Distances mission
        self.mission_data["l_climb"] = Avion.get_l_climb()
        self.mission_data["l_cruise"] = Avion.get_l_cruise()
        self.mission_data["l_descent"] = Avion.get_l_descent()
        self.mission_data["l_diversion"] = Avion.get_l_diversion()
        self.mission_data["l_holding"] = Avion.get_l_holding()

        # Temps mission
        self.mission_data["t_climb"] = Avion.get_t_climb()
        self.mission_data["t_cruise"] = Avion.get_t_cruise()
        self.mission_data["t_descent"] = Avion.get_t_descent()
        self.mission_data["t_diversion"] = Avion.get_t_diversion()
        self.mission_data["t_holding"] = Avion.get_t_holding()

        # Emissions
        getAllEmissions(Avion, Atmosphere, self)
        
        # Affichage des valeurs dans la console de manière formatée
        self.printValues()
        self.printEmissions()

        # Contrails
        # Atmosphere.determineContrails(self)
        
    def printValues(self):
        '''
        Affiche de manière formatée dans la console les temps, distances et fuel burns pour
        toutes les phases de la mission.
        '''
        # Dictionnaire des grandeurs à afficher
        phases = [
            ("Montée", 
            self.mission_data["l_climb"], 
            self.mission_data["t_climb"], 
            self.mission_data["FB_climb"]),

            ("Croisière", 
            self.mission_data["l_cruise"], 
            self.mission_data["t_cruise"], 
            self.mission_data["FB_cruise"]),

            ("Descente", 
            self.mission_data["l_descent"], 
            self.mission_data["t_descent"], 
            self.mission_data["FB_descent"]),

            ("Mission", 
            self.mission_data["l_climb"] + self.mission_data["l_cruise"] + self.mission_data["l_descent"], 
            self.mission_data["t_climb"] + self.mission_data["t_cruise"] + self.mission_data["t_descent"], 
            self.mission_data["FB_mission"]),

            ("Diversion", 
            self.mission_data["l_diversion"],
            self.mission_data["t_diversion"], 
            self.mission_data["FB_diversion"]),

            ("Holding", 
            self.mission_data["l_holding"],
            self.mission_data["t_holding"], 
            self.mission_data["FB_holding"]),

            ("Contingence", 
            "-",
            "-", 
            self.mission_data["mF_contingency"]),

            ("Reserves",
             self.mission_data["l_diversion"] + self.mission_data["l_holding"],
             self.mission_data["t_diversion"] + self.mission_data["t_holding"],
             self.mission_data["FB_diversion"] + self.mission_data["FB_holding"] + self.mission_data["mF_contingency"]
             )
        ]

        total_distance = 0.0
        total_time = 0.0
        total_fuel = 0.0

        lines = []
        header = f"{'Phase':<12}{'Distance (NM)':>15}{'Temps (min)':>15}{'Fuel Burn (kg)':>18}"
        separator = "-" * len(header)

        lines.append(separator)
        lines.append("                   RÉSUMÉ DE LA MISSION")
        lines.append(separator)

        lines.append(header)
        lines.append(separator)

        # Itération sur toutes les phases pour arriver au total
        for name, dist_m, time_s, fuel in phases:
            # Pour le total de la mission, on met un séparateur
            if name == "Mission" or name == "Reserves":
                lines.append(separator)

            # Le contingency fuel ne compte pas comme un vol, on passe à la suite
            if name == "Contingence":
                total_fuel += fuel
                lines.append(
                    f"{'Contingence':<12}{'-':>15}{'-':>15}{fuel:>18.1f}"
                )
                continue
            else:
                dist_nm = dist_m / Constantes.conv_NM_m
                time_min = time_s / 60.
                lines.append(
                    f"{name:<12}{dist_nm:>15.1f}{time_min:>15.1f}{fuel:>18.1f}"
                )

            # On remet un séparateur pour la mission et on ne compte pas sa distance parcourue
            if name == "Mission" or name == "Reserves":
                lines.append(separator)
            else:
                total_distance += dist_nm
                total_time += time_min
                total_fuel += fuel

        lines.append(
            f"{'TOTAL':<12}{total_distance:>15.1f}{total_time:>15.1f}{total_fuel:>18.1f}"
        )

        # On renvoie la string formatée
        lines.append("")
        print("\n".join(lines))

    def printEmissions(self):
        '''
        Affiche de manière mise en forme dans la console le bilan des émissions de 
        l'avion pendant les principales phases de vol.
        '''
        coeff = 3.159 / 1000 # tonne de CO2 brulé par kg de carburant

        # Dictionnaire des grandeurs à afficher
        phases = [
            ("Montée", 
            self.mission_data["FB_climb"] * coeff,
            self.mission_data["eHC_climb"], 
            self.mission_data["eCO_climb"], 
            self.mission_data["eNOx_climb"],
            self.mission_data["envPM_climb"]),

            ("Croisière", 
            self.mission_data["FB_cruise"] * coeff,
            self.mission_data["eHC_cruise"], 
            self.mission_data["eCO_cruise"], 
            self.mission_data["eNOx_cruise"],
            self.mission_data["envPM_cruise"]),

            ("Descente", 
            self.mission_data["FB_descent"] * coeff,
            self.mission_data["eHC_descent"], 
            self.mission_data["eCO_descent"], 
            self.mission_data["eNOx_descent"],
            self.mission_data["envPM_descent"]),

            ("Mission", 
            (self.mission_data["FB_climb"] + self.mission_data["FB_cruise"] + self.mission_data["FB_descent"]) * coeff,
            self.mission_data["eHC_climb"] + self.mission_data["eHC_cruise"] + self.mission_data["eHC_descent"], 
            self.mission_data["eCO_climb"] + self.mission_data["eCO_cruise"] + self.mission_data["eCO_descent"], 
            self.mission_data["eNOx_climb"] + self.mission_data["eNOx_cruise"] + self.mission_data["eNOx_descent"], 
            self.mission_data["envPM_climb"] + self.mission_data["envPM_cruise"] + self.mission_data["envPM_descent"]),

            ("Diversion", 
            self.mission_data["FB_diversion"] * coeff,
            self.mission_data["eHC_diversion"],
            self.mission_data["eCO_diversion"], 
            self.mission_data["eNOx_diversion"],
            self.mission_data["envPM_diversion"]),

            ("Holding", 
            self.mission_data["FB_holding"] * coeff,
            self.mission_data["eHC_holding"],
            self.mission_data["eCO_holding"], 
            self.mission_data["eNOx_holding"],
            self.mission_data["envPM_holding"]),

            ("Reserves",
            (self.mission_data["FB_diversion"] + self.mission_data["FB_holding"]) * coeff,
             self.mission_data["eHC_diversion"] + self.mission_data["eHC_holding"],
             self.mission_data["eCO_diversion"] + self.mission_data["eCO_holding"],
             self.mission_data["eNOx_diversion"] + self.mission_data["eNOx_holding"],
             self.mission_data["envPM_diversion"] + self.mission_data["envPM_holding"])
        ]
        
        totalCO2 = 0.0
        totalHC = 0.0
        totalCO = 0.0
        totalNOx = 0.0
        totalnvPM = 0.0

        lines = []
        header = f"{'Phase':<12}{'CO₂ (t)':>10}{'HC (kg)':>10}{'CO (kg)':>10}{'NOx (kg)':>10}{'nvPM (g)':>10}"
        separator = "-" * len(header)

        lines.append(separator)
        lines.append("                     RÉSUMÉ DES ÉMISSIONS")
        lines.append(separator)

        lines.append(header)
        lines.append(separator)

        # Itération sur toutes les phases pour arriver au total
        for name, CO2, HC, CO, NOx, nvPM in phases:
            # Pour le total de la mission, on met un séparateur
            if name == "Mission" or name == "Reserves":
                lines.append(separator)


            lines.append(
                f"{name:<12}{CO2:>10.1f}{HC:>10.1f}{CO:>10.1f}{NOx:>10.1f}{nvPM*1000:>10.1f}"
            )

            # On remet un séparateur pour la mission et on ne compte pas sa distance parcourue
            if name == "Mission" or name == "Reserves":
                lines.append(separator)
            else:
                totalCO2 += CO2
                totalHC += HC
                totalCO += CO
                totalNOx += NOx
                totalnvPM += nvPM

        lines.append(
            f"{'TOTAL':<12}{totalCO2:>10.1f}{totalHC:>10.1f}{totalCO:>10.1f}{totalNOx:>10.1f}{totalnvPM*1000:>10.1f}"
        )

        # On renvoie la string formatée
        print("\n".join(lines))

    def extend(self):
        '''
        Rajoute des 0 à la fin des tableaux pré-alloués si ceux-ci sont remplis.
        '''
        for key in self.data:
            self.data[key] = np.concatenate([
                self.data[key],
                np.zeros(self.default_size, dtype=np.float32)
            ])

    def cut(self):
        '''
        Enlève toutes les valeurs non atteintes après le counter.
        '''
        for key in self.data:
            self.data[key] = self.data[key][:self.counter]

    def reset(self):
        '''
        Remet tous les tableaux à zéro.
        '''
        self.counter = 0
        for key in self.data:
            self.data[key] = np.zeros(self.default_size, dtype=np.float32)

    def exportCSV(self, filepath):
        '''
        Exporte les données enregistrées sous forme de fichier CSV en colonnes.
        Format : 
        NomVariable1;NomVariable2;...
        Unite1;Unite2;...
        Valeur1_1;Valeur2_1;...
        
        :param filepath: Chemin complet du fichier de destination
        '''
        with open(filepath, "w", encoding="utf-8", newline='') as f:
            writer = csv.writer(f, delimiter=';')
            
            # Extraction des clés (noms des variables)
            noms_variables = list(self.data.keys())
            
            # Gestion des unités
            ligne_unites = [self.units.get(clef, "") for clef in noms_variables]
            
            # Écriture de la ligne des en-têtes, puis de la ligne des unités
            writer.writerow(noms_variables)
            writer.writerow(ligne_unites)
            
            # Extraction des données pour chaque colonne
            colonnes_donnees = [
                ["" if np.isnan(val) else val for val in self.data[clef].tolist()] 
                for clef in noms_variables
            ]
            
            # Transposition (colonnes -> lignes) et écriture
            # zip_longest permet de regrouper le 1er élément de chaque liste, puis le 2ème, etc.
            # fillvalue='' permet de combler les trous si les listes n'ont pas exactement la même taille.
            lignes_transposees = zip_longest(*colonnes_donnees, fillvalue='')
            
            # Écriture de toutes les lignes de données d'un seul coup
            writer.writerows(lignes_transposees)

    def loadCSV(self, chemin_csv):
        '''
        Remplit l'attribut enregistrement de la classe avec les données issues du CSV.

        :param chemin_csv: Chemin complet du fichier resultats_vol.csv
        '''
        self.reset()
        
        with open(chemin_csv, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=';')
            
            # On charge toutes les lignes en mémoire
            lignes = list(reader)
            
            if len(lignes) >= 2:
                # Extraction des en-têtes (clés) et des unités
                noms_variables = lignes[0]
                donnees_lignes = lignes[2:] # Tout le reste correspond aux données
                
                if donnees_lignes:
                    # Transposition : on bascule les lignes en colonnes
                    # zip(*donnees_lignes) prend toutes les lignes et regroupe les éléments par colonne
                    colonnes = list(zip(*donnees_lignes))
                    
                    # Traitement colonne par colonne
                    for i, key in enumerate(noms_variables):
                        if key in self.data:
                            # On récupère la colonne brute (une liste de chaînes de caractères)
                            colonne_brute = colonnes[i]
                            
                            # Conversion : on remplace "" par np.nan, puis on convertit en float32
                            vals = np.array(
                                [np.nan if val == "" else val for val in colonne_brute], 
                                dtype=np.float32
                            )
                            
                            l = len(vals)
                            self.data[key][:l] = vals
                            self.counter = max(self.counter, l)