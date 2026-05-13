import json
import tkinter as tk
from tkinter import ttk

from matplotlib.lines import Line2D
from matplotlib.pyplot import xlabel, ylabel

from pyflowgo import run_flowgo
import pandas
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


template = "./modelisation inverse/template.json"
json_file = template
list_T = []
list_Temp= []
list_C = []
list_P = []

def start_TP():
    with open(json_file) as data_file:
        data = json.load(data_file)
    config=data
    dist = config['runout_dist']
    dist_minus = dist * (1-0.30)
    dist_plus = dist * (1+0.30)
    ax.axvline(dist_minus, alpha = 0.75, color='b')
    colo = ['pink','yellow','black','red','purple','green','cyan']
    for T in range(1100,1205,5):
        for P in range(0,70,10):
            T_temp = T+273.15
            P_temp = P/100
            i = int(P/10)

            config['eruption_condition']['eruption_temperature'] = T_temp
            config['lava_state']['vesicle_fraction'] = P_temp
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
                list_T.append(T)
                list_P.append(P)
                ax.scatter(posi, T, marker='^', edgecolor=colo[i], facecolor=colo[i])
                canvas_fig.draw_idle()
                root.update()
            else:
                ax.scatter(posi,T, marker='^', edgecolor=colo[i], facecolor="None")
                canvas_fig.draw_idle()
                root.update()




def start():

    with open(json_file) as data_file:
        data = json.load(data_file)
        config=data
        dist = config['runout_dist']
        dist_minus = dist * (1-0.30)
        dist_plus = dist * (1+0.30)
        ax.axvline(dist_minus, alpha = 0.75, color='b')
    for T in range(1000,1305,5):

        Temp = T+273.15
        config['eruption_condition']['eruption_temperature'] = Temp
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
            list_T.append(T)
            list_Temp.append(Temp)
            ax.scatter(posi, T, marker='^', color='g', label='Température valide')
            canvas_fig.draw_idle()
            root.update()
        else:
            ax.scatter(posi,T, marker='^', color='r', label='Température invalide')
            canvas_fig.draw_idle()
            root.update()

    if not list_T:
        # texte
        text_T = (f'L\' {int(dist_minus)} – {int(dist_plus)} n\'est pas atteint sur la gamme de température choisi')
        label_T=tk.Label(ini_frame, text=text_T)
        label_T.pack(anchor=tk.W, fill='x')
        root.update()
    else:
        min_T = np.min(list_T)
        max_T = np.max(list_T)
        mean_T = np.mean(list_T)
        med_T = np.median(list_T)

        # texte
        text_T = (f'L\'intervale de distance  est {int(dist_minus)} – {int(dist_plus)} m est atteint  \n\n La gamme de température est de : {min_T}–{max_T} °C \n\n La moyenne est de : {mean_T} °C \n\n La medianne est de : {med_T} °C')
        label_T=tk.Label(ini_frame, text=text_T)
        label_T.pack(anchor=tk.W, fill='x')
        root.update()


    config['lava_state']['eruption_temperature'] = 1387.15

    for C in range(0,45,):
        C_temp = C/100
        config['eruption_condition']['crystal_fraction'] = C_temp
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
            list_C.append(C)
            ax2.scatter(posi, C, marker='d', color='g', label='Cristalinité valide')
            canvas_fig.draw_idle()
            root.update()
        else:
            ax2.scatter(posi,C, marker='d', color='r', label='Cristallinité invalide')
            canvas_fig.draw_idle()
            root.update()

    if not list_C:
        # texte
        text_C = (f'\nL\'intervale de distance est {int(dist_minus)} – {int(dist_plus)} m n\' est pas atteint pour la gamme de cristallinité choisie')
        label_C=tk.Label(ini_frame, text=text_C)
        label_C.pack(anchor=tk.W, fill='x')
        root.update()
    else:
        min_C = np.min(list_C)
        max_C= np.max(list_C)
        mean_C = np.mean(list_C)
        med_C = np.median(list_C)

        # texte
        text_C = (f'\nL\'intervale de distance {int(dist_minus)} – {int(dist_plus)} m est atteint \n\n La gamme de cristalinité est : {min_C}–{max_C} % \n\n La moyenne est de : {mean_C} % \n\n La medianne est de : {med_C} %')
        label_C=tk.Label(ini_frame, text=text_C)
        label_C.pack(anchor=tk.W, fill='x')
        root.update()

    config['lava_state']['crystal_fraction'] = 0.104

    for P in range(0,70):
        P_temp = P/100
        config['lava_state']['vesicle_fraction'] = P_temp
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
            list_P.append(P)
            ax2.scatter(posi, P, marker='o', color='g', label='Porosité valide')
            canvas_fig.draw_idle()
            root.update()
        else:
            ax2.scatter(posi,P, marker='o', color='r', label='Porosité invalide')
            canvas_fig.draw_idle()
            root.update()
    if not list_P:
        # texte
        text_P = (f'\nL\'intervale de distance est {int(dist_minus)} – {int(dist_plus)} m n\' est pas atteint pour la gamme de porosité choisie')
        label_P=tk.Label(ini_frame, text=text_P)
        label_P.pack(anchor='w', fill='x')
        root.update()

    else:
        min_P = np.min(list_P)
        max_P= np.max(list_P)
        mean_P = np.mean(list_P)
        med_P = np.median(list_P)

        # texte
        text_P = (f'\nL\'intervale de distance est valable est {int(dist_minus)} – {int(dist_plus)} m  \n\n La gamme est de : {min_P}–{max_P} °C \n\n La moyenne est de : {mean_P} °C \n\n La medianne est de : {med_P} °C')
        label_P=tk.Label(ini_frame, text=text_P)
        label_P.pack(anchor=tk.W, fill='x')
        root.update()


root = tk.Tk()
root.title("modélisation inverse: Pyflowgo")
root.geometry('1500x1000')

#frame
frame = tk.Frame(root)
frame.pack(fill="both", expand=1)

#canva
canvas = tk.Canvas(frame)
canvas.pack(fill="both",expand=1)

#roulette
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

#config canva
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

#second frame
frame_2 = tk.Frame(canvas)

#window in canvas
canvas.create_window((0,0), window=frame_2, anchor="nw")

#fig matplot
legend_elements=[Line2D([0], [0], marker='^', color='g', label='Température valide',
                        markerfacecolor='g', markersize=7.5, linestyle='None'),
                 Line2D([0], [0], marker='^', color='r', label='Température invalide',
                        markerfacecolor='r', markersize=7.5, linestyle='None'),
                 Line2D([0], [0], marker='d', color='g', label='Cristallinité valide',
                        markerfacecolor='g', markersize=7.5, linestyle='None'),
                 Line2D([0], [0], marker='d', color='r', label='Cristallinité invalide',
                        markerfacecolor='r', markersize=7.5, linestyle='None'),
                 Line2D([0], [0], marker='o', color='g', label='Porosité valide',
                        markerfacecolor='g', markersize=7.5, linestyle='None'),
                 Line2D([0], [0], marker='o', color='r', label='Porosité invalise',
                        markerfacecolor='r', markersize=7.5, linestyle='None'),]

gr = (1 + np.sqrt(5))/2
sc = 2

fig_w = 3 * gr * sc
fig_h = 3 * sc
fig = plt.figure(figsize=(fig_w,fig_h))

panel_w = 1/sc +0.15
panel_h = 1/sc +0.3
off = (1- 1/sc)/2
ax = fig.add_axes([off-0.175, off-0.15, panel_w, panel_h])
ax2 = ax.twinx()
ax.set_xlabel('Distance de l\'évent en m')
ax.set_ylabel('Température en °C')
ax2.set_ylabel('Pourcentage en %')
fig.legend(handles=legend_elements, bbox_to_anchor=(1,1))
plt.figure(figsize=(2,2))
canvas_fig = FigureCanvasTkAgg(fig, master=frame_2)
canvas_fig.draw()
canvas_fig.get_tk_widget().pack(fill="x", expand=1, anchor='nw')

#label frame
ini_frame = tk.LabelFrame(frame_2, padx=5, pady=5)
ini_frame.pack(anchor='w', fill="x", pady=5)

# start button
button_T = tk.Button(frame_2, command=start, text='Start')
button_T.pack()

button = tk.Button(frame_2, command=start_TP, text='Start TP')
button.pack()



root.mainloop()
