import numpy as np
from constantes.Constantes import Constantes
from atmosphere.Atmosphere import Atmosphere


def convert_Mach_to_CAS(Mach, press):##A VOIR SI QUI ON MET EN ENTREE GENRE LES CONSTANTES
    gamma = Constantes.gamma
    r_gp = Constantes.r
    T0 = Constantes.T0_K
    p0 = Constantes.p0_Pa

    # Delta pression compressible
    Delta_p = press * (
        ((gamma - 1) / 2 * Mach**2 + 1) ** (gamma / (gamma - 1)) - 1
    )

    # CAS
    CAS = np.sqrt(
        2 * gamma * r_gp * T0 / (gamma - 1)
        * ((1 + Delta_p / p0) ** (0.4 / gamma) - 1)
    )

    return CAS


def convert_mach_to_cas(Mach, press): ##A VOIR SI QUI ON MET EN ENTREE GENRE LES CONSTANTES
    gamma = Constantes.gamma
    r_gp = Constantes.r
    T0 = Constantes.T0_K
    p0 = Constantes.p0_Pa

    delta_p = press * ((1 + (gamma - 1) / 2 * Mach**2)**(gamma / (gamma - 1)) - 1)

    CAS = np.sqrt(
        2 * gamma * r_gp * T0 / (gamma - 1)
        * ((1 + delta_p / p0)**((gamma - 1) / gamma) - 1)
    )

    return CAS

