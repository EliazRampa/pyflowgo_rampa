import json
import time
import tkinter as tk
from tkinter import ttk
import numpy as np
import pandas
from matplotlib import pyplot as plt
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.lines import Line2D
from matplotlib.pyplot import twinx
import playsound3
from pyflowgo import run_flowgo


class TreeViewFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.hscrollbar = ttk.Scrollbar(self, orient='horizontal')
        self.vscrollbar = ttk.Scrollbar(self, orient='vertical')
        self.treeview = ttk.Treeview(
            self,
            xscrollcommand=self.hscrollbar.set,
            yscrollcommand=self.vscrollbar.set
        )
        self.hscrollbar.config(command=self.treeview.xview)
        self.hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.vscrollbar.config(command=self.treeview.yview)
        self.vscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.treeview.pack()

## Window parameters ###
root = tk.Tk()
root.title('Pyflowgo: Modélisation inverse graph')
root.geometry("1000x1000")

canvas = tk.Canvas(root)
frame = tk.Frame(canvas)

gr = (1 + np.sqrt(5))/2
sc = 2

fig_w = 3 * gr * sc
fig_h = 3 * sc
fig = plt.figure(figsize=(fig_w,fig_h))

panel_w = 1/sc +0.15
panel_h = 1/sc +0.3
off = (1- 1/sc)/2
ax = fig.add_axes([off-0.175, off-0.15, panel_w, panel_h])
#ax2 = twinx(ax)
canvas_fig = FigureCanvasTkAgg(fig, master=frame)

## code parameter ####
MODE = 'NONE'
csv = "./modelisation inverse/profile_list.csv"
template = "./modelisation inverse/template.json"
json_file = template
values = []
list_T = []
list_C = []
list_P = []
cle = 0
TP_dict = {}
TC_dict = {}
PC_dict = {}



def decorate(MODE):

    if MODE == 'mono':
        ax.set_xlabel('Distance de l\'évent en m')
        ax.set_ylabel('Température en °C')
        #ax2.set_ylabel('Pourcentage en %')
        #ax2.set_ylim(0,80)
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
                                markerfacecolor='r', markersize=7.5, linestyle='None'),
                         Line2D([0], [0], color='b', label='limites de l\'interval', linestyle='-')]
        fig.legend(handles=legend_elements, loc='upper right')
    elif MODE == 'duo':
        ax.set_xlabel('Distance de l\'évent en m')
        ax.set_ylabel('Température en °C')
        #fig.title('Distance en fonction Variation de la Température et de la Cristalinité à la porosité fixé à 30 % ')
        legend_elements=[#Line2D([0], [0], marker='^', color='gray', label='TP',
                               # markerfacecolor='g', markersize=7.5, linestyle='None'),
                         Line2D([0], [0], marker='d', color='gray', label='valide',
                                markerfacecolor='r', markersize=7.5, linestyle='None'),
                         Line2D([0], [0], marker='d', color='gray', label='invalide',
                                markerfacecolor='None', markersize=7.5, linestyle='None'),
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
                         Line2D([0], [0], color='b', label='front de l\'event', linestyle='--')]
        fig.legend(handles=legend_elements, bbox_to_anchor=(1,1))
    elif MODE == 'multi':
        legend_elements=[Line2D([0], [0], marker='x', color='g', label='groupe valide',
                                markerfacecolor='g', markersize=7.5, linestyle='None'),
                         Line2D([0], [0], marker='x', color='r', label='groupe invalide',
                                markerfacecolor='r', markersize=7.5, linestyle='None'),
                         Line2D([0], [0], color='b', label='limites de l\'interval', linestyle='-')]
        fig.legend(handles=legend_elements, bbox_to_anchor=(1,1))
    else:
        pass


def createWindow():
    erupdf = pandas.read_csv(csv, sep=';')
    for j in range(0,len(erupdf)):
        value = erupdf.at[erupdf.index[j], 'eruption']
        values.append(str(value))

    choicesvar = tk.StringVar()
    box = ttk.Combobox(frame, textvariable=choicesvar, width=25)
    box['values'] = values

    choicesvar = tk.StringVar()
    box_para = ttk.Combobox(frame, textvariable=choicesvar, width=25, )
    box_para['values'] = ['TP', 'TC', 'PC']

    var_button = tk.IntVar()
    checkbutton = tk.Checkbutton(root, text="loop through all", variable=var_button,
                             onvalue=1, offvalue=0)

    def selectProfile():
        profil = box.get()
        indice = values.index(profil)
        with open(json_file) as data_file:
            data = json.load(data_file)
        slope = f'./modelisation inverse/slopes/profile_{profil}.txt'
        erup_dist = erupdf.at[erupdf.index[indice],'distance']
        TADR = erupdf.at[erupdf.index[indice],'TADR']
        data['slope_file']= slope
        data['runout_dist']=erup_dist
        data['effusion_rate_init'] = TADR
        with open("./modelisation inverse/template.json", "w") as f:
            json.dump(data, f, indent=4)

    def start_full():
        list_T = []
        list_C = []
        list_P = []
        MODE = 'multi'
        decorate(MODE)
        profil = box.get()
        fortree = tk.Toplevel()
        fortree.title('Tableaux des résultats')
        tree = TreeViewFrame(fortree)
        tree.pack()
        tree.treeview.config(columns=("temp", "poro","crist"), show='headings')
        tree.treeview.heading("temp", text='Température en °C')
        tree.treeview.heading("poro", text='Porosité en %')
        tree.treeview.heading("crist", text='Cristallinité en %')

        with open(json_file) as data_file:
            data = json.load(data_file)
        config=data
        dist = config['runout_dist']
        dist_minus = dist * (1-0.30)
        dist_plus = dist * (1+0.30)
        ax.axvline(dist_minus, alpha = 0.75, color='b')
        ax.axvline(dist_plus, alpha = 0.75, color='b')

        for T in range(1100,1205,5):
            for P in range(0,70,10):
                for C in range(0,45,5):
                    Temp = T+273.15
                    P_temp = P/100
                    C_temp  = C/100

                    config['eruption_condition']['eruption_temperature'] = Temp
                    config['lava_state']['vesicle_fraction'] = P_temp
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
                        list_T.append(T)
                        list_P.append(P)
                        list_C.append(C)
                        i = tree.treeview.insert("",tk.END, values=(T,P,C))
                        tree.treeview.see(i)
                        ax.scatter(posi, T, marker='x', color='g')
                        canvas_fig.draw_idle()
                        root.update()
                        fortree.update()
                    else:
                        ax.scatter(posi,T, marker='x', color='r')
                        canvas_fig.draw_idle()
                        root.update()
        plt.savefig(f'./modelisation inverse/results/{profil}_multi.png')
        time.sleep(20)
        multi = {"Température": list_T, "Porosité":list_P, "Cristallinité":list_C}
        result = pandas.DataFrame(multi)
        result.to_csv(f'./modelisation inverse/results/{profil}_multi.csv', index=False)

    def start_mono():
        list_T = []
        list_C = []
        list_P = []
        MODE = 'mono'
        decorate(MODE)
        value = box.get()
        window = tk.Toplevel(root)
        window.title('Pyflowgo: Modélisation inverse résultats mono paramètre')
        ini_frame = tk.LabelFrame(window, padx=10, pady=10)
        ini_frame.pack(anchor='w', fill="x", pady=10)
        with open(json_file) as data_file:
            data = json.load(data_file)
            config=data
            dist = config['runout_dist']
            dist_minus = dist * (1-0.30)
            dist_plus = dist * (1+0.30)
            ax.axvline(dist_minus, alpha = 0.75, color='b')
            ax.axvline(dist_plus, alpha = 0.75, color='b')

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
            label_T.pack(anchor='w', fill='x')
            window.update()
            root.update()
        else:
            min_T = np.min(list_T)
            max_T = np.max(list_T)
            mean_T = np.mean(list_T)
            med_T = np.median(list_T)

            # texte
            text_T = (f'L\'intervale de distance  est {int(dist_minus)} – {int(dist_plus)} m est atteint  \n\n La gamme de température est de : {min_T}–{max_T} °C \n\n La moyenne est de : {mean_T} °C \n\n La medianne est de : {med_T} °C')
            label_T=tk.Label(ini_frame, text=text_T)
            label_T.pack(anchor='w', fill='x')
            window.update()
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
                #ax2.scatter(posi, C, marker='d', color='g', label='Cristalinité valide')
                canvas_fig.draw_idle()
                root.update()
            else:
                #ax2.scatter(posi,C, marker='d', color='r', label='Cristallinité invalide')
                canvas_fig.draw_idle()
                root.update()

        if not list_C:
            # texte
            text_C = (f'\nL\'intervale de distance est {int(dist_minus)} – {int(dist_plus)} m n\' est pas atteint pour la gamme de cristallinité choisie')
            label_C=tk.Label(ini_frame, text=text_C)
            label_C.pack(anchor='w', fill='x')
            window.update()
            root.update()
        else:
            min_C = np.min(list_C)
            max_C= np.max(list_C)
            mean_C = np.mean(list_C)
            med_C = np.median(list_C)

            # texte
            text_C = (f'\nL\'intervale de distance {int(dist_minus)} – {int(dist_plus)} m est atteint \n\n La gamme de cristalinité est : {min_C}–{max_C} % \n\n La moyenne est de : {mean_C} % \n\n La medianne est de : {med_C} %')
            label_C=tk.Label(ini_frame, text=text_C)
            label_C.pack(anchor='w', fill='x')
            window.update()
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
                #ax2.scatter(posi, P, marker='o', color='g', label='Porosité valide')
                canvas_fig.draw_idle()
                root.update()
            else:
                #ax2.scatter(posi,P, marker='o', color='r', label='Porosité invalide')
                canvas_fig.draw_idle()
                root.update()
        if not list_P:
            # texte
            text_P = (f'\nL\'intervale de distance est {int(dist_minus)} – {int(dist_plus)} m n\' est pas atteint pour la gamme de porosité choisie')
            label_P=tk.Label(ini_frame, text=text_P)
            label_P.pack(anchor='w', fill='x')
            window.update()
            root.update()


        else:
            min_P = np.min(list_P)
            max_P= np.max(list_P)
            mean_P = np.mean(list_P)
            med_P = np.median(list_P)

            # texte
            text_P = (f'\nL\'intervale de distance est valable est {int(dist_minus)} – {int(dist_plus)} m  \n\n La gamme est de : {min_P}–{max_P} °C \n\n La moyenne est de : {mean_P} °C \n\n La medianne est de : {med_P} °C')
            label_P=tk.Label(ini_frame, text=text_P)
            label_P.pack(anchor='w', fill='x')
            window.update()
            root.update()
        plt.savefig(f'./modelisation inverse/results/{value}_mono.png')
        time.sleep(20)



    def start_couple():
        if var_button.get == 1:
            para = box_para.get()
            for value in values:
                with open(json_file) as data_file:
                    data = json.load(data_file)
                slope = f'./modelisation inverse/slopes/profile_{value}.txt'
                indice = values.index(value)
                erup_dist = erupdf.at[erupdf.index[indice],'distance']
                TADR = erupdf.at[erupdf.index[indice],'TADR']
                data['slope_file']= slope
                data['runout_dist']=erup_dist
                data['effusion_rate_init'] = TADR
                with open("./modelisation inverse/template.json", "w") as f:
                    json.dump(data, f)
                cle = 0
                list_T = []
                list_C = []
                list_P = []

                MODE = 'duo'
                decorate(MODE)
                with open(json_file) as data_file:
                    data = json.load(data_file)
                config=data
                dist = config['runout_dist']
                dist_minus = dist * (1-0.30)
                dist_plus = dist * (1+0.30)
                ax.axvline(dist, alpha = 0.5, color='b', linesryle = '---')
                ax.axhline(1120, alpha = 0.5, color='b', linestyle='--')
                ax.axhline(1175, alpha = 0.5, color='b', linestyle='--')
                colo = ['pink','yellow','black','red','purple','green','cyan']
                if para == 'TP':
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
                                cle = T
                                list_P.append(P)
                                ax.scatter(posi, T, marker='^', edgecolor=colo[i], facecolor=colo[i])
                                canvas_fig.draw_idle()
                                root.update()
                            else:
                                cle = cle
                                ax.scatter(posi,T, marker='^', edgecolor=colo[i], facecolor="None")
                                canvas_fig.draw_idle()
                                root.update()
                        if cle == T:
                            TP_dict[cle] = list_P
                            list_P = []

                    plt.savefig(f'./modelisation inverse/results/{value}_TP.png')
                    time.sleep(20)

                #decorate(MODE)
                #config['lava_state']['vesicle_fraction'] = 0.3
                if para == 'TC':
                    for T in range(1100,1205,5):
                        for C in range(0,70,10):
                            T_temp = T+273.15
                            C_temp = C/100
                            i = int(C/10)

                            config['eruption_condition']['eruption_temperature'] = T_temp
                            config['lava_state']['crystal_fraction'] = C_temp
                            with open("./modelisation inverse/config.json", "w") as f:
                                json.dump(config, f, indent=4)

                            result_path = f'./modelisation inverse/results 2'
                            config_path = "./modelisation inverse/config.json"
                            flowgo = run_flowgo.RunFlowgo()
                            flowgo.run(config_path, result_path)
                            filename = flowgo.get_file_name_results(result_path, config_path)

                            df = pandas.read_csv(filename)
                            posi = df.at[df.index[-1], 'position']
                            posi_plus = (posi * 1.3)
                            posi_minus = (posi * 0.70)
                            err_plus =  posi_plus - posi
                            err_minus = posi - posi_minus
                            if dist >= posi_minus and dist <= posi_plus:
                                cle = T
                                list_C.append(C)
                                marker, cap, bar = ax.errorbar(posi, T, xerr=(err_minus, err_plus), marker='d', mfc=colo[i], mec=colo[i], ecolor=colo[i], capsize = 2)
                                bar.set_alpha(0.5)
                            else:
                                ax.scatter(posi, T, marker='d', mfc='None', mec=colo[i])
                        #if cle == T:
                            #TC_dict[cle]=list_C
                    list_C = []
                    plt.savefig(f'./modelisation inverse/results 2/{value}_TC_V2_.png')
                    time.sleep(5)
                    ax.clear()

                #decorate(MODE)
                #config['lava_state']['eruption_temperature'] = 1387.15
                #list_C =[]

                if para == 'PC':
                    for P in range(0,70,10):
                        for C in range(0,70,10):
                            P_temp = P/100
                            C_temp = C/100
                            i = int(C/10)

                            config['lava_state']['vesicle_fraction'] = P_temp
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
                                cle = P
                                list_C.append(C)
                                #ax2.scatter(posi, P, marker='o', edgecolor=colo[i], facecolor=colo[i])
                                canvas_fig.draw_idle()
                                root.update()
                            else:
                                #ax2.scatter(posi,P, marker='o', edgecolor=colo[i], facecolor="None")
                                canvas_fig.draw_idle()
                                root.update()
                        if cle ==P:
                            PC_dict[cle] = list_C
                            list_C=[]

                    plt.savefig(f'./modelisation inverse/results/{value}_PC.png')

        else:
            para = box_para.get()
            cle = 0
            list_T = []
            list_C = []
            list_P = []
            MODE = 'duo'
            decorate(MODE)
            value = box.get()
            with open(json_file) as data_file:
                data = json.load(data_file)
            config=data
            dist = config['runout_dist']
            dist_minus = dist * (1-0.30)
            dist_plus = dist * (1+0.30)
            ax.axvline(dist, alpha = 0.5, color='b', linestyle = '--')
            ax.axhline(1120, alpha = 0.5, color='b', linestyle='--')
            ax.axhline(1175, alpha = 0.5, color='b', linestyle='--')
            colo = ['pink','yellow','black','red','purple','green','cyan']
            if para == 'TP':
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
                            cle = T
                            list_P.append(P)
                            ax.scatter(posi, T, marker='^', edgecolor=colo[i], facecolor=colo[i])
                            canvas_fig.draw_idle()
                            root.update()
                        else:
                            cle = cle
                            ax.scatter(posi,T, marker='^', edgecolor=colo[i], facecolor="None")
                            canvas_fig.draw_idle()
                            root.update()
                    if cle == T:
                        TP_dict[cle] = list_P
                        list_P = []

                plt.savefig(f'./modelisation inverse/results/{value}_TP.png')
                time.sleep(20)

            #decorate(MODE)
            #config['lava_state']['vesicle_fraction'] = 0.3
            if para == 'TC':
                for T in range(1110,1185,5):
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
                        posi_plus = (posi * 1.3)
                        posi_minus = (posi * 0.70)
                        error = (1.3*posi) - posi
                        if dist >= posi_minus and dist <= posi_plus:
                            cle = T
                            list_C.append(C)
                            plt.errorbar(posi, T, xerr=error, marker='d', mfc=colo[i], mec=colo[i], ecolor=colo[i])
                            canvas_fig.draw()
                            root.update()
                        else:
                            ax.scatter(posi, T, marker='d', facecolor='None', edgecolors=colo[i])
                            canvas_fig.draw()
                            root.update()

                    if cle == T:
                        TC_dict[cle]=list_C
                        list_C = []
                plt.savefig(f'./modelisation inverse/results/{value}_TC_V2.png')
                time.sleep(0.5)
                ax.clear()
                playsound3.playsound('./modelisation inverse/ding.mp3')
            #decorate(MODE)
            #config['lava_state']['eruption_temperature'] = 1387.15
            #list_C =[]

            if para == 'PC':
                for P in range(0,70,10):
                    for C in range(0,70,10):
                        P_temp = P/100
                        C_temp = C/100
                        i = int(C/10)

                        config['lava_state']['vesicle_fraction'] = P_temp
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

                        if posi >= dist_minus:
                            cle = P
                            list_C.append(C)
                            #ax2.scatter(posi, P, marker='o', edgecolor=colo[i], facecolor=colo[i])
                            canvas_fig.draw_idle()
                            root.update()
                        else:
                            #ax2.scatter(posi,P, marker='o', edgecolor=colo[i], facecolor="None")
                            canvas_fig.draw_idle()
                            root.update()
                    if cle ==P:
                        PC_dict[cle] = list_C
                        list_C=[]

                plt.savefig(f'./modelisation inverse/results/{value}_PC.png')
                time.sleep(20)


    label_erupt = tk.Label(frame, text='Sélectionné l\'éruption à tester')
    label = tk.Label(frame, text='Séléctioné le test que vous voulez réalisé: ')
    button_couple = tk.Button(frame, command=start_couple, text='Couple de paramètre')
    button_profil = tk.Button(frame, command=selectProfile, text='Sélectionné')
    button_T = tk.Button(frame, command=start_mono, text='Mono paramètre')
    button_full = tk.Button(frame, command=start_full, text='multiparamètre')


    canvas.pack(fill='both', expand=1)
    canvas.create_window(0,0, window=frame, anchor='nw')
    label_erupt.pack()
    box.pack()
    button_profil.pack()
    checkbutton.pack()
    canvas_fig.draw()
    canvas_fig.get_tk_widget().pack(anchor='w', expand=1)
    toolbar = NavigationToolbar2Tk(canvas_fig, frame, pack_toolbar=False)
    toolbar.update()
    toolbar.pack()
    label.pack(side='left')
    button_T.pack(side='left')
    box_para.pack(side='left')
    button_couple.pack(side='left')
    button_full.pack(side='left')
    root.mainloop()


createWindow()

