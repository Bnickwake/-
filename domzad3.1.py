import iapws
import matplotlib.pyplot as plt
import numpy as np
from iapws import IAPWS97 as gas
import math
import os

MPa = 10 ** 6
kPa = 10 ** 3
unit = 1 / MPa
to_kelvin = lambda x: x + 273.15 if x else None

p_0 = 16.7 * MPa
t_0 = to_kelvin(520)
p_2 = 14.5 * MPa
avg_diameter = 0.892
degree_of_reaction = 0.08
alpha_1_deg = 13
delta_beta_deg = 5
fi = 0.97
psi = 0.935
rotation_speed = 50
kol_vo_secheni=10



def calc_traingals(p_0, t_0, p_2, avg_diameter, degree_of_reaction, alpha_1_deg, delta_beta_deg, fi, psi,
                   rotation_speed,kol_vo_secheni):
    c1_plot = []
    u1_plot = []
    w1_plot = []
    w2_plot = []
    u2_plot = []
    c2_plot = []
    for i in range(kol_vo_secheni):
        for one in range(1, 11):
            AvG = avg_diameter / one
            DeG = degree_of_reaction / one
            inlet_point = gas(P=p_0 * unit, T=t_0)
            outlet_point = gas(P=p_2 * unit, s=inlet_point.s)

            theoretical_heat_drop = inlet_point.h - outlet_point.h
            stator_heat_drop = theoretical_heat_drop * (1 - DeG)
            rotor_heat_drop = theoretical_heat_drop * DeG

            c_1t = (2 * 1000 * stator_heat_drop) ** 0.5
            c_1 = c_1t * fi
            u = math.pi * (AvG) * rotation_speed

            sin_alpha_1 = math.sin(math.radians(alpha_1_deg))
            cos_alpha_1 = math.cos(math.radians(alpha_1_deg))

            w_1 = (c_1 ** 2 + u ** 2 - 2 * c_1 * u * cos_alpha_1) ** 0.5
            w_2t = (w_1 ** 2 + 2 * rotor_heat_drop * 1000) ** 0.5
            w_2 = w_2t * psi

            beta_1 = math.atan(sin_alpha_1 / (cos_alpha_1 - u / c_1))
            beta_1_deg = math.degrees(beta_1)
            beta_2_deg = beta_1_deg - delta_beta_deg

            sin_beta_2 = math.sin(math.radians(beta_2_deg))
            cos_beta_2 = math.cos(math.radians(beta_2_deg))

            c_2 = (w_2 ** 2 + u ** 2 - 2 * w_2 * u * cos_beta_2) ** 0.5

            alpha_2 = math.atan(sin_beta_2 / (cos_beta_2 - u / w_2))
            alpha_2_deg = math.degrees(alpha_2)
            c1_plot.append([[0, -c_1 * cos_alpha_1], [0, -c_1 * sin_alpha_1]])
            u1_plot.append([[-c_1 * cos_alpha_1, -c_1 * cos_alpha_1 + u], [-c_1 * sin_alpha_1, -c_1 * sin_alpha_1]])
            w1_plot.append([[0, -c_1 * cos_alpha_1 + u], [0, -c_1 * sin_alpha_1]])

            w2_plot.append([[0, w_2 * cos_beta_2], [0, -w_2 * sin_beta_2]])
            u2_plot.append([[w_2 * cos_beta_2, w_2 * cos_beta_2 - u], [-w_2 * sin_beta_2, -w_2 * sin_beta_2]])
            c2_plot.append([[0, w_2 * cos_beta_2 - u], [0, -w_2 * sin_beta_2]])

    fig, ax = plt.subplots(1, 1, figsize=(15, 5))
    for i in range(kol_vo_secheni):
        ax.plot(c1_plot[i][0], c1_plot[i][1], label='C_1', c='red')
        ax.plot(u1_plot[i][0], u1_plot[i][1], label='u_1', c='blue')
        ax.plot(w1_plot[i][0], w1_plot[i][1], label='W_1', c='green')

        ax.plot(w2_plot[i][0], w2_plot[i][1], label='W_2', c='green')
        ax.plot(u2_plot[i][0], u2_plot[i][1], label='u_2', c='blue')
        ax.plot(c2_plot[i][0], c2_plot[i][1], label='C_2', c='red')

    ax.set_title("Треугольники скоростей")
    ax.legend()

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    folder_name = "в гитхаб"
    folder_path = os.path.join(desktop_path, folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, 'dz3.1graf1.png')

    plt.savefig(file_path)
    return plt.show()

kodik=calc_traingals(p_0, t_0, p_2, avg_diameter, degree_of_reaction,
                    alpha_1_deg, delta_beta_deg, fi, psi,rotation_speed,kol_vo_secheni)