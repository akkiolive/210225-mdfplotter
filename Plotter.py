from asammdf import MDF
import sys
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle
from MDFPlotConnect import connect
from interactor import Interactor
import bisect

class Colors:
    def __init__(self, colors=None, subcolors=None):
        # set color index
        self.color_index = 0
        # set colors
        ## arbital colors
        if colors:
            self.colors = colors
            if subcolors is None:
                self.subcolors = self.colors
        ## default colors
        else:
            self.colors = [
                "#1f77b4",
                "#ff7f0e",
                "#2ca02c",
                "#9467bd",
                "#8c564b",
                "#e377c2",
                "#7f7f7f",
                "#bcbd22",
                "#17becf"
            ]
            self.subcolors = [
                "#aec7e8",
                "#ffbb78",
                "#98df8a",
                "#c5b0d5",
                "#c49c94",
                "#f7b6d2",
                "#c7c7c7",
                "#dbdb8d",
                "#9edae5"
            ]
        # set first color
        self.color = self.colors[self.color_index]
        self.subcolor = self.subcolors[self.color_index]



    def get_color(self, proceed=False):
        self.color = self.colors[self.color_index]
        if proceed:
            self.color_index += 1
            if self.color_index >= len(self.colors):
                self.color_index = 0
        return self.color
    
    def get_subcolor(self, proceed=False):
        self.subcolor = self.subcolors[self.color_index]
        if proceed:
            self.color_index += 1
            if self.color_index >= len(self.colors):
                self.color_index = 0
        return self.subcolor

    def Proceed(self):
        self.color_index += 1
        if self.color_index >= len(self.colors):
            self.color_index = 0
        self.color = self.colors[self.color_index]
        self.subcolor = self.subcolors[self.color_index]
    
    def Receed(self):
        self.color_index += 1
        if self.color_index < 0:
            self.color_index = len(self.colors) - 1
        self.color = self.colors[self.color_index]
        self.subcolor = self.subcolors[self.color_index]
    
    def Initialize(self):
        self.color_index = 0
        # set first color
        self.color = self.colors[self.color_index]
        self.subcolor = self.subcolors[self.color_index]


class PlotSignal:
    def __init__(self, signal, color):
        self.signal = signal
        self.name = signal.name
        self.Color = color
        self.color = color.color
        self.subcolor = color.subcolor
        self.color_index = color.color_index

class MDFPlotter:
    def __init__(self, mdfpath=None):
        # asammdf
        self.LoadMDF(mdfpath)
        ## load example 3 signals
        self.AllSignalNames = []
        self.AllSignals = []
        self.PlotSignalNames = []
        self.PlotSignalNum = 0
        self.PlotSignals = []
        self.ValuesAtVCursor = []
        ## color
        self.Color = Colors()
        ### load
        i = 0
        while True:
            j = 0
            break_flag = False
            while True:
                try:
                    signal_name = self.mdf.get_channel_name(i, j)
                    if signal_name != "time" and signal_name != "t":
                        # append all names
                        self.AllSignalNames.append(signal_name)
                        # appedn all signals
                        signal = self.mdf.get(signal_name, raw=True)
                        plot_signal = PlotSignal(signal, self.Color)
                        self.AllSignals.append(plot_signal)
                        # proceed color
                        self.Color.Proceed()
                        # example plot 3 signals
                        if self.PlotSignalNum <= 3:
                            self.PlotSignalNames.append(signal_name)
                            self.PlotSignals.append(plot_signal)
                            self.PlotSignalNum += 1
                            self.ValuesAtVCursor.append(None)
                        print(signal_name)
                except:
                    if j == 0:
                        break_flag = True
                    break
                j += 1
            if break_flag:
                break
            i += 1


        # matplotlib
        self.fig = plt.figure(figsize=(10, 4.8))
        ## connct events
        self.click = False
        self.click_button = {
            "left": False,
            "middle": False,
            "right": False
        }
        self.press_keys = {
            "control": False,
            "shift": False,
            "alt": False,
            "r": False,
            "t": False,
            "y": False,
            "u": False,
            "i": False,
        }
        self.connect()
        ## set fonts
        from matplotlib import rcParams
        rcParams['font.family'] = 'sans-serif'
        rcParams['font.sans-serif'] = ['Meiryo']
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

        ## set axes
        self.main_axes = []
        self.info_axes = []
        self.info_value_texts = []
        self.vcursor_x = 0
        self.MyAnnotations = []
        self.make_axes()

        

        ## draw
        self.fig.canvas.draw()

        ## show
        plt.show()

        
    
    def apply_styles(self):
        # set main axes property
        for i, plot_signal in enumerate(self.PlotSignals):
            ax = self.main_axes[i]
            ax.spines["right"].set_visible(False)
            ax.spines["top"].set_visible(False)
            ax.spines["bottom"].set_visible(False)
            ax.spines["left"].set_color(plot_signal.color)
            ax.xaxis.set_visible(False)
            ax.tick_params(axis='y', colors=plot_signal.color, labelsize=10)
        self.main_axes[-1].xaxis.set_visible(True)
        self.main_axes[-1].tick_params(axis='x', colors="black", labelsize=10)
        # set property of other than main axes
        for ax in [self.head_ax, self.foot_ax, self.anno_ax] + self.info_axes:
            ax.patch.set_visible(False)
            ax.spines["left"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["top"].set_visible(False)
            ax.spines["bottom"].set_visible(False)
            ax.xaxis.set_visible(False)
            ax.yaxis.set_visible(False)
        print(len(self.main_axes))
        
    def make_axes(self, xlim=None):
        # grid spec
        nrows = self.PlotSignalNum + 2
        gs = GridSpec(ncols=2, nrows=nrows, height_ratios=[0.2]+[1]*self.PlotSignalNum+[0.2], width_ratios=[0.1, 0.9], left=0.2, right=0.98, top=0.97, bottom=0.03, wspace=0.2)
        # foot ax
        self.foot_ax = self.fig.add_subplot(gs[-1,1])
        # head ax
        self.head_ax = self.fig.add_subplot(gs[0,1], sharex=self.foot_ax)
        # main axes
        for ax in self.main_axes:
            ax.remove()
        self.main_axes = []
        for i, plot_signal in enumerate(self.PlotSignals):
            ax = self.fig.add_subplot(gs[i+1, 1], sharex=self.foot_ax)
            self.main_axes.append(ax)    
        ## draw line
        for i, plot_signal in enumerate(self.PlotSignals):
            signal = plot_signal.signal
            ax = self.main_axes[i]
            ax.step(signal.timestamps, signal.samples, where="post", color=plot_signal.color)
        
        
        # info axes
        for ax in self.info_axes:
            ax.remove()
        self.info_axes = []
        self.info_value_texts = []
        self.ValuesAtVCursor = [None]*self.PlotSignalNum
        for i, plot_signal in enumerate(self.PlotSignals):
            ax = self.fig.add_subplot(gs[i+1, 0])
            self.info_axes.append(ax)            
            ax.annotate(plot_signal.name, xy=(1,1), size=10, horizontalalignment="right", va="top", color=plot_signal.color)
            text = ax.annotate(str(self.ValuesAtVCursor[i]), xy=(1,1), size=10, ha="right", va="top", color=plot_signal.color)
            self.info_value_texts.append(text)
            text.set_visible(False)
        # anno ax
        remain_vcursor_visible = False
        try:
            self.anno_ax.remove()
            remain_vcursor_visible = True
        except:
            pass
        self.anno_ax = self.fig.add_subplot(gs[1:-1, 1], sharex=self.foot_ax)
        # set dummy vcursor
        self.vcursor = self.anno_ax.axvline(self.vcursor_x, lw=0.9, c="red")
        self.vcursor.set_visible(remain_vcursor_visible)

        # lim
        if xlim:
            self.foot_ax.set_xlim(xlim)
        self.xlim = list(self.main_axes[-1].get_xlim())
        # apply styles
        self.apply_styles()    

    def set_plot_signals(self, signal_names, remain_xlim=True):
        xlim = None
        if remain_xlim:
            xlim = self.main_axes[-1].get_xlim()
        # init
        self.PlotSignalNames = []
        self.PlotSignalNum = 0
        self.PlotSignals = []
        # loop
        for signal_name in signal_names:
            # found flag
            found_flag = False
            # find plot_signal
            for plot_signal in self.AllSignals:
                if plot_signal.name == signal_name:
                    self.PlotSignalNames.append(plot_signal.name)
                    self.PlotSignals.append(plot_signal)
                    self.PlotSignalNum += 1
                    found_flag = True
                    break
            if not found_flag: 
                print(signal_name, "is not found(set_plot_signals)")
        self.make_axes(xlim=xlim)    

    
    def set_values_at_vcursor(self, timestamp):
        self.ValuesAtVCursor = []
        for i, text in enumerate(self.info_value_texts):
            signal = self.PlotSignals[i].signal
            idx = find_nearest_index_bisection(signal.timestamps, timestamp)
            data = signal.samples[idx]
            self.ValuesAtVCursor.append(data)
            text.set_text( "\n="+str(data) )
            if data is None:
                text.set_visible(False)
            else:
                text.set_visible(True)
        


    def DrawRect(self, xy, width, height, fc="white", ec=None, lw=None, **kwargs):
        # # xy must be the screen xy pixels of fig
        # convert xy and w/h to xlim of bg_ax
        ## get fig size
        dpi = self.fig.get_dpi()
        figwidth = self.fig.get_figwidth() * dpi
        figheight = self.fig.get_figheight() * dpi
        ## convert
        xy_ = (
            xy[0] / figwidth,
            xy[1] / figheight
        )
        width_ = width / figwidth
        height_ = height / figheight
        # make rect
        rect = Rectangle(xy=xy_, width=width_, height=height_, fc=fc, ec=ec, lw=lw, **kwargs)
        # add to bg
        self.bg_ax.add_patch(rect)
        # drawing
        self.fig.draw_artist(rect)
        # remove rect from bg_ax
        self.bg_ax.patches[-1].remove()
    
    def LoadMDF(self, mdfpath):
        print("Loading", mdfpath, "...")
        self.mdfpath = mdfpath
        self.mdf = MDF(mdfpath)
        return self.mdf

    def Clear_Arb(self, artist, blit=False):
        bbox = artist.get_window_extent(self.fig.canvas.get_renderer())
        self.DrawRect(xy=(bbox.x0, bbox.y0), width=bbox.width, height=bbox.height)


    
    def Clear_White(self, blit=False):
        rect = Rectangle(xy=(0,0), width=1, height=1, fc="white", fill=True)
        self.bg_ax.add_patch(rect)
        self.bg_ax.draw_artist(rect)
        self.bg_ax.patches[-1].remove()
        if blit:
            self.fig.canvas.blit()

    

    def Clear_InfoAx(self, blit=False):
        for ax in self.info_axes:
            for text in ax.texts:
                self.Clear_Arb(text)
        if blit:
            self.fig.canvas.blit()
        
    def Draw_InfoAx(self, blit=False):
        for i, ax in enumerate(self.info_axes):
            data = self.ValuesAtVCursor[i]
            text = self.info_value_texts[i]
            text.set_text( str(data) )
            if data is None:
                text.set_visible(False)
            else:
                text.set_visible(True)
            for text in ax.texts:
                ax.draw_artist(text)
        if blit:
            self.fig.canvas.blit()
        
    def Refresh_InfoAx(self, blit=True):
        self.Clear_InfoAx()
        self.Draw_InfoAx(blit)
    
    def Draw_Alls(self, blit=False):
        for ax in self.fig.axes:
            # texts
            for text in ax.texts:
                self.fig.draw_artist(text)
            # lines
            for line in ax.lines:
                self.fig.draw_artist(line)
            for spine in ax.spines:
                self.fig.draw_artist(ax.spines[spine])
            # axis
            self.fig.draw_artist(ax.xaxis)
            self.fig.draw_artist(ax.yaxis)
        if blit:
            self.fig.canvas.blit()
        
    def Refresh_Alls(self, blit=True):
        self.Clear_White()
        self.Draw_Alls(blit)

    def Clear_PlotArea(self, blit=False):
        # plot area clear
        top = self.main_axes[0].get_window_extent().y0 + self.main_axes[0].get_window_extent().height
        bottom = self.main_axes[-1].get_window_extent().y0
        height = top - bottom
        
        left = self.main_axes[0].get_window_extent().x0
        width = self.main_axes[0].get_window_extent().width

        self.DrawRect(xy=(left, bottom), width=width, height=height)
        # clear xaxis
        ax = self.main_axes[-1]
        xtick_x0 = ax.get_xticklabels()[0].get_window_extent().x0
        xtick_x1 = ax.get_xticklabels()[-1].get_window_extent().x0 + ax.get_xticklabels()[-1].get_window_extent().width
        xtick_width = xtick_x1 - xtick_x0
        xtick_y0 = ax.get_xticklabels()[0].get_window_extent().y0
        xtick_y1 = ax.get_xticklabels()[-1].get_window_extent().y0 + ax.get_xticklabels()[-1].get_window_extent().height
        xtick_height = xtick_y1 - xtick_y0
        self.DrawRect(xy=(xtick_x0, xtick_y0), width=xtick_width, height=xtick_height)
        if blit:
            self.fig.canvas.blit()
    
   
    
    def Draw_Xs(self, blit=False):
        # main, foot, head, info, anno
        for ax in self.main_axes + [self.anno_ax, self.head_ax, self.foot_ax]:
            # texts
            for text in ax.texts:
                self.fig.draw_artist(text)
            # lines
            for line in ax.lines:
                self.fig.draw_artist(line)
        self.fig.draw_artist(self.main_axes[-1].xaxis)
        if blit:
            self.fig.canvas.blit()
        
    def Refresh_Xs(self, blit=True):
        self.Clear_PlotArea()
        self.Draw_Xs(blit)
        
    def SetVCursor(self, x_data):
        self.vcursor_x = x_data
        self.vcursor.set_visible(True)
        d = self.vcursor.get_data()
        self.vcursor.set_data(
            (
                x_data,
                x_data
            ),
            (
                d[1][0],
                d[1][1]

            )
        )
        print(d)
        #self.anno_ax.draw_artist(self.vcursor)
    
    
    def AddAnnotation(self):
        pass


    def onClick(self, e):
        self.click = True
        if e.inaxes == self.anno_ax:
            self.SetVCursor(e.xdata)
            self.set_values_at_vcursor(e.xdata)
            self.Refresh_Alls()
        return True

    def onClickRelease(self, e):
        print(e)
        self.click = False
        

    def onScroll(self, e):
        print(e)

        # get xlim        
        ax = self.main_axes[-1]
        xlim = ax.get_xlim()

        # set ranges
        if e.button == "down":
            if self.press_keys["control"]:
                if self.vcursor.get_visible() and self.vcursor_x >= xlim[0] and self.vcursor_x <= xlim[1]:
                    ax.set_xlim(
                        xlim[0] - (self.vcursor_x - xlim[0]) * 0.3, 
                        xlim[1] + (xlim[1] - self.vcursor_x) * 0.3
                    )
                else:
                    ax.set_xlim(
                        xlim[0] - (xlim[1]-xlim[0]) * 0.3,
                        xlim[1] + (xlim[1]-xlim[0]) * 0.3,
                    )
            else:
                ax.set_xlim(
                    xlim[0] + (xlim[1]-xlim[0]) * 0.3,
                    xlim[1] + (xlim[1]-xlim[0]) * 0.3,
                )
        elif e.button == "up":
            if self.press_keys["control"]:
                if self.vcursor.get_visible() and self.vcursor_x >= xlim[0] and self.vcursor_x <= xlim[1]:
                    ax.set_xlim(
                        xlim[0] + (self.vcursor_x - xlim[0]) * 0.3, 
                        xlim[1] - (xlim[1] - self.vcursor_x) * 0.3
                    )
                else:
                    ax.set_xlim(
                        xlim[0] + (xlim[1]-xlim[0]) * 0.3,
                        xlim[1] - (xlim[1]-xlim[0]) * 0.3,
                    )
            else:
                ax.set_xlim(
                    xlim[0] - (xlim[1]-xlim[0]) * 0.3,
                    xlim[1] - (xlim[1]-xlim[0]) * 0.3,
                )
        self.xlim = list(self.main_axes[-1].get_xlim())
        
        # set anno ax
        self.anno_ax.set_xlim(self.xlim)
        
        # refresh
        self.Refresh_Alls()
        

    def onMouseMove(self, e):
        print(e)
        if self.click == True and e.inaxes == self.anno_ax:
            self.SetVCursor(e.xdata)
            self.set_values_at_vcursor(e.xdata)
            self.Refresh_Alls()
        
    def onKeyPress(self, e):
        print(e, e.key)
        for key in e.key.split("+"):
            self.press_keys[key] = True
            if key == "ctrl":
                self.press_keys["control"] = True
        if self.press_keys["r"]:
            self.press_keys["control"] = False
            self.press_keys["r"] = False
            inter = Interactor()
            ret = inter.SignalSelector(self.AllSignalNames, self.PlotSignalNames)
            if ret[0] == True:
                print(ret[1])
                self.set_plot_signals(ret[1])
                self.Refresh_Alls()
        elif self.press_keys["t"]:
            pass
        elif self.press_keys["y"]:
            for ax in self.main_axes:
                for line in ax.lines:
                    if line.get_marker() == "None":
                        print("marker set")
                        line.set_marker("o")
                        line.set_markersize(3)
                    else:
                        print("marker unset")
                        line.set_marker("None")
            self.Refresh_Alls()
        elif self.press_keys["u"]:
            pass
        elif self.press_keys["i"]:
            pass
        elif self.press_keys["f5"]:
            self.fig.canvas.draw()

    def onKeyRelease(self, e):
        print(e, e.key)
        for key in e.key.split("+"):
            self.press_keys[key] = False
            if key == "ctrl":
                self.press_keys["control"] = False
            
        
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

def find_nearest_index_bisection(data_list, hook_value, eps=0.5):
    idx = bisect.bisect_right(data_list, hook_value)
    if idx == 0 or idx == len(data_list) - 1:
        return idx
    else:
        return idx-1
    if idx >= 0 and idx <= len(data_list) - 1 and data_list[idx] == hook_value:
        return idx
    neis = [float("inf"), float("inf"), float("inf")]
    if idx > 0:
        neis[0] = abs(data_list[idx-1] - hook_value)
    if idx >= 0 and idx <= len(data_list) - 1:
        neis[1] = abs(data_list[idx] - hook_value)
    if idx < len(data_list) - 1:
        neis[2] = abs(data_list[idx+1] - hook_value)
    nearest_idx = idx + neis.index(min(neis)) - 1
    if abs(data_list[nearest_idx] - hook_value) <= eps:
        print(nearest_idx)
        return nearest_idx
    else:
        print(None)
        return None

plter = MDFPlotter(mdfpath="sample.dat")