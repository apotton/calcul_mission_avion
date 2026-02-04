class Enregistrement:
    def __init__(self):
        # Cinématique
        self.t = []
        self.h = []
        self.l = []

        # Vitesses
        self.CAS = []
        self.TAS = []
        self.Mach = []

        # Aérodynamique
        self.Cz = []
        self.Cx = []

        # Vitesses composantes
        self.Vx = []
        self.Vz = []

        # Propulsion
        self.F_N = []
        self.SFC = []

        # Masse / carburant
        self.FB = []
        self.m = []

    def record(
        self,
        h,
        l,
        t=None,
        CAS=None,
        TAS=None,
        Mach=None,
        Cz=None,
        Cx=None,
        Vx=None,
        Vz=None,
        F_N=None,
        SFC=None,
        FB=None,
        m=None
    ):
        self.h.append(h)
        self.l.append(l)
        self.t.append(t)

        self.CAS.append(CAS)
        self.TAS.append(TAS)
        self.Mach.append(Mach)

        self.Cz.append(Cz)
        self.Cx.append(Cx)

        self.Vx.append(Vx)
        self.Vz.append(Vz)

        self.F_N.append(F_N)
        self.SFC.append(SFC)

        self.FB.append(FB)
        self.m.append(m)
