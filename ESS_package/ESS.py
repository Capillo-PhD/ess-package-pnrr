class ESS:
    """
    Energy Storage System (ESS) model.

    Superclass that models a linear ESS, being the latter the simplest one to be extended.

    Attributes
    ----------
    model : str
        Identifier or name of the ESS model.
    Q : float
        Capacity in kWh.
    p_S_max : float
        Maximum charging/discharging power in kW.
    a : float
        Empirical cost model parameter.
    b : float
        Empirical cost model parameter.
    B : float
        Empirical cost model parameter.
    eta : float
        Efficiency.
    SoE_0 : float
        Initial state of energy.
    V_n : float
        Nominal voltage of the ESS in V, assumed constant.
    SoE_min : float
        Minimum allowable state of energy, for a longer ESS life.
    SoE_max : float
        Maximum allowable state of energy, for a longer ESS life.
    Q_n : float
        Nominal capacity in kWh.
    """
    def __init__(self,
                 model,
                 Q,
                 p_S_max,
                 a,
                 b,
                 B,
                 eta,
                 SoE_0,
                 V_n,
                 SoE_min,
                 SoE_max,
                 Q_n
                 ):
        """
            Initializer of the ESS model syperclass.


            Parameters
            ----------
            model : str
                Identifier or name of the ESS model.
            Q : float
                Capacity in kWh.
            p_S_max : float
                Maximum charging/discharging power in kW.
            a : float
                Empirical cost model parameter.
            b : float
                Empirical cost model parameter.
            B : float
                Empirical cost model parameter.
            eta : float
                Efficiency.
            SoE_0 : float
                Initial state of energy.
            V_n : float
                Nominal voltage of the ESS in V, assumed constant.
            SoE_min : float
                Minimum allowable state of energy, for a longer ESS life.
            SoE_max : float
                Maximum allowable state of energy, for a longer ESS life.
            Q_n : float
                Nominal capacity in kWh.
        """
        self.model = model
        self.Q = Q
        self.p_S_max = p_S_max
        self.a = a
        self.b = b
        self.B = B
        self.eta = eta
        self.SoE_0 = SoE_0
        self.V_n = V_n
        self.SoE_min = SoE_min
        self.SoE_max = SoE_max
        self.SoE = self.SoE_0
        self.Q_n = Q_n


    def update_SoE_ch(self, p_GL_S, p_GL, delta_t):
        """
           Updates the state of energy during charging.

           Parameters
           ----------
           p_GL_S : float
               Power flow between Grid Load (GL) and Storage (S) in kW.
           p_GL : float
               Power from the Grid Load (GL) in kW.
           delta_t : float
               Simulation timestep in seconds.
        """
        p_GL_S = p_GL_S * self.eta
        en = abs(p_GL_S * delta_t) / self.Q
        self.SoE = self.SoE + en
        excess = 0
        if self.SoE > self.SoE_max:
            self.SoE = self.SoE_max
            excess = (self.SoE_max - self.SoE) * self.Q
        return excess

    def update_SoE_dch(self, p_GL_S, delta_t):
        """
            Updates the state of energy during charging.

            Parameters
            ----------
            p_GL_S : float
                Power flow between Grid Load (GL) and Storage (S) in kW.
            p_GL : float
                Power from the Grid Load (GL) in kW.
            delta_t : float
                Simulation timestep in seconds.
        """
        p_GL_S = p_GL_S / self.eta
        en = abs(p_GL_S * delta_t) / self.Q
        self.SoE = self.SoE - en
        lack = 0
        if self.SoE < self.SoE_min:
            self.SoE = self.SoE_min
            lack = (self.SoE_min - self.SoE) * self.Q
        return lack

    def get_wear_cost(self, SoE_prev, p_S_k, delta_t):
        """
            Estimates the battery wear cost, by implementing to an empirical cost model.

            Parameters
            ----------
            p_GL_S : float
                Power flow between Grid Load (GL) and Storage (S) in kW.
            delta_t : float
                Simulation timestep in seconds.

            Returns
            ----------
            C_b_k : float
                Battery wear cost.
        """
        W_SoC_k_prec = (self.B / (2 * self.Q * self.eta)) * (self.b * pow((1 - SoE_prev), (self.b - 1))) / self.a
        W_SoC_k = (self.B / (2 * self.Q * self.eta)) * (self.b * pow((1 - self.SoE), (self.b - 1))) / self.a
        C_b_k = ((delta_t / 2) * (W_SoC_k_prec + W_SoC_k)) * (abs(p_S_k))
        return C_b_k

