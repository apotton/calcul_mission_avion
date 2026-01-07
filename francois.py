# code qui crée une fonction d'estimation du fuel à emporter pour un vol donné selon l'équation de Breguet Leduc

def estimation_fuel(distance_km, consommation_kg_per_km, poids_initial_kg, poids_final_kg):
    """
    Estime la quantité de fuel nécessaire pour un vol donné en utilisant l'équation de Breguet Leduc.

    :param distance_km: Distance du vol en kilomètres
    :param consommation_kg_per_km: Consommation de fuel par kilomètre en kilogrammes
    :param poids_initial_kg: Poids initial de l'avion (avec fuel) en kilogrammes
    :param poids_final_kg: Poids final de l'avion (sans fuel) en kilogrammes
    :return: Quantité de fuel nécessaire en kilogrammes
    """
    # Calculer le ratio de poids
    ratio_poids = poids_initial_kg / poids_final_kg
    
    # Calculer la quantité de fuel nécessaire selon l'équation de Breguet Leduc
    fuel_necessaire_kg = consommation_kg_per_km * distance_km * (ratio_poids - 1)
    
    return fuel_necessaire_kg