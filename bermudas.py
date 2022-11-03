from random import random
from numpy import exp, sqrt

"""
Desarrollar un algoritmo que genere los valores de corte, 
utilizando n trayectorias de un movimiento browniano geometrico, 
para una opcion bermuda con madurez T, que puede ejercerse en t=T/3, 2T/3 o T
"""

class Bermudas():
    def __init__(self, s0, r, sigma, K, cantidad_trayectorias):
        self.s0 = s0
        self.r = r
        self.sigma = sigma
        self.K = K
        self.trayectorias = cantidad_trayectorias

    def gen_star(self):
        s_1, s_2, s_3 = self.gen_table()
        s_1_s = s_1[random.uniform(0, self.trayectorias)]
        s_2_s = s_2[random.uniform(0, self.trayectorias)]
        s_3_s = s_3[random.uniform(0, self.trayectorias)]
        return s_1_s, s_2_s, s_3_s

    def gen_table(self):
        s_1 = [self.gen_movimiento_geometrico_browniano(1/3, self.s0) for _ in range(self.trayectorias)]
        s_2 = [self.gen_movimiento_geometrico_browniano(2/3, s_1) for _ in range(self.trayectorias)]
        s_3 = [self.gen_movimiento_geometrico_browniano(1, s_2) for _ in range(self.trayectorias)]
        return s_1, s_2, s_3

    def gen_movimiento_geometrico_browniano(self, tiempo, s0):
        return s0 * exp((self.r - (self.sigma**2)/2)*(tiempo/self.trayectorias) + self.sigma * self.movimiento_browniano(tiempo))

    def movimiento_browniano(self, tiempo):
        return random.normal(0, sqrt(tiempo/self.trayectorias))

    def gen_payoff(self):
        s_1, s_2, s_3 = self.gen_table()
        return [max(self.K - max(s_1, s_2, s_3), 0) for _ in range(self.trayectorias)]

"""
Considerar: S0=36, r=0.06, σ=0.2, T= 1 año, K=35
"""
bermudas = Bermudas(36, 0.06, 0.2, 1, 35, 8)

