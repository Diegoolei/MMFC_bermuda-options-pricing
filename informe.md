# Valoración de opciones "Bermuda"

Diego Oleiarz, 14/11/22

---

## Introducción

Las opciones bermudas se caracterizan por ser un punto medio entre las opciones europeas (las cuales solo pueden ser ejercidas al vencimiento de las mismas) y las opciones americanas (que pueden ser ejercidas en cualquier momento del plazo de vencimiento).
En la práctica, las opciones bermudas son opciones americanas que solo pueden ser ejercidas en momentos determinados del plazo de vencimiento.
 Al ser una variación de las opciones americanas, las opciones bermudas tienen las mismas características que estas últimas, por lo que se puede decir que las opciones bermudas son opciones americanas con restricciones en el momento de ejercicio.
 Esto no significa que la forma de valorarlas sea la misma, ya que las opciones bermudas tienen un valor intrínseco distinto al de las opciones americanas, por lo que su valoración es distinta.
 Debido a esto, las opciones bermudas son más difíciles de valorar que las opciones americanas, ya que se debe tener en cuenta el valor intrínseco de la opción en cada momento de corte.
 En este informe se analizará la forma de valorar las opciones bermudas, utilizando una variación el modelo de Black-Scholes para la valoración de las opciones americanas.

## Algoritmo

En sí el algorítmo conlleva pocos pasos:

1. Generar los valores del activo subyacente en cada momento de corte, a través de movimientos geométricos brownianos
2. Generar las cotas inferiores conocidas como valores de barrera (ejercicio mediante parametros de barrera) a partir de los datos obtenidos en el paso anterior
3. Descartar los valores del paso 1 y generar nuevos utilizando el mismo método, pero guardando las cotas inferiores obtenidas en el paso 2
4. Con los nuevos valores y las cotas inferiores, valorar la opción bermuda.

## Análisis del Código

El código se encuentra en el archivo `bermuda.py` y se puede ejecutar con el comando `python bermuda.py`.
El código se divide en 3 partes:

1. Generación de los valores del activo subyacente
2. Generación de las cotas inferiores
3. Valoración de la opción bermuda

### Generación de los valores del activo subyacente

La generación de los valores del activo subyacente se realiza mediante el método `brownian_motion` de la clase `Bermuda`. Este método recibe como parámetros:

* `self`: instancia de la clase `Bermuda`
* `S0`: valor inicial del activo subyacente
* `mu`: tasa de crecimiento del activo subyacente
* `sigma`: volatilidad del activo subyacente
* cantidad_trayectorias: numero de trayectorias a generar

El método `brownian_motion` genera los valores del activo subyacente en cada momento de corte, a través de movimientos geométricos brownianos. Para esto, se utiliza la siguiente fórmula:

$$
S_{t} = S_{0}e^{(r-\frac{\sigma^{2}}{2})t+\sigma W_{t}}
$$

Donde $S_{t}$ es el valor del activo subyacente en el momento $t$, $S_{0}$ es el valor inicial del activo subyacente, $r$ es la tasa de crecimiento del activo subyacente, $\sigma$ es la volatilidad del activo subyacente, $t$ es el plazo de vencimiento de la opción, $W_{t}$ es el movimiento browniano en el momento $t$.

### Generación de las cotas inferiores

La generación de las cotas inferiores se realiza mediante el método `gen_star` de la clase `Bermuda`. Este método recibe como parámetros:

* `self`: instancia de la clase `Bermuda`
* `columna`: listado de valores del activo subyacente en el momento de corte correspondiente
* `siguiente_columna`: listado de valores del activo subyacente en el momento de corte siguiente

El método `gen_star` genera las cotas inferiores conocidas como valores de barrera (enfoque de ejercicio mediante parametros de barrera) mediante los datos obtenidos en el paso anterior. Para esto, con cada valor del listado `columna` individualmente se compara contra todos los valores del listado `siguiente_columna`. Si el valor de `columna` es mayor que el valor de `siguiente_columna`, quiere decir que en ese momento se debería ejercer la opción, por lo que se guarda como un posible valor de corte en una lista

### Valoración de la opción bermuda

La valoración de la opción bermuda se realiza mediante el método `valuate_bermuda_option` de la clase `Bermuda`. Este método recibe como parámetros:

* `self`: instancia de la clase `Bermuda`

El método `valuate_bermuda_option` con los nuevos valores y las cotas inferiores, valorar la opción bermuda. Para esto, se utiliza la siguiente fórmula:

$$
C_{0} = \frac{1}{M}\sum_{i=1}^{M}max(K-S_{i}^{N},0)
$$

Donde $C_{0}$ es el valor de la opción bermuda, $S_{i}^{N}$ es el valor del activo subyacente en el momento de corte $N$, $K$ es el precio de ejercicio de la opción, $M$ es el número de tiempos de corte.

## Resultados

Los resultados obtenidos se muestran en la siguiente tabla:

| N  | M    | Valor de la opción bermuda |
| -- | ---- | --------------------------- |
| 10 | 1000 |                             |

## Conclusiones

## link al repositorio

https://github.com/Diegoolei/MMFC_bermuda-options-pricing
