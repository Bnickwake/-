'''

Шалыгин Никита ФПэ-01-22

Условие задачи:

Написать код отрисовывающий процесс расширения в турбине с промежуточным перегревом в PV-диаграмме.
Для примера отрисовки взять расчет при:
* P_0 = 25 МПа
* t_0 = 560 K
* P_k = 3.5 кПа
* P_{пп} = 3.62 МПа
* t_{пп} = 565 K
* eta_{oi} = 0.85
* eta_{мех} = 0.995
* eta_{эл} = 0.99
'''

from typing import List, Tuple, Optional
from iapws import IAPWS97 as gas
import matplotlib.pyplot as plt
import numpy as np
from math import log10
import os

MPa = 10 ** 6
kPa = 10 ** 3
unit = 1 / MPa
to_kelvin = lambda x: x + 273.15 if x else None


def graf_prom_peregrev(p_0,t_0,p_middle,t_middle,p_k,t_feed_water,
                       p_feed_water,internal_efficiency,mechanical_efficiency,generator_efficiency):
    """
    Функция отрисовывающая процесс расширения в турбине с промежуточным перегревом в PV-диаграмме.
    И сохраняет график в папку: графики Шалыгин.

    """

    delta_p0 = 0.05 * p_0
    delta_p_middle = 0.1 * p_middle
    delta_p_1 = 0.03 * p_middle

    real_p0 = p_0 - delta_p0
    real_p1t = p_middle + delta_p_middle
    real_p_middle = p_middle - delta_p_1

    _point_0 = gas(P=p_0 * unit, T=to_kelvin(t_0))
    point_0 = gas(P=real_p0 * unit, h=_point_0.h)
    point_1t = gas(P=real_p1t * unit, s=_point_0.s)

    hp_heat_drop = (_point_0.h - point_1t.h) * internal_efficiency
    h_1 = point_0.h - hp_heat_drop
    point_1 = gas(P=real_p1t * unit, h=h_1)

    _point_middle = gas(P=p_middle * unit, T=to_kelvin(t_middle))
    point_middle = gas(P=real_p_middle * unit, h=_point_middle.h)
    point_2t = gas(P=p_k * unit, s=_point_middle.s)

    lp_heat_drop = (_point_middle.h - point_2t.h) * internal_efficiency
    h_2 = point_middle.h - lp_heat_drop
    point_2 = gas(P=p_k * unit, h=h_2)

    def plot_curve_between_points(ax: plt.Axes, point_start: gas, point_end: gas, num_points: int = 200, **kwargs):
        s_values = np.linspace(point_start.s, point_end.s, num_points)
        MPa = 1e6
        v_values = []
        p_values = []
        for s in s_values:
            h = np.interp(s, [point_start.s, point_end.s], [point_start.h, point_end.h])
            try:
                intermediate_point = gas(s=s, h=h)
                v_values.append(intermediate_point.v)
                p_values.append(intermediate_point.P * MPa)
            except ValueError:
                continue

        ax.plot(v_values, p_values, **kwargs)

    def plot_isobars_therms(ax: plt.Axes, point_start: gas, num_points: int = 100, **kwargs):
        MPa = 1e6
        if point_start.P > 0.1:
            isoP_V = np.linspace(point_start.v - 0.007, point_start.v + 0.007, num_points)
            isoP_p = np.array([point_start.P for i in isoP_V])
            ax.plot(isoP_V, isoP_p * MPa, **kwargs)

            T_iso = point_start.T
            isoP = np.linspace(point_start.P - 1.5, point_start.P + 1.5, num_points)
            isoT_v = np.array([gas(P=i, T=T_iso).v for i in isoP])
            # isoT_p = []
            ax.plot(isoT_v, isoP * MPa, **kwargs)
        else:
            isoP_V = np.linspace(point_start.v - 0.05, point_start.v + 0.05, num_points)
            isoP_p = np.array([point_start.P for i in isoP_V])
            ax.plot(isoP_V, isoP_p * MPa, **kwargs)

            T_iso = point_start.T
            isoP = np.linspace(point_start.P, point_start.P + 1.5, num_points)
            isoT_v = np.array([gas(P=i, T=T_iso).v for i in isoP])
            # isoT_p = []
            ax.plot(isoT_v, isoP * MPa, **kwargs)

    ps = np.arange(1e3, 2.1e7, 1e5)
    pw = np.arange(1e3, 2.1e7, 1e5)

    vss = [gas(P=_p / MPa, x=1).v for _p in ps]
    vws = [gas(P=_p / MPa, x=0).v for _p in ps]
    hum94 = [gas(P=_p / MPa, x=0.94).v for _p in ps]
    hum85 = [gas(P=_p / MPa, x=0.85).v for _p in ps]

    fig, ax = plt.subplots(figsize=(10, 10))

    ax.plot(vws, ps, label='Линия сухости x=0', color="gray")
    ax.plot(vss, ps, label='Линия сухости x=1', color="gray")
    ax.plot(hum85, ps, label='Линия сухости x=0.85', color="gray")
    ax.plot(hum94, ps, label='Линия сухости x=0.94', color="gray")

    ax.scatter(_point_0.v, _point_0.P * MPa, color='red')  # , label='Начальная точка'
    ax.scatter(point_1.v, point_1.P * MPa, color='red')  # , label='Конечная точка'

    ax.scatter(point_0.v, point_0.P * MPa, color='red')
    ax.scatter(point_1t.v, point_1t.P * MPa, color='red')

    ax.scatter(point_1.v, point_1.P * MPa, color='red')
    ax.scatter(_point_middle.v, _point_middle.P * MPa, color='red')

    ax.scatter(point_middle.v, point_middle.P * MPa, color='red')
    ax.scatter(point_2.v, point_2.P * MPa, color='red')

    ax.scatter(_point_middle.v, _point_middle.P * MPa, color='red')
    ax.scatter(point_2t.v, point_2t.P * MPa, color='red')

    plot_curve_between_points(ax, _point_0, point_1, color='purple', label='Кривая интерполяции')
    plot_curve_between_points(ax, point_1, _point_middle, color='purple')
    plot_curve_between_points(ax, _point_middle, point_2, color='purple')

    plot_isobars_therms(ax, _point_0, color="orange")
    plot_isobars_therms(ax, point_0, color="orange")
    plot_isobars_therms(ax, point_1, color="orange")
    plot_isobars_therms(ax, point_1t, color="orange")
    plot_isobars_therms(ax, point_middle, color="orange")
    plot_isobars_therms(ax, _point_middle, color="orange")

    ax.set_xscale('log')
    ax.set_xlabel(r"$v, \frac{м^3}{кг}$", fontsize=14)
    ax.set_ylabel(r"$P, \text{МПа}$", fontsize=14)
    ax.set_title("Процесс расширения газа в турбине", fontsize=18)
    ax.legend()
    ax.grid()

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    folder_name = "графики Шалыгин"
    folder_path = os.path.join(desktop_path, folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, 'dz3.3graf1.png')

    plt.savefig(file_path)
    return plt.show()

"""
Дано:
"""

p_0 = 25 * MPa
t_0 = 560
p_middle = 3.62 * MPa
t_middle = 565
p_k = 3.5 * kPa
t_feed_water = 269
p_feed_water = 1.35 * p_0
internal_efficiency = 0.85
mechanical_efficiency = 0.995
generator_efficiency = 0.99

if __name__ == "__main__":
    """
    Построение и вывод графика
    """

    graf_prom_peregrev(p_0,t_0,p_middle,t_middle,p_k,t_feed_water,
                       p_feed_water,internal_efficiency,mechanical_efficiency,generator_efficiency)