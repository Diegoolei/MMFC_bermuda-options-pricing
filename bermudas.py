from random import random
from numpy import exp
"""
Desarrollar un algoritmo que genere los valores de corte, 
utilizando n trayectorias de un movimiento browniano geometrico, 
para una opcion bermuda con madurez T, que puede ejercerse en t=T/3, 2T/3 o T
"""
def cut_gen(s0, r, sigma, T, K, cantidad):
    return movimiento_geometrico_browniano(s0, r, sigma, T, K, cantidad)

def movimiento_browniano(media, sigma, cantidad):
    return random.normal(media, sigma, cantidad)

def movimiento_geometrico_browniano(s0, tendencia, t, volatilidad, cantidad):
    return s0 * exp(tendencia * t + volatilidad * movimiento_browniano(tendencia, volatilidad, cantidad))

"""
Considerar: S0=36, r=0.06, σ=0.2, T= 1 año, K=35
S0:
r: ¿Log-Retorno?
sigma: Desviación Estandar {Volatilidad}
T:
K:
{Tendencia?}
"""

print(cut_gen(36, 0.06, 0.2, 1, 35))