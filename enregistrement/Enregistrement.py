from atmosphere.Atmosphere import Atmosphere
from constantes.Constantes import Constantes
from avions.Avion import Avion
import numpy as np
from itertools import zip_longest
import csv

class Enregistrement:
    def __init__(self):
        self.default_size = 10000  # Taille par défaut des tableaux numpy

        # Compteur (pour la taille à chaque changement)
        self.counter = 0

        self.data = {
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
            "F_N" : np.zeros(self.default_size, dtype=np.float32),
            "SFC" : np.zeros(self.default_size, dtype=np.float32),
            "FF" : np.zeros(self.default_size, dtype=np.float32),

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
            "ECCF": np.zeros(self.default_size, dtype = np.float32)
        }

        self.units = {
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
            "F_N" : "N",
            "SFC" : "kg/(N.s)",
            "FF"  : "kg/s",

            # Masse / carburant
            "FB" : "kg",
            "m"  : "kg",

            # Atmosphere
            "P" : "Pa",
            "T" : "K",
            "rho" : "kg/m³",

            # Paramètres économiques croisière
            "SGR" : "m/kg",
            "SAR" : "m/kg",
            "ECCF": "kg/m"
        }

        # Données de convergence simu
        self.data_simu = {
            # Précision
            "ecart_mission" : [],

            # Longueur descentes
            "l_descent" : [],
            "l_descent_diversion" : [],

            # Masse fuel mission
            "FB_mission" : []
        }

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
            "t_holding": 0.0
        }

    
    def save(self, Avion: Avion, Atmosphere: Atmosphere, dt):
        '''
        Enregistre toutes les variables dynamiques contenues dans les deux classes.
        
        :param Avion: Instance de la classe Avion
        :param Atmosphere: Instance de la classe Atmosphere
        :param dt: Pas de temps (s)
        '''
        self.data["t"][self.counter] = self.data["t"][self.counter - 1] + dt if self.counter > 1 else 0

        self.data["h"][self.counter] = Avion.geth()
        self.data["l"][self.counter] = Avion.getl()

        self.data["CAS"][self.counter] = Avion.Aero.getCAS()
        self.data["TAS"][self.counter] = Avion.Aero.getTAS()
        self.data["Mach"][self.counter] = Avion.Aero.getMach()

        self.data["Cz"][self.counter] = Avion.Aero.getCz()
        self.data["Cx"][self.counter] = Avion.Aero.getCx()
        self.data["finesse"][self.counter]  = Avion.Aero.getCz() / Avion.Aero.getCx()

        self.data["F_N"][self.counter] = Avion.Moteur.getF()
        self.data["SFC"][self.counter] = Avion.Moteur.getSFC()
        self.data["FF"][self.counter] = Avion.Moteur.getFF()

        self.data["FB"][self.counter] = Avion.Masse.getFuelBurned()
        self.data["m"][self.counter] = Avion.Masse.getCurrentMass()

        self.data["P"][self.counter] = Atmosphere.getP_t()
        self.data["T"][self.counter] = Atmosphere.getT_t()
        self.data["rho"][self.counter] = Atmosphere.getRho_t()


        if Avion.cruise:
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


    def saveSimu(self, Avion: Avion, ecart_mission):
        '''
        Enregistre les données de performance de la boucle (l'écart de précision,
        les longueurs de descente et la masse de fuel brulée pour la mission).
        
        :param Avion: Instance de la classe Avion
        :param ecart_mission: Ecart relatif sur le fuel burn mission (%)
        '''
        self.data_simu["ecart_mission"].append(ecart_mission)
        self.data_simu["l_descent"].append(Avion.get_l_descent())
        self.data_simu["FB_mission"].append(Avion.Masse.getFuelMission())
        self.data_simu["l_descent_diversion"].append(Avion.getl_descent_diversion())

    def saveFinal(self, Avion: Avion):
        '''
        Enregistre les valeurs finales des caractéristiques de la mission (masses, distances...)

        :param Avion: Instance de la classe avion
        '''
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

        valeurs_mises_en_forme = self.printValues()
        print(valeurs_mises_en_forme)
        
    def printValues(self):
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
        return "\n".join(lines)


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
            
            # 3. Extraction des données pour chaque colonne
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

            