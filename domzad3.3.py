from typing import List, Tuple, Optional
from iapws import IAPWS97 as gas
import matplotlib.pyplot as plt
import numpy as np
from math import log10
import os

def graf_prom_peregrev(p_0,t_0,p_middle,t_middle,p_k,t_feed_water,
                       p_feed_water,internal_efficiency,mechanical_efficiency,generator_efficiency):


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


    def get_humidity_constant_line(degree_of_dryness, pressure_range):
        v_values = []
        p_values = []

        for P in pressure_range:
            try:
                point = gas(P=P, x=degree_of_dryness)
                v_values.append(point.v)
                p_values.append(point.P)
            except ValueError:
                continue

        return np.array(v_values), np.array(p_values)


    def plot_curve_between_points(ax: plt.Axes, point_start: gas, point_end: gas, num_points: int = 100, **kwargs):
        s_values = np.linspace(point_start.s, point_end.s, num_points)

        v_values = []
        p_values = []
        for s in s_values:
            h = np.interp(s, [point_start.s, point_end.s], [point_start.h, point_end.h])
            try:
                intermediate_point = gas(s=s, h=h)
                v_values.append(intermediate_point.v)
                p_values.append(intermediate_point.P)
            except ValueError:
                continue

        ax.plot(v_values, p_values, **kwargs)

    degrees_of_dryness = [point_2.x, point_2t.x, 1]

    pressure_range = np.logspace(-3, 0.4, 100)
    v_range = np.logspace(-3, 2, 100)

    # Создание графика
    fig, ax = plt.subplots(figsize=(10, 10))

    for degree in degrees_of_dryness:
        v_values, p_values = get_humidity_constant_line(degree, pressure_range)
        ax.plot(v_values, p_values, label=f'Линия сухости x={degree:.2f}')

    plot_curve_between_points(ax, _point_0, point_1, color='purple', label='Кривая интерполяции')
    ax.scatter(_point_0.v, _point_0.P, color='red')  # , label='Начальная точка'
    ax.scatter(point_1.v, point_1.P, color='red')  # , label='Конечная точка'

    plot_curve_between_points(ax, _point_0, point_1t, color='purple')
    ax.scatter(_point_0.v, _point_0.P, color='red')
    ax.scatter(point_1t.v, point_1t.P, color='red')

    plot_curve_between_points(ax, point_1, _point_middle, color='purple')
    ax.scatter(point_1.v, point_1.P, color='red')
    ax.scatter(_point_middle.v, _point_middle.P, color='red')

    plot_curve_between_points(ax, _point_middle, point_2, color='purple')
    ax.scatter(_point_middle.v, _point_middle.P, color='red')
    ax.scatter(point_2.v, point_2.P, color='red')

    plot_curve_between_points(ax, _point_middle, point_2t, color='purple')
    ax.scatter(_point_middle.v, _point_middle.P, color='red')
    ax.scatter(point_2t.v, point_2t.P, color='red')

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel("v, м^3/кг", fontsize=14)
    ax.set_ylabel("P, МПа", fontsize=14)
    ax.set_title("Процесс расширения газа в турбине", fontsize=18)
    ax.legend()
    ax.grid()

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    folder_name = "в гитхаб"
    folder_path = os.path.join(desktop_path, folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, 'dz3.3graf1.png')

    plt.savefig(file_path)
    return plt.show()

MPa = 10 ** 6
kPa = 10 ** 3
unit = 1 / MPa
to_kelvin = lambda x: x + 273.15 if x else None

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


graf_prom_peregrev(p_0,t_0,p_middle,t_middle,p_k,t_feed_water,
                       p_feed_water,internal_efficiency,mechanical_efficiency,generator_efficiency)