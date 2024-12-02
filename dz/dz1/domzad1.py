''' Шалыгин Никита ФПэ-01-22 

Задача 1

Построить `график` зависимости термического КПД паротурбинного цикла без промежуточного перегрева пара при следующих параметрах пара:
$P_0$ = 5, 10, 15, 20 MPa. Для каждого значения взять следующие значения температуры $t_0$ = 300, 350, 400, 450, 500 градусов Цельсия, $P_k$ = 5 kPa.
Принять давление за последней ступенью паровой турбины $P_2$ = $P_k$. Термический КПД цикла оценивать без учета подогрева воды в питательном насосе и регенеративной системе.

Задача 2

Построить `график` зависимости термического КПД паротурбинного цикла без промежуточного перегрева пара при следующих параметрах пара:
$P_0$ = 5 MPa, $t_0$ = 450 градусов Цельсия, $P_k$ = 5, 10, 15, 20, 50 kPa. Принять давление за последней ступенью паровой турбины $P_2$ = $P_k$. 
Термический КПД цикла оценивать без учета подогрева воды в питательном насосе и регенеративной системе.

'''

import numpy as np
import matplotlib.pyplot as plt
from iapws import IAPWS97 as gas
import os

MPa = 10 ** 6
kPa = 10 ** 3
unit = 1 / MPa
grad_Cels = 1



"""                 Задача 1    
"""

def kpd(PO,TO,PK):
    
    '''
    функция производит расчет значения термического кпд  
    от параметров РО,ТО,РК, где PO- значение давления,
    TO- значение температуры, Pk- значение давления в конденсаторе
    
    '''
    
    point_0 = gas(P = PO * unit, T = (TO + 273.15))
    point_condenser_inlet = gas(P = (PK * unit) , s = point_0.s)
    point_pump_outlet = gas(P = (PK * unit), x = 0)
    useful_energy = point_0.h - point_condenser_inlet.h
    full_energy = point_0.h - point_pump_outlet.h
    kpd_value = (useful_energy / full_energy) * 100
    return kpd_value

def graf_term_kpd(dPO,dTO,PK):
    
    """
    функциия строит график зависимости термического КПД 
    без промежуточного перегрева пара от параметров dРО,dТО,РК, где dPO- изменяющееся значение давления,
    dTO-изменяющееся значение температуры, Pk- значение давления в конденсаторе
    Дано:
    p01 = np.array([5 * MPa, 10 * MPa, 15 * MPa, 20 * MPa]) # Мега Паскаль
    t01 = np.array([300, 350, 400, 450 ,500]) # Градус Цельсия
    pk1 = 5 * kPa
    
    """
    
    for p0 in dPO:
        KPD = []
        for t0 in dTO:
            kpd_value = kpd(p0, t0, PK)
            KPD.append(kpd_value)
        plt.xlabel("t0, градусы Цельсия")
        plt.ylabel("Термический КПД, %")
        plt.title("График зависимости термического КПД от to")
        plt.plot(dTO,KPD, label = f"При dP0 = {p0 * unit} МПа")
    plt.grid()
    plt.legend()
    # Определяем путь к рабочему столу
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    # Определяем путь к папке "в гитхаб", так называется моя папка с графиками
    folder_name = "в гитхаб"
    folder_path = os.path.join(desktop_path, folder_name)

    # Проверяем, существует ли папка "в гитхаб"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Форматируем путь к файлу
    file_path = os.path.join(folder_path, 'dz1graf1.png')

    # Сохраняем график в указанной папке (это перезапишет файл, если он существует)
    plt.savefig(file_path)
    return plt.show()




"""                 Задача 2
"""

def graf_pk(PO,TO,dPK):
    
    """
    функция строит график зависимости термического КПД от параметров РО,ТО,dРК,где PO- значение давления,
    TO- значение температуры, dPk- изменяющееся значение давления в конденсаторе. KPD- массив КПД
    Дано:
    p02 = 5 * MPa  #мега паскаль
    t02 = 450 #градусы цельсия
    pk2 = np.array([5 * kPa, 10 * kPa, 15 * kPa, 20 * kPa, 50 * kPa]) # Кило Паскаль
    """

    KPD = []
    for PK1 in dPK:
        kpd_value = kpd(PO, TO, PK1)
        KPD.append(kpd_value)
    plt.xlabel("Pk, Па")
    plt.ylabel("Термический КПД, %")
    plt.title("График зависимости термического КПД от Pk")
    plt.plot(dPK,KPD, label = f"При P0 = {PO * unit} (МПа) и температуре t0= {TO} (градус Цельсия)")
    plt.grid()
    plt.legend( loc='upper left')

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    folder_name = "графики Шалыгин"
    folder_path = os.path.join(desktop_path, folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, 'dz1graf2.png')

    plt.savefig(file_path)
    return plt.show()

if __name__ == "__main__":

    """
    Построение графиков из задачи 1 и задачи 2.
    Дано для задачи 1 с индексом 1 и для задачи 2 с индексом 2:
    """
    
    p01 = np.array([5 * MPa, 10 * MPa, 15 * MPa, 20 * MPa]) # Мега Паскаль
    t01 = np.array([300, 350, 400, 450 ,500]) # Градус Цельсия
    pk1 = 5 * kPa

    p02 = 5 * MPa  #мега паскаль
    t02 = 450 #градусы цельсия
    pk2 = np.array([5 * kPa, 10 * kPa, 15 * kPa, 20 * kPa, 50 * kPa]) # Кило Паскаль

    grafik1 = graf_term_kpd(p01, t01, pk1)
    grafik2 = graf_pk(p02, t02, pk2)


