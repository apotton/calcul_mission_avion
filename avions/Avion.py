import os
import csv

class Avion:
    def __init__(self, nom_fichier_csv):

        # Dossier de ce fichier Avion.py
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Construire le chemin complet vers csv_avions
        csv_folder = os.path.join(base_dir, "avions", "csv_avions")
        full_path = os.path.join(csv_folder, nom_fichier_csv)

        # Si fichier non trouvé
        if not os.path.isfile(full_path):
            raise FileNotFoundError(f"Fichier CSV non trouvé : {full_path}")

        # Lecture CSV
        with open(full_path, mode='r', encoding='utf-8') as f:
            lecteur = csv.reader(f, delimiter=';')
            for ligne in lecteur:
                if len(ligne) == 2:
                    cle, valeur = ligne
                    # Conversion en float si possible
                    try:
                        valeur = float(valeur)
                    except ValueError:
                        pass

                    # Attribution dynamique des attributs
                    setattr(self, cle, valeur)

    def __repr__(self):
        return f"<Avion: {getattr(self, 'Name', 'Unknown')}>"
