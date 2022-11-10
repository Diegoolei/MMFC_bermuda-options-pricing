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

    def get_cut_values(self):
        """
        Para cada columna de la tabla, se obtiene el valor de cortes
        que maximiza el payoff
        """
        table = self.gen_table(self.trayectorias)
        #table = TEST_TABLE
        #self.K = 1.1
        self.gen_dataframe(table[0], table[1], table[2], table[3])
        payoff_column_3 = [self.gen_payoff(elem) for elem in table[3]]
        s_2_s = self.gen_star(table[2], payoff_column_3)
        s_2_s_payoff = self.get_cut_possible_values(s_2_s, table[2],
                                                    payoff_column_3)
        #print(f"V(3): {s_2_s_payoff}")
        s_1_s = self.gen_star(table[1], s_2_s_payoff)
        #print("--------------------------------------------------------------")
        #print(self.dataframe)
        return s_1_s, s_2_s, self.K

    def gen_table(self, n):
        """
        Genera una tabla 3xN con los valores de las trayectorias
        """
        motion_ammount = range(n)
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

    def geo_brownian_motion(self, tiempo, s0):
        sigma = self.sigma
        w_t = self.movimiento_browniano(tiempo)
        mean = (self.r - sigma**2/2) * tiempo/self.trayectorias
        return np.round(s0 * np.exp(mean + sigma*w_t), 4)

    def movimiento_browniano(self, tiempo) -> float:
        return np.random.normal(0, np.sqrt(tiempo/self.trayectorias))

    def gen_star(self, columna, payoff_column) -> float:
        """ Obtiene el valor de corte que maximiza el payoff """
        possible_cuts = [self.get_cut_possible_values(columna[i], columna,
                                                      payoff_column)
                         for i in range(self.trayectorias)]

        #for possible_cut in possible_cuts:
        #    print(f"""{ [np.round(elem, 4) for elem in possible_cut]}""")

        average = [np.round(np.sum(elem) / self.trayectorias, 4)
                   for elem in possible_cuts]
        #print(f"---{average}---")

        max_average_elem_index = average.index(np.max(average))
        return columna[max_average_elem_index]

    def get_cut_possible_values(self, elem_columna,
                                columna, siguiente_columna):
        """ Obtiene la lista de los payoffs para cada posible corte"""
        posible_corte = []
        for i in range(self.trayectorias):
            if columna[i] <= elem_columna:
                posible_corte.append(self.gen_payoff(columna[i]))
            else:
                posible_corte.append(self.deduct_period(siguiente_columna[i]))
        return [np.round(elem, 4) for elem in posible_corte]

    def gen_payoff(self, s_i_j):
        return max(self.K - s_i_j, 0.0)

    def deduct_period(self, value):
        return value * np.exp(-self.r * 1)

    def valuate_bermuda_option(self, s_1_s, s_2_s, s_3_s, n):
        table = self.gen_table(n)
        self.gen_dataframe(table[0], table[1], table[2], table[3])
        #print(self.dataframe)
        v_3 = [self.gen_payoff(elem) for elem in table[3]]
        payoff_column_3 = self.get_cut_possible_values(s_3_s, table[3], v_3)
        #print(payoff_column_3)
        payoff_column_2 = self.get_cut_possible_values(s_2_s, table[2], payoff_column_3)
        #print(payoff_column_2)
        payoff_column_1 = self.get_cut_possible_values(s_1_s, table[1], payoff_column_2)
        #print(payoff_column_1)
        average = sum(payoff_column_1) / self.trayectorias
        deducted_average = self.deduct_period(average)

        early_exercise = max(self.K - self.s0, 0.0)
        return max(early_exercise, deducted_average)


"""
Considerar: S0=36, r=0.06, σ=0.2, T= 1 año, K=35
"""
bermudas_n_8 = Bermudas(35, 0.06, 0.2, 35, 8)
s_1_s, s_2_s, s_3_s = bermudas_n_8.get_cut_values()
print(f"s*(1): {s_1_s},")
print(f"s*(2): {s_2_s},")
print(f"s*(3): {s_3_s}")

prima_n_8 = bermudas_n_8.valuate_bermuda_option(s_1_s, s_2_s, s_3_s, 8)
print(f"la prima de la opción bermuda es: {prima_n_8}")

prima_n_8 = bermudas_n_8.valuate_bermuda_option(s_1_s, s_2_s, s_3_s, 8)
print(f"la prima de la opción bermuda es: {prima_n_8}")

bermudas_n_1000 = Bermudas(35, 0.06, 0.2, 35, 1000)
s_1_s, s_2_s, s_3_s = bermudas_n_1000.get_cut_values()

prima_n_20000 = bermudas_n_1000.valuate_bermuda_option(s_1_s, s_2_s, s_3_s, 20000)
print(f"la prima de la opción bermuda es: {prima_n_20000}")
prima_n_20000 = bermudas_n_1000.valuate_bermuda_option(s_1_s, s_2_s, s_3_s, 20000)
print(f"la prima de la opción bermuda es: {prima_n_20000}")
