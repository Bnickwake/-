# Шалыгин Никита ФПэ-01-22

import numpy as np
import matplotlib.pyplot as plt
import iapws
from iapws import IAPWS97 as gas

MPa = 10 ** 6
kPa = 10 ** 3
unit = 1 / MPa
grad_Cels = 1
                  #Задача 1
#Построить график зависимости термического КПД паротурбинного цикла без промежуточного перегрева пара при следующих параметрах пара:
# 𝑃0 = 5, 10, 15, 20 МПа. Для каждого значения взять следующие значения температуры
# 𝑡0= 300, 350, 400, 450, 500 градусов Цельсия,
# 𝑃𝑘= 5 кПа. Принять давление за последней ступенью паровой турбины
# 𝑃2=𝑃𝑘. Термический КПД цикла оценивать без учета подогрева воды в питательном насосе и регенеративной системе.

# масивы значений давления и темпратуры
p0 = np.array([5, 10 , 15 , 20]) # Мега Паскаль
t0 = np.array([300, 350, 400, 450 ,500]) # Градус Цельсия
pk = 5 * kPa
# 1) KPD- массив КПД
for P0 in p0:
    KPD = []
    for T0 in t0:
        point_0 = gas(P = P0, T = (T0 + 273.15))
        point_condenser_inlet = gas(P = (pk * unit) , s = point_0.s)
        point_pump_outlet = gas(P = (pk * unit), x = 0)
        useful_energy = point_0.h - point_condenser_inlet.h
        full_energy = point_0.h - point_pump_outlet.h
        kpd_value = (useful_energy / full_energy) * 100
        KPD.append(kpd_value)
    plt.xlabel("t0, градусы Цельсия")
    plt.ylabel("Термический КПД, %")
    plt.title("График зависимости термического КПД от to")
    plt.plot(t0[0:5],KPD[0:5], label = f"При P0 = {P0} МПа")
plt.grid()
plt.legend()
plt.show()


                # Задача 2
# Построить график зависимости термического КПД паротурбинного цикла без промежуточного перегрева пара при следующих параметрах пара:
# 𝑃0= 5 МПа,
# 𝑡0= 450 градусов Цельсия,
# 𝑃𝑘= 5, 10, 15, 20, 50 кПа. Принять давление за последней ступенью паровой турбины
# 𝑃2= 𝑃𝑘. Термический КПД цикла оценивать без учета подогрева воды в питательном насосе и регенеративной системе.


# Значение давления и темпратуры
p0 = 5   #мега паскаль
t0 = 450 #градусы цельсия
pk = np.array([5, 10, 15, 20, 50]) # Кило Паскаль
# 1) KPD- массив КПД
KPD = []
for Pk in pk:
    point_0 = gas(P = p0, T = (t0 + 273.15))
    point_condenser_inlet = gas(P = Pk * (kPa / MPa), s = point_0.s)
    point_pump_outlet = gas(P = Pk * (kPa / MPa), x = 0)
    useful_energy = point_0.h - point_condenser_inlet.h
    full_energy = point_0.h - point_pump_outlet.h
    kpd_value = (useful_energy / full_energy) * 100
    KPD.append(kpd_value)
plt.xlabel("Pk, кПа")
plt.ylabel("Термический КПД, %")
plt.title("График зависимости термического КПД от Pk")
plt.plot(pk[0:5],KPD[0:5], label = f"При P0 = {p0} (МПа) и температуре t0= {t0} (градус Цельсия)")
plt.grid()
plt.legend( loc='upper left')
plt.show()


