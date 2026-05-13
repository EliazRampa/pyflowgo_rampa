import json
import time
import tkinter as tk
from matplotlib import patches
import numpy as np
import pandas
from matplotlib import pyplot as plt
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.lines import Line2D

from pyflowgo import run_flowgo

json_file = "./modelisation inverse/template.json"
csv = "./modelisation inverse/profile_list.csv"
TC_dict = {}
values = []
list_cle = []
T_plus = 1175
T_minus = 1120

list_C = []
erupdf = pandas.read_csv(csv, sep=';')
for j in range(0,len(erupdf)):
    value = erupdf.at[erupdf.index[j], 'eruption']
    values.append(str(value))
    for value in values:
        gr = (1 + np.sqrt(5))/2
        sc = 2

        fig_w = 3 * gr * sc
        fig_h = 3 * sc
        fig = plt.figure(figsize=(fig_w,fig_h))

        panel_w = 1/sc +0.15
        panel_h = 1/sc +0.3
        off = (1- 1/sc)/2
        ax = fig.add_axes([off-0.175, off-0.15, panel_w, panel_h])

        ax.set_xlabel('Distance de l\'évent en m')
        ax.set_ylabel('Température en °C')
        legend_elements=[
            Line2D([0], [0], marker='d', color='gray', label='TC',
                   markerfacecolor='r', markersize=7.5, linestyle='None'),
            Line2D([0], [0], marker='s', color='pink', label='0%',
                   markerfacecolor='pink', markersize=7.5, linestyle='None'),
            Line2D([0], [0], marker='s', color='yellow', label='10%',
                   markerfacecolor='yellow', markersize=7.5, linestyle='None'),
            Line2D([0], [0], marker='s', color='black', label='20%',
                   markerfacecolor='black', markersize=7.5, linestyle='None'),
            Line2D([0], [0], marker='s', color='red', label='30%',
                   markerfacecolor='red', markersize=7.5, linestyle='None'),
            Line2D([0], [0], marker='s', color='purple', label='40%',
                   markerfacecolor='purple', markersize=7.5, linestyle='None'),
            Line2D([0], [0], marker='s', color='green', label='50%',
                   markerfacecolor='green', markersize=7.5, linestyle='None'),
            Line2D([0], [0], marker='s', color='cyan', label='60%',
                   markerfacecolor='cyan', markersize=7.5, linestyle='None'),
            Line2D([0], [0], color='b', label='limites de l\'interval', linestyle='-')]
        fig.legend(handles=legend_elements, bbox_to_anchor=(1,1))
        with open(json_file) as data_file:
            data = json.load(data_file)
            indice = values.index(value)
            slope = f'./modelisation inverse/slopes/profile_{value}.txt'
            erup_dist = erupdf.at[erupdf.index[indice],'distance']
            TADR = erupdf.at[erupdf.index[indice],'TADR']
            data['slope_file']= slope
            data['runout_dist']=erup_dist
            data['effusion_rate_init'] = TADR
            with open("./modelisation inverse/template.json", "w") as f:
                json.dump(data, f)

            with open(json_file) as data_file:
                data = json.load(data_file)
                config=data
            dist = config['runout_dist']
            dist_minus = dist * (1-0.30)
            dist_plus = dist * (1+0.30)
            ax.axvline(dist_minus, alpha = 0.75, color='b')
            ax.axvline(dist_plus, alpha = 0.75, color='b')
            colo = ['pink','yellow','black','red','purple','green','cyan']

            for T in range(1100,1205,5):
                for C in range(0,70,10):
                    T_temp = T+273.15
                    C_temp = C/100
                    i = int(C/10)

                    config['eruption_condition']['eruption_temperature'] = T_temp
                    config['lava_state']['crystal_fraction'] = C_temp
                    with open("./modelisation inverse/config.json", "w") as f:
                        json.dump(config, f)

                    result_path = f'./modelisation inverse/results'
                    config_path = "./modelisation inverse/config.json"
                    flowgo = run_flowgo.RunFlowgo()
                    flowgo.run(config_path, result_path)
                    filename = flowgo.get_file_name_results(result_path, config_path)

                    df = pandas.read_csv(filename)
                    posi = df.at[df.index[-1], 'position']

                    if posi >= dist_minus and posi <= dist_plus:
                        cle = T
                        list_C.append(C)
                        # ax.scatter(posi, T, marker='d', edgecolor=colo[i], facecolor=colo[i])
                        # plt.draw()

                    else:
                        pass
                        # ax.scatter(posi,T, marker='d', edgecolor=colo[i], facecolor="None")
                        # plt.draw()
                        # plt.pause(0.5)
                if cle == T:
                    TC_dict[cle] = list_C
                    list_C = []
            lim_T_plus = TC_dict[T_plus]
            lim_T_min = TC_dict[T_minus]
            if len(lim_T_min) == len(lim_T_plus):
                max = max(lim_T_plus)
                min = min(lim_T_plus)
                width = max-min
                heigth = T_plus-T_minus
                ax.plot(patches.Rectangle([T_minus,min], width,heigth))
            else:
                min = min(lim_T_min)
                max = max(lim_T_plus)
                width = max-min
                heigth = T_plus-T_minus
                ax.plot(patches.Rectangle([T_minus,min], width,heigth))

            plt.savefig(f'./modelisation inverse/results/{value}_TC.png')
            plt.pause(1)

plt.show()