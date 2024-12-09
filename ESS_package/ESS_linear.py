from ESS_package.ESS import ESS


class ESS_linear(ESS):
    """
        Subclass that models a linear ESS.

        It is a formally a subclass, since it is equal to the superclass.
    """
    def __init__(self,
                 model,
                 Q,
                 p_S_max,
                 a,
                 b,
                 B,
                 eta,
                 SoC_0,
                 V_n,
                 SoC_min,
                 SoC_max,
                 Q_n
                 ):
        """
            Same as superclass initializer.
        """
        super().__init__(model,
                       Q,
                       p_S_max,
                       a,
                       b,
                       B,
                       eta,
                       SoC_0,
                       V_n,
                       SoC_min,
                       SoC_max,
                       Q_n
                       )

    def update_SoE_ch(self, p_GL_S, p_GL, delta_t):
        """
            Same as ESS.update_SoE_ch.
        """
        return super().update_SoE_ch(p_GL_S, p_GL, delta_t)

    def update_SoE_dch(self, p_GL_S, delta_t):
        """
            Same as ESS.update_SoE_dch.
        """
        return super().update_SoE_dch(p_GL_S, delta_t)

    def get_wear_cost(self, SoE_prev, p_S_k, delta_t):
        """
            Same as ESS.get_wear_cost.
        """
        return super().get_wear_cost(SoE_prev, p_S_k, delta_t)
