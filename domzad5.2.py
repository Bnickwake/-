'''
Шалыгин Никита ФПэ-01-22

Условие задачи:

Написать автоматизированный поиск коэффициента по оси Y для заданного значения по оси X
для линии 7 в случае наличия пром. перегрева (график с пары).Вывести полученный график коэффициентов.
'''



import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os



def poisk_koef(data):

    '''
    Aвтоматизированный поиск коэффициента с оси Y по данному значению оси Х для линии 7 в случае присутствия пром. перегрева.
    '''
    def polynomial_4(x, a, b, c, d, e):  # , e
        return a * x ** 4 + b * x ** 3 + c * x ** 2 + d * x + e


    def linear(x, m, c):
        return m * x + c


    def piecewise_fit(data, intervals):
        x = data[:, 0]
        y = data[:, 1]

        results = []
        for interval, func in intervals:
            mask = (x >= interval[0]) & (x <= interval[1])
            x_interval = x[mask]
            y_interval = y[mask]

            if func == "polynomial_4":
                params, _ = curve_fit(polynomial_4, x_interval, y_interval)
                results.append((interval, polynomial_4, params))
            elif func == "linear":
                params, _ = curve_fit(linear, x_interval, y_interval)
                results.append((interval, linear, params))
                # print(interval)
        return results


    intervals = [
        ([0.29, 0.634343], "polynomial_4"),
        ([0.634343, 0.644444], "linear"),
        ([0.644444, 0.727273], "polynomial_4"),
        ([0.727273, 0.739394], "linear"),
        ([0.739394, 0.840404], "polynomial_4"),
        ([0.840404, 0.850505], "linear"),
        ([0.850505, 0.953535], "polynomial_4"),
        ([0.953535, 0.959596], "linear")
    ]

    results = piecewise_fit(data, intervals)

    plt.scatter(data[:, 0], data[:, 1], label="Исходные данные", color="black")
    for interval, func, params in results:
        x_fit = np.linspace(interval[0], interval[1], 10000)
        if func == polynomial_4:
            y_fit = polynomial_4(x_fit, *params)
            label = f"Полином 4 степени: {interval}"
        elif func == linear:
            y_fit = linear(x_fit, *params)
            label = f"Прямая: {interval}"
        plt.plot(x_fit, y_fit, label=label)

    plt.legend()

    plt.xlabel(r"$\frac{t_{п.в} - t_{к}}{t'_0 - t_{к}}$, б/р", fontsize=12)
    plt.ylabel(r"$\frac{\xi^{\text{пп}}_p}{(\xi^{\text{пп} \infty}_k)_{\text{max}}}$, б/р", fontsize=12)

    plt.title("Аппроксимация данных графика потерь")

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    folder_name = "графики Шалыгин"
    folder_path = os.path.join(desktop_path, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, 'dz5graf1.png')
    plt.savefig(file_path)

    return plt.show()


data = np.array([
    [0.294949,0.5115],
    [0.30101,0.522031],
    [0.307071,0.531056],
    [0.315152,0.538568],
    [0.321212,0.547593],
    [0.331313,0.55962],
    [0.341414,0.574661],
    [0.351515,0.586688],
    [0.363636,0.595697],
    [0.373737,0.606218],
    [0.387879,0.619742],
    [0.40404,0.63326],
    [0.418182,0.648291],
    [0.428283,0.655798],
    [0.436364,0.664818],
    [0.444444,0.670824],
    [0.452525,0.678336],
    [0.458586,0.684348],
    [0.468687,0.693362],
    [0.474747,0.697866],
    [0.484848,0.703867],
    [0.492929,0.71138],
    [0.50303,0.717381],
    [0.517172,0.726385],
    [0.529293,0.733888],
    [0.539394,0.739889],
    [0.553535,0.747386],
    [0.569697,0.754878],
    [0.579798,0.759373],
    [0.593939,0.763857],
    [0.610101,0.769843],
    [0.618182,0.772836],
    [0.634343,0.777315],
    [0.638384,0.786344],
    [0.640404,0.790859],
    [0.642424,0.793867],
    [0.644444,0.799888],
    [0.650505,0.80138],
    [0.656566,0.802871],
    [0.662626,0.805869],
    [0.668687,0.80736],
    [0.676768,0.808847],
    [0.686869,0.813341],
    [0.69697,0.813316],
    [0.709091,0.814792],
    [0.717172,0.816278],
    [0.727273,0.820773],
    [0.731313,0.828296],
    [0.735354,0.837325],
    [0.737374,0.84184],
    [0.739394,0.847861],
    [0.747475,0.850854],
    [0.759596,0.853837],
    [0.767677,0.856829],
    [0.779798,0.858306],
    [0.79596,0.859772],
    [0.80404,0.859751],
    [0.818182,0.858209],
    [0.828283,0.858184],
    [0.840404,0.858153],
    [0.842424,0.862668],
    [0.846465,0.871698],
    [0.850505,0.880727],
    [0.852525,0.886748],
    [0.858586,0.886733],
    [0.868687,0.883694],
    [0.882828,0.882152],
    [0.90101,0.877587],
    [0.921212,0.873016],
    [0.937374,0.868456],
    [0.953535,0.862389],
    [0.955556,0.865397],
    [0.955556,0.86841],
    [0.955556,0.863891],
    [0.955556,0.866904],
    [0.955556,0.860877],
    [0.957576,0.869912],
    [0.957576,0.875938],
    [0.957576,0.872925],
    [0.957576,0.881965],
    [0.957576,0.878951],
    [0.959596,0.883466],
    ])

if __name__ == "__main__":

    """
    Построение и вывод графика
    """

    koef=poisk_koef(data)




