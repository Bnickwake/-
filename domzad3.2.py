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

p_k = 5 * kPa
p_0 = {"P = 5 МPa": 5 * MPa, "P = 10 МPa": 10 * MPa, "P = 15 МPa": 15 * MPa, "P = 20 МPa": 20 * MPa}
t_0 = [300, 350, 400, 450, 500]


def calc_graf_lopat_kpd(p_0, t_0, p_2, avg_diameter, degree_of_reaction, alpha_1_deg, delta_beta_deg, fi, psi,
                   rotation_speed):
    kappa = 1
    DEG = []
    for i in range(750):
        DEG.append(float(degree_of_reaction + i * 0.001))
    # print(len(DEG))
    eta = []
    for j in range(len(DEG)):
        inlet_point = gas(P=p_0 * unit, T=t_0)
        outlet_point = gas(P=p_2 * unit, s=inlet_point.s)
        # print(DEG[j])
        theoretical_heat_drop = inlet_point.h - outlet_point.h
        stator_heat_drop = theoretical_heat_drop * (1 - DEG[j])
        rotor_heat_drop = theoretical_heat_drop * DEG[j]

        c_1t = (2 * 1000 * stator_heat_drop) ** 0.5
        c_1 = c_1t * fi
        u = math.pi * avg_diameter * rotation_speed

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

        mass_flow = outlet_point.rho * w_2 * math.pi * avg_diameter ** 2 / 2

        outlet_speed_loss = 0.5 * c_2 ** 2

        stator_speed_loss = 0.5 * ((c_1t ** 2) - (c_1 ** 2))
        rotor_speed_loss = 0.5 * ((w_2t ** 2) - (w_2 ** 2))

        constant_part = (
        theoretical_heat_drop * 1000 - kappa * outlet_speed_loss) - stator_speed_loss - rotor_speed_loss
        useful_energy = constant_part - (1 - kappa) * outlet_speed_loss
        eta.append(useful_energy / (theoretical_heat_drop * 1000 - kappa * outlet_speed_loss))
    plt.figure(figsize=(10, 6))
    plt.title('Зависимость eta от степени реактивности', fontsize=16)
    plt.xlabel('Степень реактивности', fontsize=14)
    plt.ylabel('eta', fontsize=14)
    plt.grid(True)
    plt.plot(DEG, eta, marker='o')

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    folder_name = "в гитхаб"
    folder_path = os.path.join(desktop_path, folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, 'dz3.2graf1.png')

    plt.savefig(file_path)

    return plt.show()


p_0 = 16.7 * MPa
t_0 = to_kelvin(520)
p_2 = 14.5 * MPa
avg_diameter = 0.892
degree_of_reaction = 0.05
alpha_1_deg = 13
delta_beta_deg = 5
fi = 0.97
psi = 0.935
rotation_speed = 50

itog = calc_graf_lopat_kpd(p_0, t_0, p_2, avg_diameter, degree_of_reaction, alpha_1_deg, delta_beta_deg, fi, psi,
                     rotation_speed)


