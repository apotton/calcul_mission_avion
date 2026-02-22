class PrintRedirector:
    def __init__(self, textbox):
        ''' Initialise la classe de redirection de la console. '''
        self.textbox = textbox
        self.log_filepath = None
        self.silent_mode = False

    def start_logging(self, filepath, silent=False):
        """ Démarre l'écriture dans un fichier. Si silent=True, n'écrit plus dans l'interface """
        self.log_filepath = filepath
        self.silent_mode = silent

    def stop_logging(self):
        """ Arrête l'écriture dans le fichier et restaure l'affichage normal """
        self.log_filepath = None
        self.silent_mode = False

    def write(self, texte):
        ''' Ecrit dans la console ou dans un fichier '''
        # Écriture dans l'interface si on n'est pas en mode silencieux
        if not self.silent_mode:
            self.textbox.insert("end", texte)
            self.textbox.see("end")
            self.textbox.update_idletasks()
        
        # Écriture dans le fichier de log si actif
        if self.log_filepath:
            try:
                with open(self.log_filepath, "a", encoding="utf-8") as f:
                    f.write(texte)
            except Exception:
                pass # Évite de faire crasher le code si le fichier est verrouillé

    def flush(self):
        pass