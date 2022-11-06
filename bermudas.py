import numpy as np
import pandas as pd
"""
Desarrollar un algoritmo que genere los valores de corte,
utilizando n trayectorias de un movimiento browniano geometrico,
para una opcion bermuda con madurez T, que puede ejercerse en t=T/3, 2T/3 o T
"""
TEST_TABLE = [[1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00],
              [1.09, 1.16, 1.22, 0.93, 1.11, 0.76, 0.92, 0.88],
              [1.08, 1.26, 1.07, 0.97, 1.56, 0.77, 0.84, 1.22],
              [1.34, 1.54, 1.03, 0.92, 1.52, 0.90, 1.01, 1.34], ]

table = [0.0, 0.0, 0.659, 0.1695, 0.0, 0.34, 0.26, 0.0]


class Bermudas():
    def __init__(self, s0, r, sigma, K, cantidad_trayectorias):
        self.s0 = s0
        self.r = r
        self.sigma = sigma
        self.K = K
        self.trayectorias = cantidad_trayectorias
        self.dataframe = []

    def main(self):
        """
        Para cada columna de la tabla, se obtiene el valor de cortes
        que maximiza el payoff
        Corregir: s_1_s no se hace con los valores correctos
        """
        # table = self.gen_table()
        table = TEST_TABLE
        self.K = 1.1
        self.gen_dataframe(table[0], table[1], table[2], table[3])
        s_3_s = self.K
        s_2_s = self.gen_star(table[2], table[3])
        s_1_s = self.gen_star(table[1], table[2])
        print(self.dataframe)
        print(s_1_s, s_2_s, s_3_s)
        return s_1_s, s_2_s, s_3_s

    def gen_table(self):
        """
        Genera una tabla 3xN con los valores de las trayectorias
        """
        motion_ammount = range(self.trayectorias)
        s_0 = [self.s0 for _ in motion_ammount]
        s_1 = [self.geo_brownian_motion(1/3, self.s0) for _ in motion_ammount]
        s_2 = [self.geo_brownian_motion(2/3, s_1[i]) for i in motion_ammount]
        s_3 = [self.geo_brownian_motion(1, s_2[i]) for i in motion_ammount]
        return [s_0, s_1, s_2, s_3]

    def gen_dataframe(self, s_0, s_1, s_2, s_3):
        df = pd.DataFrame()
        df['t = 0'] = s_0
        df['t = 1'] = s_1
        df['t = 2'] = s_2
        df['t = 3'] = s_3
        self.dataframe = df

    def geo_brownian_motion(self, tiempo, s0: float) -> float:
        sigma = self.sigma
        w_t = self.movimiento_browniano(tiempo)
        mean = (self.r - sigma**2/2) * tiempo/self.trayectorias
        return s0 * np.exp(mean + sigma*w_t)

    def movimiento_browniano(self, tiempo) -> float:
        return np.random.normal(0, np.sqrt(tiempo/self.trayectorias))

    def gen_star(self, columna, siguiente_columna) -> float:
        a = [self.get_maximizer(columna[i], columna, siguiente_columna) for i in range(self.trayectorias)]
        print(f"---{a}---")
        return columna[a.index(max(a))]

    def get_maximizer(self, elem_columna, columna, siguiente_columna):
        a = []
        for i in range(self.trayectorias):
            if columna[i] <= elem_columna:
                a.append((np.round(self.gen_payoff(columna[i]), 4)))
            else:
                a.append((np.round(self.deduct_period(self.gen_payoff(siguiente_columna[i])), 4)))
        return np.round(sum(a) / self.trayectorias, 4)

    def gen_payoff(self, s_i_j):
        return max(self.K - s_i_j, 0.0)

    def deduct_period(self, value):
        return value * np.exp(-self.r * 1)

    def valuate_bermuda_option(self):
        """Autocompletado"""
        s_1_s, s_2_s, s_3_s = self.main()
        promedio = (s_1_s + s_2_s + s_3_s) / 3
        ajuste = self.deduct_period(self.gen_payoff(s_1_s))
        return max(promedio, ajuste)


"""
Considerar: S0=36, r=0.06, σ=0.2, T= 1 año, K=35
"""
bermudas = Bermudas(36, 0.06, 0.2, 35, 8)
bermudas.valuate_bermuda_option()
