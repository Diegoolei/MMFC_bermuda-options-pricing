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
Para poder ejecutar el código se debe tener instalado `numpy` (pip install numpy) y `pandas` (pip install pandas).
El código se divide en 3 partes:

1. Generación de los valores del activo subyacente
2. Generación de las cotas inferiores
3. Valoración de la opción bermuda

### Generación de los valores del activo subyacente

La generación de los valores del activo subyacente se realiza mediante el método `geo_brownian_motion` de la clase `Bermuda`. Este método recibe como parámetros:

* `self`: instancia de la clase `Bermuda`
* `delta_t`: paso de tiempo entre cada valor generado
* `s0`: valor inicial del activo subyacente

El método `brownian_motion` genera los valores del activo subyacente en cada momento de corte, a través de movimientos geométricos brownianos. Para esto, se utiliza la siguiente fórmula:

$$
S_{t} = S_{0}e^{(r-\frac{\sigma^{2}}{2})t+\sigma W_{t}}
$$

Donde $S_{t}$ es el valor del activo subyacente en el momento $t$, $S_{0}$ es el valor inicial del activo subyacente, $r$ es la tasa de crecimiento del activo subyacente, $\sigma$ es la volatilidad del activo subyacente, $t$ es el plazo de vencimiento de la opción, $W_{t}$ es el movimiento browniano en el momento $t$.

### Generación de las cotas inferiores

La generación de las cotas inferiores se realiza mediante el método `gen_barrier` de la clase `Bermuda`. Este método recibe como parámetros:

* `self`: instancia de la clase `Bermuda`
* `actual_column`: listado de valores del activo subyacente en el momento de corte `t`
* `payoff_column`: listado de valores del activo subyacente en el momento de corte `t + 1`

El método `gen_barrier` genera las cotas inferiores conocidas como valores de barrera (enfoque de ejercicio mediante parametros de barrera) mediante los datos obtenidos en el paso anterior. Para esto, con cada valor del listado `actual_column` se compara individualmente (de ahora en mas `possible_value`) contra todos los valores del listado `payoff_column`.

```python
    posible_corte = []
    for i in range(self.trayectorias):
```

Si `possible_value` es mayor que el valor de `actual_column[i]`, quiere decir que en ese momento se debería ejercer la opción utilizando el valor `actual_column[i]`, por lo que se guarda su payoff como un posible valor de corte en una lista.

```python
    if actual_column[i] <= possible_value:
        posible_corte.append(self.gen_payoff(actual_column[i]))
```

Si `possible_value` es menor que el valor de `actual_column[i]`, quiere decir que en ese momento no se debería ejercer la opción, por lo que se guarda el valor de `payoff_column[i]` deducido un período como un posible valor de corte en una lista.

```python
    else:
        posible_corte.append(self.deduct_period(payoff_column[i]))

```

Al finalizar el cíclo, se obtiene el promedio de los valores guardados en la lista `posible_corte` y se guarda como posible valor de corte para el momento `t`.

```python
    return sum(posible_corte) / len(posible_corte)
```

Se repite el proceso para todos los elementos de `actual_column`, al terminar se guarda el máximo `posible_corte` y se guarda el valor de `actual_column` correspondiente al mismo como el valor de corte para el momento `t`.
```python
    average = [sum(elem) / len(possible_cuts) for elem in possible_cuts]
    max_average_elem_index = average.index(np.max(average))
    return actual_column[max_average_elem_index]
```
### Valoración de la opción bermuda

La valoración de la opción bermuda se realiza mediante el método `valuate_bermuda_option` de la clase `Bermuda`. Este método recibe como parámetros:

* `self`: instancia de la clase `Bermuda`
* `s_1_s, s_2_s, s_3_s`: valores de corte al momento `t=1`, `t=2` y `t=3` respectivamente
* `n`: cantidad de pasos de tiempo a simular

El método `valuate_bermuda_option` utiliza las cotas inferiores obtenidas anteriormente y nuevos valores generados para el activo subyacente para obtener la prima para la opción bermuda.
Para ello, genera una nueva tabla de valores utilizando `gen_table` y con ellos 

```python
    table = self.gen_table(n)

    v_3 = [self.gen_payoff(elem) for elem in table[3]]
    payoff_column_3 = self.get_cut_possible_values(s_3_s, table[3], v_3)
    payoff_column_2 = self.get_cut_possible_values(s_2_s, table[2],
                                                    payoff_column_3)
    payoff_column_1 = self.get_cut_possible_values(s_1_s, table[1],
                                                    payoff_column_2)
    average = sum(payoff_column_1) / self.trayectorias
    deducted_average = self.deduct_period(average)

    early_exercise = max(self.K - self.s0, 0.0)
    return max(early_exercise, deducted_average)
```

## Resultados

Los resultados obtenidos se muestran en la siguiente tabla:

| N  | M    | Valor de la opción bermuda |
| -- | ---- | --------------------------- |
| 10 | 1000 |                             |

## Conclusiones

## link al repositorio

https://github.com/Diegoolei/MMFC_bermuda-options-pricing
