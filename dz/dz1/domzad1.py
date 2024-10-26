# Шалыгин Никита ФПэ-01-22


import numpy as np
import matplotlib.pyplot as plt
from iapws import IAPWS97 as gas
import os

MPa = 10 ** 6
kPa = 10 ** 3
unit = 1 / MPa
grad_Cels = 1
                  #Задача 1
#функции производят расчет значения термического кпд и строят график зависимости термического КПД 
#без промежуточного перегрева пара от параметров dРО,dТО,РК, где dPO- изменяющееся значение давления,
#dTO-изменяющееся значение температуры, Pk- значение критического давления

def kpd(PO,TO,PK):
        point_0 = gas(P = PO * unit, T = (TO + 273.15))
        point_condenser_inlet = gas(P = (PK * unit) , s = point_0.s)
        point_pump_outlet = gas(P = (PK * unit), x = 0)
        useful_energy = point_0.h - point_condenser_inlet.h
        full_energy = point_0.h - point_pump_outlet.h
        kpd_value = (useful_energy / full_energy) * 100
        return kpd_value

def graf_term_kpd(PO,TO,PK):
    for p0 in PO:
        KPD = []
        for t0 in TO:
            kpd_value = kpd(p0, t0, PK)
            KPD.append(kpd_value)
        plt.xlabel("t0, градусы Цельсия")
        plt.ylabel("Термический КПД, %")
        plt.title("График зависимости термического КПД от to")
        plt.plot(TO,KPD, label = f"При P0 = {p0 * unit} МПа")
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

if __name__ == "__main__":
    #дано
    p0 = np.array([5 * MPa, 10 * MPa, 15 * MPa, 20 * MPa]) # Мега Паскаль
    t0 = np.array([300, 350, 400, 450 ,500]) # Градус Цельсия
    pk = 5 * kPa


#построение графика используя функцию
grafik1 = graf_term_kpd(p0,t0,pk)



                # Задача 2
#функция строит график зависимости термического КПД от параметров РО,ТО,dРК,где PO- значение давления,
#TO- значение температуры, dPk- изменяющееся значение критического давления
def graf_pk(PO,TO,PK):
    # 1) KPD- массив КПД
    KPD = []
    for PK1 in pk:
        kpd_value = kpd(PO, TO, PK1)
        KPD.append(kpd_value)
    plt.xlabel("Pk, Па")
    plt.ylabel("Термический КПД, %")
    plt.title("График зависимости термического КПД от Pk")
    plt.plot(PK,KPD, label = f"При P0 = {PO * unit} (МПа) и температуре t0= {TO} (градус Цельсия)")
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
# Значение давления и темпратуры
    p0 = 5 * MPa  #мега паскаль
    t0 = 450 #градусы цельсия
    pk = np.array([5 * kPa, 10 * kPa, 15 * kPa, 20 * kPa, 50 * kPa]) # Кило Паскаль
  
#построение графика используя функцию
graf22 = graf_pk(p0,t0,pk)


