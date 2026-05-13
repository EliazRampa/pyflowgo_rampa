import random
import tkinter as tk
from cProfile import label

import numpy as np
import playsound3
from matplotlib import pyplot as plt
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle

def launch():
    legend = []
    root = tk.Tk()
    root.title('Pyflowgo: graph cycle')
    root.geometry("1500x1000")

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
    ax.set_xlabel('Cristallinité en %')
    ax.set_ylabel('Température en °C')
    ax.set_ylim(1100,1200)
    ax.set_xlim(-5,100)
    canvas_fig = FigureCanvasTkAgg(fig, master=frame)
    toolbar = NavigationToolbar2Tk(canvas_fig, frame, pack_toolbar=False)
    toolbar.update()

    entry_Tmax = tk.Entry(frame)

    entry_Tmin = tk.Entry(frame)

    entry_Cmax = tk.Entry(frame)

    entry_Cmin = tk.Entry(frame)
    entry_label = tk.Entry(frame)

    def draw():
        T_max = int(entry_Tmax.get())
        T_min = int(entry_Tmin.get())
        C_max = int(entry_Cmax.get())
        C_min = int(entry_Cmin.get())
        label = str(entry_label.get())

        color = (random.random(), random.random(), random.random())

        coor = (C_min, T_min)
        h = T_max-T_min
        w = C_max-C_min
        print(coor)
        print(type(coor))
        ax.add_patch(Rectangle(coor, width=w, facecolor='none', edgecolor=color, height=h, linewidth=1))
        legend.append(Rectangle(coor, width=w, facecolor='none', edgecolor=color, height=h, linewidth=1, label=label))
        fig.legend(handles=legend, loc='upper right')
        canvas_fig.draw_idle()
        root.update()
        playsound3.playsound('./modelisation inverse/ding.mp3')

    canvas.pack(fill='both', expand=1)
    canvas.create_window(0,0, window=frame, anchor='nw')
    button_draw = tk.Button(frame, text='DRAW', command=draw)
    label_label = tk.Label(frame, text='Éruption')
    label_label.pack()
    entry_label.pack()
    canvas_fig.draw()
    canvas_fig.get_tk_widget().pack()
    toolbar.pack()
    label1 = tk.Label(frame,text='Température max')
    label1.pack(side='left', anchor='n')
    entry_Tmax.pack(side='left', anchor='s')
    label2 = tk.Label(frame,text='Température min')
    label2.pack(side='left', anchor='n')
    entry_Tmin.pack(side='left', anchor='s')
    label3 = tk.Label(frame,text='Cristallinité max')
    label3.pack(side='left', anchor='n')
    entry_Cmax.pack(side='left', anchor='s')
    label4 = tk.Label(frame,text='Cristallinité min')
    label4.pack(side='left', anchor='n')
    entry_Cmin.pack(side='left', anchor='s')
    button_draw.pack(side='left', anchor='s')

    root.mainloop()
launch()