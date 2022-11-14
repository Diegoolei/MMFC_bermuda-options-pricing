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
              [1.34, 1.54, 1.03, 0.92, 1.52, 0.90, 1.01, 1.34]]
K = 1.1


class Bermudas():
    def __init__(self, s0, r, sigma, K, cantidad_trayectorias):
        self.s0 = s0
        self.r = r
        self.sigma = sigma
        self.K = K
        self.trayectorias = cantidad_trayectorias
        self.dataframe = []

    def gen_barriers(self):
        """
        Para cada columna de la tabla, se obtiene el valor de cortes
        que maximiza el payoff
        """
        table = self.gen_table(self.trayectorias)
        # table = TEST_TABLE
        # self.K = 1.1
        self.gen_dataframe(table[0], table[1], table[2], table[3])

        payoff_column_3 = [self.gen_payoff(elem) for elem in table[3]]
        s_2_s = self.gen_barrier(table[2], payoff_column_3)

        s_2_s_payoff = self.get_cut_possible_values(s_2_s, table[2],
                                                    payoff_column_3)
        # print(f"V(3): {s_2_s_payoff}")
        s_1_s = self.gen_barrier(table[1], s_2_s_payoff)
        # print("--------------------------------------------------------------")
        # print(self.dataframe)
        return s_1_s, s_2_s, self.K

    def gen_table(self, n):
        """
        Genera una tabla 3xN con los valores de las trayectorias
        """
        motion_ammount = range(n)
        s_0 = [self.s0 for _ in motion_ammount]
        s_1 = [self.geo_brownian_motion(self.s0) for _ in motion_ammount]
        s_2 = [self.geo_brownian_motion(s_1[i]) for i in motion_ammount]
        s_3 = [self.geo_brownian_motion(s_2[i]) for i in motion_ammount]
        return [s_0, s_1, s_2, s_3]

    def gen_dataframe(self, s_0, s_1, s_2, s_3):
        df = pd.DataFrame()
        df['t = 0'] = s_0
        df['t = 1'] = s_1
        df['t = 2'] = s_2
        df['t = 3'] = s_3
        self.dataframe = df

    def geo_brownian_motion(self, s0):
        sigma = self.sigma
        w_t = self.brownian_motion()
        mean = (self.r - sigma**2/2) / 3
        return np.round(s0 * np.exp(mean + sigma*w_t), 4)

    def brownian_motion(self) -> float:
        return np.random.normal(0, np.sqrt(1/3))

    def gen_barrier(self, actual_column, payoff_column) -> float:
        """ Obtiene el valor de corte que maximiza el payoff """
        possible_cuts = [self.get_cut_possible_values(actual_column[i],
                                                      actual_column,
                                                      payoff_column)
                         for i in range(self.trayectorias)]

        # for possible_cut in possible_cuts:
        # print(f"""{ [np.round(elem, 4) for elem in possible_cut]}""")

        average = [np.round(np.sum(elem) / self.trayectorias, 4)
                   for elem in possible_cuts]
        # print(f"---{average}---")

        max_average_elem_index = average.index(np.max(average))
        return actual_column[max_average_elem_index]

    def get_cut_possible_values(self, possible_value,
                                actual_column, payoff_column):
        """ Obtiene la lista de los payoffs para cada posible corte"""
        posible_corte = []
        for i in range(self.trayectorias):
            if actual_column[i] <= possible_value:
                posible_corte.append(self.gen_payoff(actual_column[i]))
            else:
                posible_corte.append(self.deduct_period(payoff_column[i]))
        return [np.round(elem, 4) for elem in posible_corte]

    def gen_payoff(self, s_i_j):
        return max(self.K - s_i_j, 0.0)

    def deduct_period(self, value):
        return value * np.exp(-self.r * 1/3)

    def valuate_bermuda_option(self, s_1_s, s_2_s, s_3_s, n):
        table = self.gen_table(n)
        # table = TEST_TABLE
        self.gen_dataframe(table[0], table[1], table[2], table[3])
        # print(self.dataframe)
        v_3 = [self.gen_payoff(elem) for elem in table[3]]
        payoff_column_3 = self.get_cut_possible_values(s_3_s, table[3], v_3)
        # print(payoff_column_3)
        payoff_column_2 = self.get_cut_possible_values(s_2_s, table[2],
                                                       payoff_column_3)
        # print(payoff_column_2)
        payoff_column_1 = self.get_cut_possible_values(s_1_s, table[1],
                                                       payoff_column_2)
        # print(payoff_column_1)
        average = sum(payoff_column_1) / self.trayectorias
        deducted_average = self.deduct_period(average)

        early_exercise = max(self.K - self.s0, 0.0)
        return max(early_exercise, deducted_average)


"""
Considerar: S0=36, r=0.06, σ=0.2, T= 1 año, K=35
"""
bermudas_n_8 = Bermudas(35.1, 0.06, 0.2, 35, 8)
s_1_s, s_2_s, s_3_s = bermudas_n_8.gen_barriers()
print(f"s*(1): {s_1_s},")
print(f"s*(2): {s_2_s},")
print(f"s*(3): {s_3_s}")

prima_n_8 = bermudas_n_8.valuate_bermuda_option(s_1_s, s_2_s, s_3_s, 8)
print(f"la prima de la opción bermuda es: {prima_n_8:.4f}")

prima_n_8 = bermudas_n_8.valuate_bermuda_option(s_1_s, s_2_s, s_3_s, 8)
print(f"la prima de la opción bermuda es: {prima_n_8:.4f}")

bermudas_n_1000 = Bermudas(35, 0.06, 0.2, 35, 1000)
s_1_s, s_2_s, s_3_s = bermudas_n_1000.gen_barriers()

prima_n_20000 = bermudas_n_1000.valuate_bermuda_option(s_1_s, s_2_s,
                                                       s_3_s, 20000)
print(f"la prima de la opción bermuda es: {prima_n_20000:.4f}")

prima_n_20000 = bermudas_n_1000.valuate_bermuda_option(s_1_s, s_2_s,
                                                       s_3_s, 20000)
print(f"la prima de la opción bermuda es: {prima_n_20000:.4f}")
