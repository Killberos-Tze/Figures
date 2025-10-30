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
from numpy import array as nparray
from numpy import shape as npshape

#figure with of without linked right axes
class FigureXY2(Figure):
    def __init__(self,y2=False,figsize=(11/2.54,8/2.54),axsize=[2/11,2/11,7/11,5/8],**kwargs):
        super().__init__(**kwargs)
        self.set_size_inches(figsize)
        self._axy=self.add_axes(axsize)
        self._axy.tick_params(labelsize=8)
        self._axy.grid(color='lightgray', which='major', axis='both')
        self._y2=y2

        if self._y2:
            #linked right axes  https://matplotlib.org/stable/gallery/subplots_axes_and_figures/two_scales.html#sphx-glr-gallery-subplots-axes-and-figures-two-scales-py
            self._axy2=self._axy.twinx()
            self._axy2.tick_params(labelsize=8)
            self._axy.tick_params(axis='y',labelcolor='tab:blue')
            self._axy.grid(color="tab:blue",ls='--',which='major', axis='y')
            self._axy2.tick_params(axis='y',labelcolor='tab:red')
            self._axy2.grid(color="tab:red",ls=':',which='major', axis='y')

        self._init_figure()

    def __str__(self):
        return 'v_draw'

    def add_canvas(self,canvas):
        self.canvas=canvas
        self.canvasdraw=self.canvas.draw

    def _update_x_label(self,xname):
        self._axy.set_xlabel(xname,fontsize=10, position=(0.5,0),labelpad=5)

    def _update_y_label(self,yname):
        if self._y2:
            self._axy.set_ylabel(yname,fontsize=10, position=(0.5,0),labelpad=5,color='tab:blue')
        else:
            self._axy.set_ylabel(yname,fontsize=10, position=(0.5,0),labelpad=5)

    def _update_y2_label(self,y2name):
        if self._y2:
            self._axy2.set_ylabel(y2name,fontsize=10, position=(0.5,0),labelpad=5,color='tab:red')

    #initlizes the figure
    def _init_figure(self):
        self._axy.set_xlim(0,1)
        self._axy.set_ylim(0,1)
        if self._y2:
            self._axy2.set_ylim(0,1)

    def _init_plots(self):
        if self._y2:
            if len(self._axy.lines)==0:
                self._axy.plot([],[],color='tab:blue')
            if len(self._axy2.lines)==0:
                self._axy2.plot([],[],color='tab:red')
        else:
            if len(self._axy.lines)==0:
                self._axy.plot([],[])
    def _clear_plots(self):
        while (len(self._axy.lines)):
            self._axy.lines[-1].remove()
        if self._y2:
            while (len(self._axy2.lines)):
                self._axy2.lines[-1].remove()
    #if x negative i start from 1.02xmin, if x positive I start from 0
    #0.98 is here if I don't want to use 0 as reference
    def _find_min(self,x,zero=False):
        if zero:
            return min([0,1.02*(npmin(x)),0.98*(npmin(x))])
        else:
            return min([1.02*(npmin(x)),0.98*(npmin(x))])
    #if x negative I start from 0, if x positive I end up with 1.02xmax
    #0.98 is here if I don't want to use 0 as reference
    def _find_max(self,x,zero=False):
        if zero:
            return max([0,1.02*(npmax(x)),0.98*(npmax(x))])
        else:
            return max([1.02*(npmax(x)),0.98*(npmax(x))])
    #not private
    #plots the data it receives (appending should be done in main if needed)
    def plot_data(self,x,y,y2=nparray([])):#x, y, y2 are just numpy arrays
        self._init_plots()
        if len(x)==len(y):
            if npshape(x)!=npshape(nparray([])):
                self._axy.set_xlim(self._find_min(x),self._find_max(x))
            if npshape(y)!=npshape(nparray([])):
                self._axy.set_ylim(self._find_min(y),self._find_max(y))
            self._axy.lines[-1].set_xdata(x)
            self._axy.lines[-1].set_ydata(y)
        if self._y2:
            if len(x)==len(y2):
                if npshape(y2)!=npshape(nparray([])):
                    self._axy2.set_ylim(self._find_min(y2),self._find_max(y2))
                self._axy2.lines[-1].set_ydata(y2)
        self.canvasdraw()

#appends and then plots data
    def append_plot_data(self,x,y,y2=None):
        if len(self._axy.lines)!=0:
            xold=self._axy.lines[-1].get_xdata()
            yold=self._axy.lines[-1].get_ydata()
        else:
            xold=nparray([])
            yold=nparray([])
        x=npappend(xold,x)
        y=npappend(yold,y)
        if self._y2:
            if len(self._axy2.lines)!=0:
                y2old=self._axy2.lines[-1].get_ydata()
            else:
                y2old=nparray([])
            y2=npappend(y2old,y2)
            self.plot_data(x,y,y2)
        else:
            self.plot_data(x,y)
        self.canvasdraw()

    #clears the whole graph
    def clear_graph(self):
        self._clear_plots()
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

    def set_x_grid_lines(self,num):
        self._axy.locator_params(axis='x', nbins=num)
        self.canvasdraw()

    def clear_xy_curves(self):
        tmp=self._axy.get_legend()
        if tmp:
            tmp.remove()
        while len(self._axy.lines)!=0:
            self._axy.lines[-1].remove()
        self._axy.set_xlim(0,1)
        self._axy.set_ylim(0,1)
        self.canvasdraw()

    #plots xy sets of data that can be masked (masking assumes that you are sending either checkbox of on/off button reference)
    def plot_xy_dict(self,datalist={},masklist={},RTA=True):#datalist is dictionary of datadictionaries masklist is a dictionary of checkboxe references
        self.clear_xy_curves()
        if len(datalist)==len(masklist) and len(datalist)!=0:
            xmin=[]
            xmax=[]
            ymin=[]
            if RTA:
                ymax=[1]
            else:
                ymax=[]
            handles=[]
            self._axy.set_prop_cycle(None)
            for key in masklist.keys():
                if masklist[key].get_state() == 'on':
                    x=datalist[key]['#data_table'][:,datalist[key]['#data_summary']['x1_col']]
                    y=datalist[key]['#data_table'][:,datalist[key]['#data_summary']['y1_col']]
                    xmin.append(npmin(x))
                    xmax.append(npmax(x))
                    ymin.append(self._find_min(y))
                    ymax.append(self._find_max(y))
                    self._axy.set_xlim(min(xmin),max(xmax))
                    self._axy.set_ylim(min(ymin),max(ymax))
                    tmp,=self._axy.plot(x,y,label=datalist[key]["#data_summary"]["y1_label"])
                    handles.append(tmp)
                    self._update_x_label(datalist[key]['#data_summary']['x1_name']+' '+'('+datalist[key]['#data_summary']['x1_prefix']+datalist[key]['#data_summary']['x1_unit']+')')
                elif masklist[key].get_state() == 'off':
                    self._axy.plot([],[])
            if len(handles):
                self._axy.legend(handles=handles,loc=(1,0))
            self.canvasdraw()

    def plot_xy_lists(self,datalist=[],masklist=[],RTA=True):#datalist is list of datadictionaries masklist is a list of checkboxe references
        self.clear_xy_curves()
        if len(datalist)==len(masklist) and len(datalist)!=0:
            xmin=[]
            xmax=[]
            ymin=[]
            if RTA:
                ymax=[1]
            else:
                ymax=[]
            handles=[]
            self._axy.set_prop_cycle(None)
            for key,item in enumerate(masklist):
                if item.is_enabled() == False:
                    x=datalist[key]['#data_table'][:,datalist[key]['#data_summary']['x1_col']]
                    y=datalist[key]['#data_table'][:,datalist[key]['#data_summary']['y1_col']]
                    xmin.append(npmin(x))
                    xmax.append(npmax(x))
                    ymin.append(self._find_min(y))
                    ymax.append(self._find_max(y))
                    self._axy.set_xlim(min(xmin),max(xmax))
                    self._axy.set_ylim(min(ymin),max(ymax))
                    tmp,=self._axy.plot(x,y,label=datalist[key]["#data_summary"]["y1_label"],linestyle=(0, (5, 10)))
                    handles.append(tmp)
                    self._update_x_label(datalist[key]['#data_summary']['x1_name']+' '+'('+datalist[key]['#data_summary']['x1_prefix']+datalist[key]['#data_summary']['x1_unit']+')')
                elif item.get_state() == 'on':
                    x=datalist[key]['#data_table'][:,datalist[key]['#data_summary']['x1_col']]
                    y=datalist[key]['#data_table'][:,datalist[key]['#data_summary']['y1_col']]
                    xmin.append(npmin(x))
                    xmax.append(npmax(x))
                    ymin.append(self._find_min(y))
                    ymax.append(self._find_max(y))
                    self._axy.set_xlim(min(xmin),max(xmax))
                    self._axy.set_ylim(min(ymin),max(ymax))
                    tmp,=self._axy.plot(x,y,label=datalist[key]["#data_summary"]["y1_label"])
                    handles.append(tmp)
                    self._update_x_label(datalist[key]['#data_summary']['x1_name']+' '+'('+datalist[key]['#data_summary']['x1_prefix']+datalist[key]['#data_summary']['x1_unit']+')')
                elif masklist[key].get_state() == 'off':
                    self._axy.plot([],[])
            if len(handles):
                self._axy.legend(handles=handles,loc=(1,0))
            self.canvasdraw()

#multpiple legends add_artist (old legend)



class FigureLineMap(Figure):
    def __init__(self,*args,figsize=(9.5/2.54,14/2.54),**kwargs):
        #matplotlib muliplies axes size with large figure size that is why you always divide with large figure size
        xdim=figsize[0]*2.54
        ydim=figsize[1]*2.54
        super().__init__(*args,figsize=figsize,**kwargs)
        axx=7
        axy=5
        axx0=1.5
        axy0=1.5
        spacing=1.5
        self._axy=self.add_axes((axx0/xdim,axy0/ydim,axx/xdim,axy/ydim))
        self._axy.tick_params(labelsize=8)
        self._axy.grid(color='lightgray', which='major', axis='both')
        self._axy2=self.add_axes([axx0/xdim,(axy0+axy+spacing)/ydim,axx/xdim,axy/ydim])
        self._axy2.tick_params(labelsize=8)
        self._axy2.grid(color='lightgray', which='major', axis='both')

    def __str__(self):
        return 'v_draw'

    def add_canvas(self,canvas):
        self.canvas=canvas
        self.canvasdraw=self.canvas.draw

    def _update_x_label(self,xname):
        self._axy.set_xlabel(xname,fontsize=10, position=(0.5,0),labelpad=5)

    def _update_x2_label(self,xname):
        self._axy2.set_xlabel(xname,fontsize=10, position=(0.5,0),labelpad=5)

    def _update_y_label(self,yname):
        self._axy.set_ylabel(yname,fontsize=10, position=(0.5,0),labelpad=5)

    def _update_y2_label(self,yname):
        self._axy2.set_ylabel(yname,fontsize=10, position=(0.5,0),labelpad=5)

    def plot_absorbance(self,R,T,A):
        self.clear_absorbance()
        self._axy.set_prop_cycle(None)
        self._axy2.set_prop_cycle(None)
        self._axy.set_ylim(0,1.02)
        self._axy2.set_ylim(0,1.02)
        xmin=[]
        xmax=[]
        handles=[]
        handles2=[]
        for item in [R,T,A]:
            x=item['#data_table'][:,item['#data_summary']['x1_col']]
            xmin.append(npmin(x))
            xmax.append(npmax(x))
            self._axy.set_xlim(min(xmin),max(xmax))
            self._axy2.set_xlim(min(xmin),max(xmax))

        xt=T['#data_table'][:,T['#data_summary']['x1_col']]
        yt=T['#data_table'][:,T['#data_summary']['y1_col']]
        labelt=T["#data_summary"]["y1_label"]
        xr=R['#data_table'][:,R['#data_summary']['x1_col']]
        yr=R['#data_table'][:,R['#data_summary']['y1_col']]
        labelr='1-'+R["#data_summary"]["y1_label"]
        xa=A['#data_table'][:,R['#data_summary']['x1_col']]
        ya=A['#data_table'][:,R['#data_summary']['y1_col']]
        labela=A["#data_summary"]["y1_label"]

        tmp,=self._axy.plot(xt,yt,color='black',label=labelt)
        handles.append(tmp)
        tmp,=self._axy.plot(xr,1-yr,color='blue',label=labelr)
        handles.append(tmp)
        tmp=self._axy.fill_between(xr,yt,1-yr,color='red',label=labela)
        handles.append(tmp)
        self._axy.legend(handles=handles,loc=(1,0))

        tmp,=self._axy2.plot(xa,ya,label=labela,color='red')
        handles2.append(tmp)
        self._axy2.legend(handles=handles2,loc=(1,0))
        self._update_x2_label(A['#data_summary']['x1_name']+' ('+A['#data_summary']['x1_prefix']+A['#data_summary']['x1_unit']+')')
        self._update_x_label(A['#data_summary']['x1_name']+' ('+A['#data_summary']['x1_prefix']+A['#data_summary']['x1_unit']+')')
        self.canvasdraw()

    def clear_absorbance(self):
        while len(self._axy.collections):
            self._axy.collections[-1].remove()
        while len(self._axy.lines):
            self._axy.lines[-1].remove()
        while len(self._axy2.lines):
            self._axy2.lines[-1].remove()
        self.canvasdraw()
