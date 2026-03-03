import numpy as np
from scipy.interpolate import interp1d
from atmosphere.Atmosphere import Atmosphere
from avions.Avion import Avion

def calculateFFf(FF, Tamb, Pamb, Mach):
    """
    Calcule le Fuel Flow équivalent au niveau de la mer (Wff) selon la méthode BFFM2.
    
    :param FF: Array NumPy des débits de carburant réels en vol (kg/s)
    :param Tamb: Array NumPy des températures ambiantes statiques (Kelvin)
    :param Pamb: Array NumPy des pressions ambiantes statiques (Pascals)
    :param Mach: Array NumPy des nombres de Mach
    
    :return FFf: Array NumPy des débits de carburant équivalents SLS (kg/s)
    """
    
    # Constantes de l'atmosphère standard au niveau de la mer (ISA)
    T_SLS = 273.15  # Kelvin
    P_SLS = 101325.0  # Pascals
    
    # Calcul des ratios thermodynamiques
    theta_amb = Tamb / T_SLS
    delta_amb = Pamb / P_SLS
    
    # Calcul vectorisé du Wff (Application de l'équation BFFM2)
    return FF * ( (theta_amb**3.8) / delta_amb ) * np.exp(0.2 * Mach**2)


def get_interpolated_EI(FFf_array, FF_ref, EI_ref):
    """
    Fonction vectorisée pour interpoler les indices d'émission (EI) 
    en échelle log-log, avec gestion des zéros et extrapolation.
    
    :param FFf_array Array NumPy des Fuel Flows équivalents (sol) de la mission (kg/s)
    :param FF_ref: Liste ou array des 4 Fuel Flows de référence (sol) ICAO (kg/s)
    :param EI_ref: Liste ou array des 4 EI de référence (sol) ICAO correspondants (g/kg)
    :return EI_out: Les émissions interpolées pour la poussée au sol FFf_array (g/kg)
    """
    
    # Conversion en arrays NumPy pour la vectorisation
    Wff = np.asarray(FFf_array)
    FF_ref = np.asarray(FF_ref)
    EI = np.asarray(EI_ref)
    
    # Gestion du piège log(0) pour les HC et CO
    # On remplace les valeurs <= 0 par une valeur infinitésimale (ex: 1e-5)
    # Cela permet au logarithme de fonctionner sans fausser le bilan de masse final.
    EI_safe = np.where(EI <= 0, 1e-5, EI)
    
    # Passage en espace logarithmique
    log_Wf_ref = np.log(FF_ref)
    log_EI_ref = np.log(EI_safe)
    log_Wff = np.log(Wff)
    
    # Création de la fonction d'interpolation/extrapolation
    # 'fill_value="extrapolate"' dit à SciPy de continuer la pente log-log 
    # si le Wff de la mission est inférieur au ralenti ou supérieur au décollage.
    interp_func = interp1d(log_Wf_ref, log_EI_ref, kind='linear', fill_value='extrapolate') # type: ignore
    
    # Calcul vectoriel sur toute la mission et retour en exponentielle
    log_EI_out = interp_func(log_Wff)
    EI_out = np.exp(log_EI_out)
    
    # Optionnel : Si l'EI calculé est très proche de zéro (suite à notre 1e-5), on le force à 0
    EI_out = np.where(EI_out < 1e-4, 0.0, EI_out)
    
    return np.array(EI_out, dtype=np.float32)


def correct_EI_for_flight(EI_HC_ref, EI_CO_ref, EI_NOx_ref, Tamb, Pamb, humidity=0.0):
    """
    Applique les corrections d'altitude de la méthode BFFM2 aux indices d'émission.
    
    :param EI_HC_ref: Array des EI HC interpolés au sol (g/kg)
    :param EI_CO_ref: Array des EI CO interpolés au sol (g/kg)
    :param EI_NOx_ref: Arrays des EI NOx interpolés au sol (g/kg)
    :param Tamb: Array des températures ambiantes (Kelvin)
    :param Pamb: Array des pressions ambiantes (Pascals)
    :param humidity: Array de l'humidité spécifique (kg eau / kg air sec).
                 
    :return: Les indices d'émission réels en vol (g/kg)
    """
    
    T_SLS = 273.15
    P_SLS = 101325.0
    
    # Ratios thermodynamiques
    theta = np.asarray(Tamb) / T_SLS
    delta = np.asarray(Pamb) / P_SLS
    
    # Facteur de correction de base (commun à tous les polluants)
    # On calcule (theta^3.3 / delta^1.02) une seule fois pour optimiser
    thermo_factor = (theta**3.3) / (delta**1.02)
    
    # Application aux HC et CO
    EI_HC = EI_HC_ref * thermo_factor
    EI_CO = EI_CO_ref * thermo_factor
    
    # Calcul du facteur d'humidité pour les NOx
    H = -19.0 * (humidity - 0.00634)
    
    # Application aux NOx (inverse de la racine du thermo_factor * humidité)
    EI_NOx = EI_NOx_ref * (1.0 / np.sqrt(thermo_factor)) * np.exp(H)
    
    return EI_HC, EI_CO, EI_NOx

def getAllEmissions(Avion: Avion, Atmosphere: Atmosphere, Enregistrement):
    '''
    Calcule les émissions instantannées (kg/s) et totales (kg) de différents
    polluants: HC, CO, NOx et nvPM.

    :param Avion: Instance de la classe Avion
    :param Atmosphere: Instance de la classe Atmosphere
    :param Enregistrement: Instance de la classe Enregistrement    
    '''
    # Calcul de l'humidité relative
    w = Atmosphere.calculateHumidity(Enregistrement)

    # Recalage Fuel Flow au sol (méthode BFFM2)
    FFf = calculateFFf(Enregistrement.data["FF"],
                       Enregistrement.data["T"], 
                       Enregistrement.data["P"],
                       Enregistrement.data["Mach"])
    
    # Interpolation au sol des émissions (pas d'autres interpolations pour nvPM)
    EI_HC_sol = get_interpolated_EI(FFf, Avion.Moteur.getfuel_flow_ref(), Avion.Moteur.getEI_HC_ref())
    EI_CO_sol = get_interpolated_EI(FFf, Avion.Moteur.getfuel_flow_ref(), Avion.Moteur.getEI_CO_ref())
    EI_Nox_sol = get_interpolated_EI(FFf, Avion.Moteur.getfuel_flow_ref(), Avion.Moteur.getEI_NOx_ref())
    EI_nvPM_vol = get_interpolated_EI(FFf, Avion.Moteur.getfuel_flow_ref(), Avion.Moteur.getEI_nvPM_Mass())

    # Calcul des émissions en vol, en g/kg
    EI_HC_vol, EI_CO_vol, EI_Nox_vol = correct_EI_for_flight(EI_HC_sol, EI_CO_sol, EI_Nox_sol,
                                                             Enregistrement.data["T"],
                                                             Enregistrement.data["P"],
                                                             humidity=w)
    
    # Calcul des émissions instantannées (kg/s)
    FF = Enregistrement.data["FF"]
    Enregistrement.data["eHC"] = FF * EI_HC_vol / 1000
    Enregistrement.data["eCO"] = FF * EI_CO_vol / 1000
    Enregistrement.data["eNOx"] = FF * EI_Nox_vol / 1000
    Enregistrement.data["envPM"] = FF * EI_nvPM_vol / 1000

    # Calcul (intégration) des émissions totales
    phase = Enregistrement.data["phase"]
    t = Enregistrement.data["t"]

    # Montée
    mask_climb = (phase == 0)
    Enregistrement.mission_data["eHC_climb"] = np.trapezoid(Enregistrement.data["eHC"][mask_climb], t[mask_climb])
    Enregistrement.mission_data["eCO_climb"] = np.trapezoid(Enregistrement.data["eCO"][mask_climb], t[mask_climb])
    print(f"CO montée: {Enregistrement.mission_data["eCO_climb"]}")
    Enregistrement.mission_data["eNOx_climb"] = np.trapezoid(Enregistrement.data["eNOx"][mask_climb], t[mask_climb])
    Enregistrement.mission_data["envPM_climb"] = np.trapezoid(Enregistrement.data["envPM"][mask_climb], t[mask_climb])

    # Croisière
    mask_cruise = (phase == 1)
    Enregistrement.mission_data["eHC_cruise"] = np.trapezoid(Enregistrement.data["eHC"][mask_cruise], t[mask_cruise])
    Enregistrement.mission_data["eCO_cruise"] = np.trapezoid(Enregistrement.data["eCO"][mask_cruise], t[mask_cruise])
    print(f"CO cruise: {Enregistrement.mission_data["eCO_cruise"]}")
    Enregistrement.mission_data["eNOx_cruise"] = np.trapezoid(Enregistrement.data["eNOx"][mask_cruise], t[mask_cruise])
    Enregistrement.mission_data["envPM_cruise"] = np.trapezoid(Enregistrement.data["envPM"][mask_cruise], t[mask_cruise])

    # Descente
    mask_descent = (phase == 2)
    Enregistrement.mission_data["eHC_descent"] = np.trapezoid(Enregistrement.data["eHC"][mask_descent], t[mask_descent])
    Enregistrement.mission_data["eCO_descent"] = np.trapezoid(Enregistrement.data["eCO"][mask_descent], t[mask_descent])
    Enregistrement.mission_data["eNOx_descent"] = np.trapezoid(Enregistrement.data["eNOx"][mask_descent], t[mask_descent])
    Enregistrement.mission_data["envPM_descent"] = np.trapezoid(Enregistrement.data["envPM"][mask_descent], t[mask_descent])

    # Diversion
    mask_diversion = (phase == 3)
    Enregistrement.mission_data["eHC_diversion"] = np.trapezoid(Enregistrement.data["eHC"][mask_diversion], t[mask_diversion])
    Enregistrement.mission_data["eCO_diversion"] = np.trapezoid(Enregistrement.data["eCO"][mask_diversion], t[mask_diversion])
    Enregistrement.mission_data["eNOx_diversion"] = np.trapezoid(Enregistrement.data["eNOx"][mask_diversion], t[mask_diversion])
    Enregistrement.mission_data["envPM_diversion"] = np.trapezoid(Enregistrement.data["envPM"][mask_diversion], t[mask_diversion])

    # Holding
    mask_holding = (phase == 4)
    Enregistrement.mission_data["eHC_holding"] = np.trapezoid(Enregistrement.data["eHC"][mask_holding], t[mask_holding])
    Enregistrement.mission_data["eCO_holding"] = np.trapezoid(Enregistrement.data["eCO"][mask_holding], t[mask_holding])
    Enregistrement.mission_data["eNOx_holding"] = np.trapezoid(Enregistrement.data["eNOx"][mask_holding], t[mask_holding])
    Enregistrement.mission_data["envPM_holding"] = np.trapezoid(Enregistrement.data["envPM"][mask_holding], t[mask_holding])

