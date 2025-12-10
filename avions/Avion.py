import os
import csv
from .aero import Aero
from .masse import Masse

class Avion:
    def __init__(self, nom_fichier_csv):

        # Dossier de ce fichier Avion.py
        base_dir = os.path.dirname(os.path.abspath(__file__)) #Renvoie le Directory du fichier actuel et remont d'un cran
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

        self.Aero = Aero(self)
        self.Masse = Masse(self)

    def __repr__(self):
        return f"<Avion: {getattr(self, 'Name', 'Unknown')}>"
