from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path

def loadData(chemin_fichier):
    '''
    Charge un fichier de configuration moteur.
    
    :param chemin_fichier: Le chemin du fichier
    '''
    chemin_fichier = Path(chemin_fichier)

    # Check de l'existence du fichier
    if not chemin_fichier.exists():
        raise FileNotFoundError(f"{chemin_fichier} introuvable")

    spec = spec_from_file_location(
        name=chemin_fichier.stem,
        location=str(chemin_fichier)
    )

    # Check de la spec
    if spec is None:
        raise ValueError(f"Impossible de créer une spécification pour {chemin_fichier}")
    module = module_from_spec(spec)
    
    # Check du loader
    if spec.loader is None:
        raise ValueError(f"Impossible de créer un loader pour {chemin_fichier}")
    spec.loader.exec_module(module)

    return module.load()