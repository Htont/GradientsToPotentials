import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
import tkinter.filedialog as fd
import matplotlib.patheffects as path_effects

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

import os

#initial diretory
init_dir = os.getcwd()
f_points = "points.txt"
f_dU = "dU.txt"
f_pols = "pols.txt"

# Create window
win = tk.Tk()
win.title('Graph test')

# Create map
fig = Figure(#figsize = (5, 5),
                 dpi = 100)

ax = fig.add_subplot(111)

# make graph to fill all space
ax.set_position([0,0,1,1])
fig.set_layout_engine(layout="none")

# prepare axis ticks
ax.axis('equal')
ax.tick_params(axis="y",direction="in", pad=-15)
ax.tick_params(axis="x",direction="in", pad=-15)
plt.setp(ax.get_yticklabels(), va="center", rotation=90)
ax.ticklabel_format(axis="both", useOffset=False, style="plain")
ax.margins(0.1)

# Add left panel
panel_w = 150
panel = tk.Frame(win, width=panel_w, bg="#F0F0F0", bd=0, relief=tk.FLAT)
panel.pack(fill="y", side="left", expand=False)

def show_points():
    global ax
    global w_name
    global x
    global y
    ax.clear()
    # Read wells coords
    wells = pd.read_csv(f_points, sep="\t", header=0)
    w_name = wells.iloc[:, 0]
    x = wells.iloc[:, 1]
    y = wells.iloc[:, 2]
    
    # Draw wells
    ax.scatter(x, y, color="black")
    
    plt.setp(ax.get_yticklabels(), va="center", rotation=90)
    ax.ticklabel_format(axis="both", useOffset=False, style="plain")
    ax.margins(0.1)

    for i in range(len(w_name)):
        text = ax.text(x[i], y[i], w_name[i],
                       ha='center', va='center',
                       size=14, weight=1000)
        text.set_path_effects([path_effects.Stroke(linewidth=2, foreground='white'),
                               path_effects.Normal()])
    canvas.draw()
    
def show_dU():
    global ax
    global dU
    
    # Read dU
    dU = pd.read_csv(f_dU, sep="\t", header=0)

    pts_ns = pd.Series(pd.concat([dU.iloc[:, 0],
                                   dU.iloc[:, 1]],
                                  ignore_index=True).sort_values().unique())
    
#    # Draw arrow
#
#        x1 = float(x[w_name == p[len(p)-1]])
#        y1 = float(y[w_name == p[len(p)-1]])
#        x2 = float(x[w_name == p[0]])
#        y2 = float(y[w_name == p[0]])
#        
#        ax.annotate('',
#                    xy=((pd.Series(my_x, dtype="float64").mean() + x2)/2,
#                        (pd.Series(my_y, dtype="float64").mean() + y2)/2),
#                    xytext=((pd.Series(my_x, dtype="float64").mean() + x1)/2,
#                            (pd.Series(my_y, dtype="float64").mean() + y1)/2),
#                    arrowprops=dict(facecolor='steelblue',
#                                    shrink=0.05),
#                    zorder = -1)

    
    # Write dUs on graph
    dU_x = pd.Series(dtype='float64')
    dU_y = pd.Series(dtype='float64')
    pt_1i = pd.Series(dtype='int64')
    pt_2i = pd.Series(dtype='int64')
    for _, dU_vect in dU.iterrows():
        
        x1 = float(x[w_name == dU_vect[0]])
        y1 = float(y[w_name == dU_vect[0]])
        x2 = float(x[w_name == dU_vect[1]])
        y2 = float(y[w_name == dU_vect[1]])
        
        if pts_ns[pts_ns == dU_vect[0]].index[0] > pts_ns[pts_ns == dU_vect[1]].index[0]:
            temp_1i = pts_ns[pts_ns == dU_vect[1]].index[0]
            temp_2i = pts_ns[pts_ns == dU_vect[0]].index[0]
        else:
            temp_1i = pts_ns[pts_ns == dU_vect[0]].index[0]
            temp_2i = pts_ns[pts_ns == dU_vect[1]].index[0]
        
        if len(pt_1i) > 0:
            if sum((pt_1i == temp_1i) & (pt_2i == temp_2i)) > 0:
                pt_1i = pd.concat([pt_1i, pd.Series(temp_1i)],ignore_index=True)
                pt_2i = pd.concat([pt_2i, pd.Series(temp_2i)],ignore_index=True)
            else:
                pt_1i = pd.concat([pt_1i, pd.Series(temp_1i)],ignore_index=True)
                pt_2i = pd.concat([pt_2i, pd.Series(temp_2i)],ignore_index=True)
                
                ax.annotate('',
                            xy=(x2,y2),
                            xytext=(x1,y1),
                            arrowprops=dict(facecolor='black',
                                            shrink=0.03),
                            zorder = -1)
        else:
            pt_1i = pd.concat([pt_1i, pd.Series(temp_1i)],ignore_index=True)
            pt_2i = pd.concat([pt_2i, pd.Series(temp_2i)],ignore_index=True)
            
            ax.annotate('',
                        xy=(x2,y2),
                        xytext=(x1,y1),
                        arrowprops=dict(facecolor='black',
                                        shrink=0.03),
                        zorder = -1)
            
        x_mean = (x1 + x2) / 2
        y_mean = (y1 + y2) / 2
        dU_x = pd.concat([dU_x, pd.Series(x_mean)],ignore_index=True)
        dU_y = pd.concat([dU_y, pd.Series(y_mean)],ignore_index=True)
        
        if pts_ns[pts_ns == dU_vect[0]].index[0] > pts_ns[pts_ns == dU_vect[1]].index[0]:
            text = ax.text(x_mean,
                        y_mean - sum((dU_x == x_mean) & (dU_y == y_mean))*40 + 60,
                        -dU_vect[2],
                        ha='center',
                        va='center',
                        color='brown',
                        size=14,
                        weight=1000)
        else:
            text = ax.text(x_mean,
                        y_mean - sum((dU_x == x_mean) & (dU_y == y_mean))*40 + 60,
                        dU_vect[2],
                        ha='center',
                        va='center',
                        color='brown',
                        size=14,
                        weight=1000)
        text.set_path_effects([path_effects.Stroke(linewidth=2, foreground='white'),
                            path_effects.Normal()])
    canvas.draw()

def show_contour_error():
    global ax
    global dU
    
    # Calculate and write contour summ
    with open(f_pols) as f:
        pols_t = [line.rstrip() for line in f]

    pols = [list(map(int, p.split())) for p in pols_t]

    dU_U = dU.iloc[:, 2]
    dU_N1 = dU.iloc[:, 0]
    dU_N2 = dU.iloc[:, 1]

    for p in pols:
        myU = 0
        my_x = []
        my_y = []
        for i in range(0, len(p)-1):
            myU += pd.concat([dU_U[(dU_N1 == p[i]) & (dU_N2 == p[i+1])],
                            -dU_U[(dU_N1 == p[i+1]) & (dU_N2 == p[i])]],
                            ignore_index=True).mean()
            my_x.append(float(x[w_name == p[i]]))
            my_y.append(float(y[w_name == p[i]]))
        myU += pd.concat([dU_U[(dU_N1 == p[len(p)-1]) & (dU_N2 == p[0])],
                        -dU_U[(dU_N1 == p[0]) & (dU_N2 == p[len(p)-1])]],
                        ignore_index=True).mean()
        my_x.append(float(x[w_name == p[len(p)-1]]))
        my_y.append(float(y[w_name == p[len(p)-1]]))
        
        # Write contour summ
        text = ax.text(pd.Series(my_x, dtype="float64").mean(),
                    pd.Series(my_y, dtype="float64").mean(),
                    round(myU, 3),
                    ha='center',
                    va='center',
                    color='blue',
                    size=14,
                    weight=1000)
        text.set_path_effects([path_effects.Stroke(linewidth=2, foreground='white'),
                            path_effects.Normal()])
        
        # Draw arrow
        x1 = float(x[w_name == p[len(p)-1]])
        y1 = float(y[w_name == p[len(p)-1]])
        x2 = float(x[w_name == p[0]])
        y2 = float(y[w_name == p[0]])
        
        ax.annotate('',
                    xy=((pd.Series(my_x, dtype="float64").mean() + x2)/2,
                        (pd.Series(my_y, dtype="float64").mean() + y2)/2),
                    xytext=((pd.Series(my_x, dtype="float64").mean() + x1)/2,
                            (pd.Series(my_y, dtype="float64").mean() + y1)/2),
                    arrowprops=dict(facecolor='steelblue',
                                    shrink=0.05),
                    zorder = -1)
    canvas.draw()
    

def load_xy_poinst():
    global init_dir
    global f_points
    
    filetypes = (("Текстовый файл", "*.txt"),
                 ("CSV", "*.csv"),
                 ("Любой", "*"))
    filename = fd.askopenfilename(title="Открыть файл", initialdir=init_dir,
                                    filetypes=filetypes)
    if filename:
        init_dir = os.path.dirname(filename)
        f_points = filename
        show_points()
        
def load_dU():
    global init_dir
    global f_dU
    
    filetypes = (("Текстовый файл", "*.txt"),
                 ("CSV", "*.csv"),
                 ("Любой", "*"))
    filename = fd.askopenfilename(title="Открыть файл", initialdir=init_dir,
                                    filetypes=filetypes)
    if filename:
        init_dir = os.path.dirname(filename)
        f_dU = filename
        show_dU()

def load_pols():
    global init_dir
    global f_pols
    
    filetypes = (("Текстовый файл", "*.txt"),
                 ("CSV", "*.csv"),
                 ("Любой", "*"))
    filename = fd.askopenfilename(title="Открыть файл", initialdir=init_dir,
                                    filetypes=filetypes)
    if filename:
        init_dir = os.path.dirname(filename)
        f_pols = filename
        show_contour_error()
        
def reload():
    show_points()

    show_dU()

    show_contour_error()

    canvas.draw()

# ToDo Add Buttons for loading data
but1_x = 5
but1_y = 15
but_dy = 10
but_h = 40

but_load_points = tk.Button(panel, text="Загрузить точки",
                            command=load_xy_poinst)
but_load_points.place(x=but1_x,
                      y=but1_y,
                      width=panel_w - 2*but1_x,
                      height=but_h)

but_load_dU = tk.Button(panel, text="Загрузить разницы\nпотенциалов",
                            command=load_dU)
but_load_dU.place(x=but1_x,
                  y=but1_y + (but_h + but_dy),
                  width=panel_w - 2*but1_x,
                  height=but_h)

but_load_dU = tk.Button(panel, text="Загрузить контуры",
                            command=load_pols)
but_load_dU.place(x=but1_x,
                  y=but1_y + 2*(but_h + but_dy),
                  width=panel_w - 2*but1_x,
                  height=but_h)

but_reload = tk.Button(panel, text="Перечитать файлы",
                            command=reload)
but_reload.place(x=but1_x,
                  y=but1_y + 3*(but_h + but_dy),
                  width=panel_w - 2*but1_x,
                  height=but_h)

canvas = FigureCanvasTkAgg(fig, master=win)

show_points()

show_dU()

show_contour_error()

canvas.draw()

# placing the canvas on the Tkinter window
canvas.get_tk_widget().pack(fill="both", side="top", expand=True)

# creating the Matplotlib toolbar
toolbar = NavigationToolbar2Tk(canvas, win)
toolbar.update()

# placing the toolbar on the Tkinter window
canvas.get_tk_widget().pack()


def onclick(event):
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))

cid = fig.canvas.mpl_connect('button_press_event', onclick)

win.mainloop()