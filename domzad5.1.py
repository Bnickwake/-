"""
Шалыгин Никита ФПэ-01-22

Условие задачи:

Оценить расходы в цилиндре высокого давления и в конденсаторе турбины без промежуточного перегрева пара.

Заданные параметры:

Номинальная электрическая мощность: 250 МВт
Начальное давление свежего пара: 23.5 МПа
Начальная температура свежено пара: 540 C
Конечное давление пара: 6.9 кПа
Температура питательной воды: 263 C
Число отборов: 8
Механическое КПД: 99.2%
КПД Электрогенератора: 99%

"""
import iapws
from iapws import IAPWS97 as gas
import os

MPa = 10 ** 6
kPa = 10 ** 3
MBt = 10 ** 6
unit = 1 / MPa
to_kelvin = lambda x: x + 273.15 if x else None




def ocenka_rashodov(electrical_power,p_0,t_0,p_k,z,t_feed_water,p_feed_water,t_nas_0,mechanical_efficiency
    ,generator_efficiency,internal_efficiency):
    """
    Функция приводит оценочное значение расхода в цилиндре высокого давления
    и в конденсаторе турбины без промежуточного переграва пара.
    """
    # Определение параметров точек цикла,необходимые для расчета
    delta_CVD = 0.05 * p_0
    real_p_0 = p_0 - delta_CVD
    teor_point_0 = gas(P = p_0 * unit, T=to_kelvin(t_0))
    point_0 = gas(P=real_p_0 * unit, h=teor_point_0.h)
    point_feed_water = gas(P=p_feed_water * unit, T=to_kelvin(t_feed_water))
    point_k_kip_water = gas(P=p_k * unit, x=0)
    teor_point_k = gas(P=p_k * unit, s = teor_point_0.s)
    heat_drop_i = ( teor_point_0.h - teor_point_k.h) * internal_efficiency
    h_k = teor_point_0.h - heat_drop_i
    point_k = gas(P = p_k * unit, h = h_k)

    # Расчет относительного КПД ЦВД
    efficiency_oi = (teor_point_0.h - point_k.h)/(teor_point_0.h - teor_point_k.h)
    print("efficiency_oi =", efficiency_oi)

    # Расчет коэфициетна кси с бесконечным числом отборов
    numenator_without = point_k.T * (teor_point_0.s - point_k_kip_water.s)
    denumenator_without = teor_point_0.h - point_k_kip_water.h
    without_part = 1 - (numenator_without/denumenator_without)
    numenator_infinity = point_k.T * (teor_point_0.s - point_feed_water.s)
    denumenator_infinity =  teor_point_0.h - point_feed_water.h
    infinity_part = 1 - (numenator_infinity / denumenator_infinity)
    ksi_infinity = 1 - (without_part / infinity_part)
    print('ksi_infinity =',ksi_infinity)

    # "x" -----> ((t_пв__t_k)(t_nas_0__t_k))
    x = (point_feed_water.T - point_k.T) / (to_kelvin(t_nas_0) - point_k.T)
    print('x =', x)

    # Расчет коэфициетна кси с 7 числом отборов
    ksi = 0.86 * ksi_infinity
    print('ksi =',ksi)

    eff_num = (teor_point_0.h - teor_point_k.h) * internal_efficiency
    eff_denum =  teor_point_0.h - point_k_kip_water.h
    efficiency = (eff_num / eff_denum) * (1 + ksi)
    print('efficiency =',efficiency)
    print('eff_num =',eff_num)
    print('eff_denum =', eff_denum)

    estimated_heat_drop = efficiency * (teor_point_0.h - point_feed_water.h)
    print('estimated_heat_drop =',estimated_heat_drop)

    inlet_mass_flow = electrical_power / (estimated_heat_drop * 1000 * mechanical_efficiency * generator_efficiency)

    mass_flow_denum = 1000 * (point_k.h - point_k_kip_water.h) * mechanical_efficiency * generator_efficiency
    mass_flow_factor = (1/efficiency) - 1
    condenser_mass_flow = (electrical_power * mass_flow_factor)/mass_flow_denum

    return inlet_mass_flow, condenser_mass_flow

'''
Дано:
'''
electrical_power = 250 * MBt
p_0 = 23.5 * MPa
t_0 = 540
p_k = 6.9 * kPa
z = 7
t_feed_water = 263
p_feed_water = 1.35 * p_0 #  рпв=(1,33-1,35)р0 при сверхкритических параметрах свежего пара.
t_nas_0 = 374.2 #– температура насыщения при давлении свежего пара р0 (при сверхкритическом давлении принять =374,2 С)
mechanical_efficiency = 0.992
generator_efficiency = 0.99
internal_efficiency = 0.85

if __name__ == "__main__":
    '''
    Вывод значений расходов в цилиндре высокого давления и в конденсаторе турбины без промежуточного перегрева пара.
    '''

    mass_flow = ocenka_rashodov(electrical_power,p_0,t_0,p_k,z,t_feed_water,p_feed_water,t_nas_0,mechanical_efficiency
        ,generator_efficiency,internal_efficiency)


    print("Массовый расход в турбину на входе", mass_flow[0])

    print("Массовый расход в конденсаторe:", mass_flow[1])








