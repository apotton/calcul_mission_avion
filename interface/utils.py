import re

# Regex pour détecter les codes ANSI (ex: \033[31m, \033[0m, \033[1;32m)
ANSI_PATTERN = re.compile(r'(\033\[[\d;]*m)')

class PrintRedirector:
    def __init__(self, textbox):
        self.textbox = textbox
        self.log_filepath = None
        self.silent_mode = False
        self.current_color_tag = None
        
        # Configuration des couleurs ANSI (Tu peux ajuster les codes hexadécimaux)
        self.colors = {
            '30': 'black',
            '31': '#E74C3C', # Rouge (Erreurs)
            '32': '#2ECC71', # Vert (Succès)
            '33': '#F1C40F', # Jaune (Avertissements)
            '34': '#3498DB', # Bleu (Infos)
            '35': '#9B59B6', # Magenta
            '36': '#1ABC9C', # Cyan
            '37': 'white',   # Blanc
            '90': 'gray',    # Gris foncé
        }
        
        # Création des tags dans la textbox de CustomTkinter
        for code, color in self.colors.items():
            self.textbox.tag_config(f"color_{code}", foreground=color)

    def start_logging(self, filepath, silent=False):
        """ Démarre l'écriture dans un fichier. Si silent=True, n'écrit plus dans l'interface """
        self.log_filepath = filepath
        self.silent_mode = silent

    def stop_logging(self):
        """ Arrête l'écriture dans le fichier et restaure l'affichage normal """
        self.log_filepath = None
        self.silent_mode = False

    def write(self, texte):
        # 1. Nettoyage du texte pour le fichier (on supprime tous les codes ANSI)
        clean_text = re.sub(r'\033\[[\d;]*m', '', texte)
        
        # 2. Écriture dans le fichier de log si actif
        if self.log_filepath:
            try:
                with open(self.log_filepath, "a", encoding="utf-8") as f:
                    f.write(clean_text)
            except Exception:
                pass

        # 3. Écriture dans l'interface avec interprétation des couleurs
        if not self.silent_mode:
            # On découpe la string en gardant les codes ANSI comme éléments de la liste
            parts = ANSI_PATTERN.split(texte)
            
            for part in parts:
                if part.startswith('\033['):
                    # C'est un code de couleur ANSI
                    code_interieur = part[2:-1] # On extrait ce qu'il y a entre \033[ et m
                    
                    if code_interieur == '0' or code_interieur == '':
                        # Reset de la couleur (\033[0m)
                        self.current_color_tag = None
                    else:
                        # Gestion des codes composés (ex: 1;31 pour gras et rouge)
                        codes = code_interieur.split(';')
                        for c in codes:
                            if c in self.colors:
                                self.current_color_tag = f"color_{c}"
                
                elif part: # Si la partie n'est pas vide, c'est du texte à afficher
                    if self.current_color_tag:
                        self.textbox.insert("end", part, self.current_color_tag)
                    else:
                        self.textbox.insert("end", part)
                        
            self.textbox.see("end")
            self.textbox.update_idletasks()

    def flush(self):
        # Nécessaire pour simuler complètement sys.stdout
        pass