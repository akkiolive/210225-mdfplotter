from asammdf import MDF
import sys
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle
from MDFPlotConnect import connect

class Sig:
    def __init__(self, timestamps=None, samples=None, name=None):
        if timestamps is None or samples is None:
            from numpy.random import random
            for i in range(10):
                self.timestamps = i + random()
                self.samples = i*i*random()
                self.name = "ExampleSignal"
        else:
            self.timestamps = timestamps
            self.samples = samples
            self.name = name


class MDFPlotter:
    def __init__(self, mdfpath=None):
        # asammdf
        self.LoadMDF(mdfpath)
        ## load example 3 signals
        self.AllSignalNames = []
        self.PlotSignalNames = []
        self.PlotSignalNum = 0
        self.PlotSignals = []
        ### load
        i = 0
        while True:
            j = 0
            break_flag = False
            while True:
                try:
                    signal_name = self.mdf.get_channel_name(i, j)
                    if signal_name != "time" and signal_name != "t":
                        self.PlotSignalNames.append(signal_name)
                        self.PlotSignals.append(self.mdf.get(signal_name, raw=True))
                        self.PlotSignalNum += 1
                        print(signal_name)
                        if self.PlotSignalNum >= 3:
                            break_flag = True
                            break
                except:
                    if j == 0:
                        break_flag = True
                    break
                j += 1
            if break_flag:
                break


        # matplotlib
        self.fig = plt.figure()
        self.connect()
        ## set background ax
        gs = GridSpec(ncols=1, nrows=1, left=0, right=1, top=1, bottom=0)
        self.bg_ax = self.fig.add_subplot(gs[0])
        ax = self.bg_ax
        ax.patch.set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)

        ## set info ax
        self.info_axes = []
        self.set_info_axes()

        ## set main ax
        self.main_axes = []
        self.set_main_axes()

        ## draw line
        for i, signal in enumerate(self.PlotSignals):
            ax = self.main_axes[i]
            ax.step(signal.timestamps, signal.samples, where="post")
        self.xlim = list(self.main_axes[-1].get_xlim())
        
        ## draw
        self.fig.canvas.draw()

        ## show
        plt.show()

        
        

    def set_main_axes(self):
        nrows = self.PlotSignalNum + 2
        gs = GridSpec(ncols=2, nrows=nrows, width_ratios=[0.1, 0.9], left=0.2, right=0.8, top=0.8, bottom=0.2)
        self.head_ax = self.fig.add_subplot(gs[0,1])
        self.foot_ax = self.fig.add_subplot(gs[-1,1])
        for ax in self.main_axes:
            ax.remove()
        for i, signal_name in enumerate(self.PlotSignalNames):
            ax = self.fig.add_subplot(gs[i+1, 1], sharex=self.foot_ax)
            self.main_axes.append(ax)
            ax.spines["right"].set_visible(False)
            ax.spines["top"].set_visible(False)
            ax.spines["bottom"].set_visible(False)
            ax.xaxis.set_visible(False)
        

            

    def set_info_axes(self):
        nrows = self.PlotSignalNum + 2
        gs = GridSpec(ncols=2, nrows=nrows, width_ratios=[0.1, 0.9], left=0.2, right=0.8, top=0.8, bottom=0.2)
        for ax in self.info_axes:
            ax.remove()
        for i, signal_name in enumerate(self.PlotSignalNames):
            ax = self.fig.add_subplot(gs[i+1, 0])
            self.info_axes.append(ax)
            ax.patch.set_visible(False)
            ax.spines["left"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["top"].set_visible(False)
            ax.spines["bottom"].set_visible(False)
            ax.xaxis.set_visible(False)
            ax.yaxis.set_visible(False)

            

    def LoadMDF(self, mdfpath):
        print("Loading", mdfpath, "...")
        self.mdfpath = mdfpath
        self.mdf = MDF(mdfpath)
        return self.mdf

    def Clear_White(self):
        rect = Rectangle(xy=(0,0), width=1, height=1, fc="white")
        self.bg_ax.draw_artist(rect)
        self.fig.canvas.blit()
    
    def Draw_Alls(self):
        		
		for num, ax in enumerate(self.main_axes):
			ax.patch.set_visible(False)
			#ax.spines["left"].set_visible(False)
			ax.spines["right"].set_visible(False)
			ax.spines["top"].set_visible(False)
			ax.spines["bottom"].set_visible(False)
			if num != len(self.main_axes) - 1:
				ax.xaxis.set_visible(False)
		self.fig.canvas.draw()
		self.REDRAWALL()

    def onClick(self, e):
        print(e)

        self.SetVCursor(e.xdata)
        self.REDRAWALL()
        return True
        #self.FILLWHITE()
        self.CLEARPLOTAREAS()
        ax = self.main_axes[-1]
        ax.plot([1,2,3,4], [2,34,5,6])
        #self.fig.draw_artist(ax.xaxis)
        
        bbox = ax.xaxis.get_tightbbox(self.fig.canvas.get_renderer())
        self.DrwaRect(xy=(bbox.x0, bbox.y0), width=bbox.width, height=bbox.height, fc=None, ec="red", lw=1, fill=False)
        
    

        xtick_x0 = ax.get_xticklabels()[0].get_window_extent().x0
        xtick_x1 = ax.get_xticklabels()[-1].get_window_extent().x0 + ax.get_xticklabels()[-1].get_window_extent().width
        xtick_width = xtick_x1 - xtick_x0
        xtick_y0 = ax.get_xticklabels()[0].get_window_extent().y0
        xtick_y1 = ax.get_xticklabels()[-1].get_window_extent().y0 + ax.get_xticklabels()[-1].get_window_extent().height
        xtick_height = xtick_y1 - xtick_y0
        self.DrwaRect(xy=(xtick_x0, xtick_y0), width=xtick_width, height=xtick_height, fill=False, ec="green", lw=1)

        print(xtick_x0)

    
        x0 = ax.get_xticklabels()[0].get_window_extent().x0
        y0 = ax.get_xticklabels()[0].get_window_extent().y0
        width = ax.get_xticklabels()[0].get_window_extent().width
        height = ax.get_xticklabels()[0].get_window_extent().height
        self.DrwaRect(xy=(x0, y0), width=width, height=height, fill=False, ec="red", lw=1)


        bbox = ax.get_tightbbox(self.fig.canvas.get_renderer(), call_axes_locator=True, for_layout_only=True)
        self.DrwaRect(xy=(bbox.x0, bbox.y0), width=bbox.width, height=bbox.height, fc=None, ec="blue", lw=1, fill=False)
        
        self.fig.canvas.blit()


    def onClickRelease(self, e):
        print(e)

    def onScroll(self, e):
        print(e)
        self.CLEARXAXIS()
        self.CLEARPLOTAREAS_EX()

        ax = self.main_axes[-1]
        xlim = ax.get_xlim()

        self.fig.draw_artist(ax.spines["bottom"])


        if e.button == "down":
            ax.set_xlim(
                xlim[0] + (xlim[1]-xlim[0]) * 0.3,
                xlim[1] + (xlim[1]-xlim[0]) * 0.3,
            )
        elif e.button == "up":
            ax.set_xlim(
                xlim[0] - (xlim[1]-xlim[0]) * 0.3,
                xlim[1] - (xlim[1]-xlim[0]) * 0.3,
            )
        
        
        self.anno_ax.set_xlim(self.main_axes[-1].get_xlim())
        
        self.fig.draw_artist(ax.xaxis)
        
        
        self.REDRAWLINES()
        self.REDRAWANNOAX()
        #self.fig.canvas.blit()
        self.REDRAWALL()
        self.main_xlim = self.main_axes[-1].get_xlim()


    def onMouseMove(self, e):
        print(e)

    def onKeyPress(self, e):
        print(e, e.key)
        if e.key == "ctrl+r":
            inter = Interactor()
            print(type(self.plot_signal_names))
            ret = inter.SignalSelector(self.all_signal_names, self.plot_signal_names)
            if ret[0] == True:
                self.plot_signal_names = ret[1]
                print(ret[1])
                self.REFRESHPLOTSIGS()
        elif e.key == "f5":
            self.fig.canvas.draw()

    def onKeyRelease(self, e):
        print(e)
        #self.main_axes[0].set_position([0.1,0.4,0.5,0.5])
        self.REDRAWALL()

    def onPick(self, e):
        print(e)

    def onDraw(self, e):
        print(e)
        
        
    def onResize(self, e):
        print(e)
        
    
    def connect(self):
        self.fig.canvas.mpl_connect("button_press_event", self.onClick)
        self.fig.canvas.mpl_connect("button_release_event", self.onClickRelease)
        self.fig.canvas.mpl_connect("motion_notify_event", self.onMouseMove)
        self.fig.canvas.mpl_connect("scroll_event", self.onScroll)
        self.fig.canvas.mpl_connect("key_press_event", self.onKeyPress)
        self.fig.canvas.mpl_connect("key_release_event", self.onKeyRelease)
        self.fig.canvas.mpl_connect("pick_event", self.onPick)
        self.fig.canvas.mpl_connect("draw_event", self.onDraw)
        self.fig.canvas.mpl_connect("resize_event", self.onResize)


plter = MDFPlotter(mdfpath=sys.argv[1])