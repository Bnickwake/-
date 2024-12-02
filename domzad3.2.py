"""
Шалыгин Никита ФПэ-01-22

Условие задачи:

Для условия `задачи 1` построить график зависимости лопаточного кпд на среднем диаметре от
степени реактивности ступени $\eta_{ср}$ = f($\rho_{ср}$). Степень реактивности взять от 0.05 до 0.8 с шагом 0.001.
При численной невозможности вычислить треугольники скоростей при какой-либо степени реактивности, заменить лопаточный КПД
при этом значении степени реактивности на None


"""


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

# p_k = 5 * kPa
# p_0 = {"P = 5 МPa": 5 * MPa, "P = 10 МPa": 10 * MPa, "P = 15 МPa": 15 * MPa, "P = 20 МPa": 20 * MPa}
# t_0 = [300, 350, 400, 450, 500]


def calc_graf_lopat_kpd(P_0,T_0,P_2,D_cp,alfa_1_ср,
    d_beta,fi,psi,l, rps):
    """
    Функция строит график зависимости лопаточного кпд на среднем диаметре от
    степени реактивности ступени и сохраняет график в папку.

    """
    rho = []
    for i in range(751):
        rho.append(round((0.05 + l * i), 3))

    Efficiency = []
    Reactivity = []

    for reactivity in rho:

        i = i + 1
        inlet_point = gas(P=P_0 * unit, T=T_0)
        outlet_point = gas(P=P_2 * unit, s=inlet_point.s)
        theor_drop = inlet_point.h - outlet_point.h
        stator_drop = theor_drop * (1 - reactivity)
        rotor_drop = theor_drop * reactivity

        c_1t = (2 * 1000 * stator_drop)**0.5
        c_1 = c_1t * fi
        u = math.pi * D_cp * rps

        sin_alpha_1 = math.sin(math.radians(alfa_1_ср))
        cos_alpha_1 = math.cos(math.radians(alfa_1_ср))

        w_1 = (c_1 ** 2 + u ** 2 - 2 * c_1 * u * cos_alpha_1)**0.5
        w_2t = (w_1 ** 2 + 2 * rotor_drop * 1000)**0.5
        w_2 = w_2t * psi

        # Дополнительный расчёт, чтобы избежать отрицательных значений углов (Прямоугольный треугольник, катеты а,b и гипотенуза с)
        c = w_1
        a = cos_alpha_1 * c_1 - u
        beta_1 = math.acos(a / c)
        beta_1_deg = math.degrees(beta_1)
        sin_beta_1 = math.sin(math.radians(beta_1_deg))
        cos_beta_1 = math.cos(math.radians(beta_1_deg))
        beta_2_deg = beta_1_deg - d_beta
        sin_beta_2 = math.sin(math.radians(beta_2_deg))
        cos_beta_2 = math.cos(math.radians(beta_2_deg))

        c_2 = (w_2 ** 2 + u ** 2 - 2 * w_2 * u * cos_beta_2)**0.5

        outlet_speed_loss = 0.5 * c_2**2
        stator_speed_loss = 0.5 * ((c_1t ** 2) - (c_1 ** 2))
        rotor_speed_loss = 0.5 * ((w_2t ** 2) - (w_2 ** 2))

        a = sin_beta_2 * w_2  # Катет напротив угла альфа 2
        c = c_2  # Гипотенуза
        alpha_2 = math.asin(a / c)
        alpha_2_deg = math.degrees(alpha_2)
        cos_alpha_2 = math.cos(math.radians(alpha_2_deg))

        # Расчет лопаточного КПД
        constant_part = theor_drop * 1000 - stator_speed_loss - rotor_speed_loss
        useful_energy = constant_part - outlet_speed_loss
        efficiency = useful_energy / constant_part * 100

        # Замена КПД на None при невозможности вычислений
        relative_projection = w_1 * math.cos(beta_1) + w_2 * cos_beta_2
        absolute_projection = c_1 * cos_alpha_1 + c_2 * math.cos(alpha_2)
        if efficiency > 0:
            Reactivity.append(reactivity)
            Efficiency.append(efficiency)
            if absolute_projection == relative_projection:
                Reactivity.append(reactivity)
                Efficiency.append(None)

    fig, graf = plt.subplots(1, 1, figsize=(9, 7))
    graf.grid()
    graf.set_xlabel("Степень реактивности ступени")
    graf.set_ylabel("Лопаточный КПД, %")
    graf.set_title("График зависимости лопаточного КПД от степени реактивности ступени")
    graf.plot(Reactivity, Efficiency, label=f'График зависимости лопаточного КПД от степени реактивности ступени',
              color='green')
    graf.legend();

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    folder_name = "графики Шалыгин"
    folder_path = os.path.join(desktop_path, folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, 'dz3.2graf1.png')

    plt.savefig(file_path)

    return plt.show()

"""
Дано:
"""

P0 = 16.7 * MPa
t0 = to_kelvin(520)
P2 = 14.5 * MPa
D_cp = 0.892
alfa_1_ср = 13
d_beta = 5
fi = 0.97
psi = 0.935
l = 0.001
rps = 50
kappa = 1

if __name__ == "__main__":
    """
    Построение и вывод графика
    """

    itog = calc_graf_lopat_kpd(P0,t0,P2,D_cp,alfa_1_ср,
    d_beta,fi,psi,l, rps)


