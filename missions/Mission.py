import numpy as np
from atmosphere.Atmosphere import Atmosphere
from constantes.constantes import constantes

class CruiseSimulator:
    def __init__(self, avion, atm, moteur, dt=60):
        self.avion = avion
        self.atm = atm
        self.moteur = moteur
        self.dt = dt
        self.results = []

    def calculate_SGR(self, h_m, m_kg, mach, vw_mps):
        """Calcule le Specific Ground Range : distance sol par kg de fuel"""
        self.atm.getRhoPT(h_m)
        p, T = self.atm.getP_t(), self.atm.getT_t()
        tas = mach * np.sqrt(constantes.gamma * constantes.r * T)
        
        # Aéro
        cz = self.avion.Aero.calculate_cz(m_kg, p, mach) # Ajouté à la classe Aero
        self.avion.Aero.Cz_t = cz
        self.avion.Aero.CalculateCxCruise_Simplified()
        finesse = cz / self.avion.Aero.getCx()
        
        # Poussée et SFC
        thrust_req = (m_kg * constantes.g) / finesse
        fn_max = self.moteur.get_Fn_MCL(mach, h_m / constantes.conv_ft_m)
        sfc = self.moteur.get_SFC_MCL(mach, h_m / constantes.conv_ft_m)

        fuel_flow = sfc * thrust_req
        vx = tas + vw_mps
        return vx / fuel_flow, thrust_req, fn_max, tas

    def run(self, range_target_nm, h_initial_m, mach, vw_kt):
        vw_mps = vw_kt * constantes.conv_kt_mps
        h = h_initial_m
        dist_m = 0
        
        while dist_m < (range_target_nm * constantes.conv_NM_m):
            # 1. Performance actuelle
            sgr, thrust_req, fn_max, tas = self.calculate_SGR(h, self.avion.Masse.current_mass, mach, vw_mps)
            
            # 2. Check Step-Climb (2000 ft plus haut)
            h_up = h + (2000 * constantes.conv_ft_m)
            sgr_up, _, fn_max_up, _ = self.calculate_SGR(h_up, self.avion.Masse.current_mass, mach, vw_mps)
            
            # Logique de montée : SGR meilleur ET réserve de puissance suffisante
            # RRoC = (Fn - R) / mg * TAS
            rroc_up = (fn_max_up - thrust_req) / (self.avion.Masse.current_mass * constantes.g) * tas
            
            if sgr_up > sgr and rroc_up > (300 * constantes.conv_ft_m / 60): # 300 ft/min min
                h = h_up
                print(f"Step Climb vers FL{h/constantes.conv_ft_m/100:.0f}")
            # 3. Intégration temporelle
            dm = - (thrust_req * self.moteur.get_SFC_MCL(mach, h/constantes.conv_ft_m)) * self.dt
            dl = (tas + vw_mps) * self.dt
            
            self.avion.Masse.update_fuel(dm)
            dist_m += dl
            
            # Stockage résultats
            self.results.append({
                "dist_nm": dist_m / constantes.conv_NM_m,
                "alt_ft": h / constantes.conv_ft_m,
                "mass": self.avion.Masse.current_mass,
                "fuel": self.avion.Masse.fuel
            })