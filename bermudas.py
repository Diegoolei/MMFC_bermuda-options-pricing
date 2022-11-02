from random import random
from numpy import exp, sqrt
"""
Desarrollar un algoritmo que genere los valores de corte, 
utilizando n trayectorias de un movimiento browniano geometrico, 
para una opcion bermuda con madurez T, que puede ejercerse en t=T/3, 2T/3 o T
"""

class Bermudas():
    def __init__(self, s0, r, sigma, tiempo, K, cantidad):
        self.s0 = s0
        self.r = r
        self.sigma = sigma
        self.tiempo = tiempo
        self.K = K
        self.cantidad = cantidad

    def cut_gen(self):
        for _ in range(self.cantidad):
            s_3_star = max(self.K - self.gen_movimiento_geometrico_browniano(), 0)

    def movimiento_browniano(self):
        return random.normal(self.media * self.tiempo, self.sigma * sqrt(self.tiempo), self.cantidad)

    def gen_movimiento_geometrico_browniano(self):
        return self.s0 * exp(self.tendencia * self.tiempo + self.volatilidad * self.movimiento_browniano())

"""
Considerar: S0=36, r=0.06, σ=0.2, T= 1 año, K=35
S0:
r: ¿Log-Retorno?
sigma: Desviación Estandar {Volatilidad}
T:
K:
{Tendencia?}
"""

bermudas = Bermudas(36, 0.06, 0.2, 1, 35, 8)

print(bermudas.cut_gen())
