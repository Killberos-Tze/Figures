#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 06:49:34 2024

@author: tze
"""

from matplotlib.figure import Figure
from numpy import min as npmin
from numpy import max as npmax
from numpy import append as npappend

#figure with of without linked right axes
class FigureXY2(Figure):
    def __init__(self,y2=False,**kwargs):
        super().__init__(**kwargs)
        self.set_size_inches((11/2.54,8/2.54))
        self._axy=self.add_axes([2/11,2/11,7/11,5/8])
        self._axy.tick_params(labelsize=8)

        self._y2=y2

        if self._y2:
            #linked right axes  https://matplotlib.org/stable/gallery/subplots_axes_and_figures/two_scales.html#sphx-glr-gallery-subplots-axes-and-figures-two-scales-py
            self._axy2=self._axy.twinx()
            self._axy2.tick_params(labelsize=8)
            self._axy.tick_params(axis='y',labelcolor='tab:blue')
            self._axy2.tick_params(axis='y',labelcolor='tab:red')

        self._init_figure()

    def __str__(self):
        return 'v_draw'

    
    def add_canvas(self,canvas):
        self.canvas=canvas
        self.canvasdraw=self.canvas.draw

    def _update_x_label(self,xname):
        self._axy.set_xlabel(xname,fontsize=10, position=(0.5,0),labelpad=5)

    def _update_y_label(self,yname):
        self._axy.set_ylabel(yname,fontsize=10, position=(0.5,0),labelpad=5,color='tab:blue')

    def _update_y2_label(self,y2name):
        if self._y2:
            self._axy2.set_ylabel(y2name,fontsize=10, position=(0.5,0),labelpad=5,color='tab:red')

    #initlizes the figure
    def _init_figure(self):
        self._axy.set_xlim(0,1)
        self._axy.set_ylim(0,1)
        if self._y2:
            self._axy.plot([],[],color='tab:blue')
            self._axy2.plot([],[],color='tab:red')
            self._axy2.set_ylim(0,1)

    #if x negative i start from 1.02xmin, if x positive I start from 0
    #0.98 is here if I don't want to use 0 as reference
    def _find_min(self,x):
        return min([0,1.02*(npmin(x)),0.98*(npmin(x))])
    #if x negative I start from 0, if x positive I end up with 1.02xmax
    #0.98 is here if I don't want to use 0 as reference
    def _find_max(self,x):
        return max([0,1.02*(npmax(x)),0.98*(npmax(x))])

    #not private
    #plots the data it receives (appending should be done in main if needed)
    def plot_measured_data(self,x,y,y2=None):#x, y, y2 are just numpy arrays
        if len(x)==len(y):
            self._axy.set_xlim(self._find_min(x),self._find_max(x))
            self._axy.set_ylim(self._find_min(y),self._find_max(y))
        if len(self._axy.lines)!=0:
            self._axy.lines[-1].set_xdata(x)
            self._axy.lines[-1].set_ydata(y)
        if self._y2:
            if len(x)==len(y2):
                self._axy2.set_ylim(self._find_min(y2),self._find_max(y2))

            if len(self._axy2.lines)!=0:
                self._axy2.lines[-1].set_ydata(y2)
        self.canvasdraw()


    def plot_loaded_curves(self,datalist=[],masklist=[]):#datalist is list of datadictionaries masklist is a list of checkboxes states
        if len(datalist)==len(masklist) and len(datalist)!=0:
            self._axy.set_prop_cycle(None)
            for idx,item in enumerate(masklist):
                if item == 'on':
                    self._axy.plot(datalist[idx]['#data_table'][:,0],datalist[idx]['#data_table'][:,1])
                elif item == 'off':
                    self._axy.plot([],[])

    #appends and then plots data
    def append_plot_data(self,x,y,y2):
        if len(self._axy.lines)!=0:
            xold=self._axy.lines[-1].get_xdata()
            yold=self._axy.lines[-1].get_ydata()
        x=npappend(xold,x)
        y=npappend(yold,y)
        if self._y2:
            if len(self._axy2.lines)!=0:
                y2old=self._axy2.lines[-1].get_ydata()

            y2=npappend(y2old,y2)
            self.plot_data(x,y,y2)
        else:
            self.plot_data(x,y)

        self.canvasdraw()
    #clears the whole graph
    def clear_graph(self):
        while (len(self._axy.lines)):
            self._axy.lines[-1].remove()
        if self._y2:
            while (len(self._axy2.lines)):
                self._axy2.lines[-1].remove()
        self._init_figure()
        self.canvasdraw()

    #clears the last point
    def delete_last_point(self):
        if len(self._axy.lines)!=0:
            x=self._axy.lines[-1].get_xdata()
            y=self._axy.lines[-1].get_ydata()
            self._axy.lines[-1].set_xdata(x[:-1])
            self._axy.lines[-1].set_ydata(y[:-1])
        if self._y2:
            if len(self._axy2.lines)!=0:
                y2=self._axy2.lines[-1].get_ydata()
                self._axy2.lines[-1].set_ydata(y2[:-1])
        self.canvasdraw()

    #updates labels
    def update_labels(self,*args,**kwargs):
        if args:
            if len(args)>=3 and self._y2:
                self._update_y2_label(args[2])
            if len(args)>=2:
                self._update_y_label(args[1])
            if len(args)>=1:
                self._update_x_label(args[0])
            return
        if kwargs:
            if 'x' in kwargs:
                self._update_x_label(kwargs['x'])
            if 'y1' in kwargs:
                self._update_y_label(kwargs['y1'])
            if 'y2' in kwargs and self._y2:
                self._update_y2_label(kwargs['y2'])
            return
        self.canvasdraw()