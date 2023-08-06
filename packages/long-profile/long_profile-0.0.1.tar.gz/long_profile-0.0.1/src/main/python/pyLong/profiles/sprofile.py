import os

from matplotlib.lines import Line2D as mpl_Line
from matplotlib.axes import Subplot
import numpy as np

from pyLong.profiles.zprofile import zProfile
from pyLong.dictionnaries.styles import marker_styles
from pyLong.dictionnaries.colors import colors

class sProfile:
    def __init__(self):
        self._name = "new slope profile"

        self._label = ""

        self._zprofile = zProfile()

        self._xzs = []

        self._line = mpl_Line([], [])
        
        self._line_percent = mpl_Line([], [])
        
        self._line_degree = mpl_Line([], [])
        
        self._trick_line = mpl_Line([], [])

        self._marker_style = "cross"

        self._marker_color = "Black"
        
        self._marker_size = 1.
        
        self._values_color = "Black"
        
        self._values_size = 9.

        self._values_shift = 0.
        
        self._values_shift_percent = 0.
        
        self._values_shift_degree = 0.

        self._opacity = 1.
        
        self._order = 1

        self._markers_visible = False
        
        self._values_visible = False

        self._active = True
        
    """
    Methods:
    - clear
    - copy_style
    - duplicate
    - export
    - export_style
    - import_style
    - listing
    - mean
    - plot
    - update
    """

    def clear(self):
        """
        clear lines

        returns:
        - None - NoneType

        examples:
        >>> sprofile.clear()
        
        """
        self._line = mpl_Line([], [])
        self._line_percent = mpl_Line([], [])
        self._line_degree = mpl_Line([], [])
        self._trick_line = mpl_Line([], [])
        
    def copy_style(self, sprofile):
        """
        copy the style of a slope profile

        arguments:
        - sprofile: slope profile whose style is to be copied - sProfile

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> new_sprofile.copy_style(sprofile)
        
        """
        if isinstance(sprofile, sProfile):
            self._marker_style = sprofile.marker_style
            self._marker_color = sprofile.marker_color
            self._marker_sier = sprofile.marker_size
            self._values_color = sprofile.values_color
            self._values_size = sprofile.values_size
            self._values_shift = sprofile.values_shift
            self._values_shift_percent = sprofile.values_shift_percent
            self._values_shift_degree = sprofile.values_shift_degree
            self._opacity = sprofile.opacity
            self._order = sprofile.order
            return True
        else:
            return False
    
    def export(self, filename, xz_decimals=3, s_decimals=3):        
        if not isinstance(filename, str) or not isintance(xz_decimals, int) or not isinstance(s_decimals, int):
            return False
        
        if len(filename) == 0:
            return False
        
        with open(filename, 'w') as file:
            file.write(f"X\tZ\tS\n")
            for x, z, s in self._xzs:
                file.write(f"{round(x, xz_decimals)}\t{round(z, xz_decimals)}\t{round(s, s_decimals)}\n")
                
            return True
    
    def export_style(self, filename):
        pass
    
    def import_style(self, filename):
        pass
    
    def listing(self, unit="%", decimals=3):
        if unit not in ["%", "°"]:
            return
        
        if not isinstance(decimals, int):
            return
        
        if not 0 <= decimals:
            return
        
        for i, (x, z, s) in enumerate(self._xzs):
            if unit == "%":
                print(f"vertice {i}: x = {round(x, 3)} m ; z = {round(z, 3)} m ; s = {round(self._signed_slopes[i] * 100, decimals)}%")
            else:
                print(f"vertice {i}: x = {round(x, 3)} m ; z = {round(z, 3)} m ; s = {round(np.degrees(np.arctan(self._signed_slopes[i])), decimals)}°")
    
    def mean(self, **kwargs):
        if "unit" not in kwargs.keys():
            return None
        
        if unit not in ["percent", "degree"]:
            return None
        
        self.update()

        x_zprofile = np.array([x for x, z in self._zprofile.xz])
        z_zprofile = np.array([z for x, z in self._zprofile.xz])

        s = np.array(self.s)
        
        d = np.sqrt((x_zprofile[1:] - x_zprofile[:-1])**2 + (z_zprofile[1:] - z_zprofile[:-1])**2)
        
        mean_slope = np.sum(s * d) / np.sum(d)
        
        if unit == "percent":
            return float(mean_slope) * 100.
        else:
            return float(np.degrees(np.arctan(mean_slope)))   
        
    def plot(self, ax, unit="percent", twin_ax=None, decimals=1):
        if not isinstance(ax, Subplot) or not isinstance(twin_ax, (type(None), Subplot)) or not isinstance(unit, str):
            return
        
        if unit not in ["percent", "degree"]:
            return
        
        self.clear()
        self.update()
        
        ax.add_line(self._trick_line)
        
        if not twin_ax:
            ax.add_line(self._line)
            
            if self._values_visible:
                if unit == "percent":
                    for i, slope in enumerate(self.slopes(unit="percent")):
                        ax.text(self._xzs[i][0],
                                self._xzs[i][1] + self._values_shift,
                                s=f"{round(slope, decimals)}%",
                                fontsize=self._values_size,
                                color=colors[self._values_color],
                                alpha=self._opacity,
                                horizontalalignment='center',
                                verticalalignment='center',
                                rotation=0,
                                zorder=self._order)
                        
                elif unit == "degree":
                    for i, slope in enumerate(self.slopes(unit="degree")):
                        ax.text(self._xzs[i][0],
                                self._xzs[i][1] + self._values_shift,
                                s=f"{round(slope, decimals)}°",
                                fontsize=self._values_size,
                                color=colors[self._values_color],
                                alpha=self._opacity,
                                horizontalalignment='center',
                                verticalalignment='center',
                                rotation=0,
                                zorder=self._order)
                        
        else:
            if unit == "percent":
                twin_ax.add_line(self._line_percent)
                if self._values_visible:
                    for i, slope in enumerate(self.slopes(unit="percent")):
                        if twin_ax.get_xlim()[0] <= slope <= twin_ax.get_xlim()[1]:
                            twin_ax.text(self._xzs[i][0],
                                         slope + self._values_shift_percent,
                                         s=f"{round(slope, decimals)}%",
                                         fontsize=self._values_size,
                                         color=colors[self._values_color],
                                         alpha=self._opacity,
                                         horizontalalignment='center',
                                         verticalalignment='bottom',
                                         zorder=self._order)

            else:
                twin_ax.add_line(self._line_degree)
                if self._values_visible:
                    for i, slope in enumerate(self.slopes(unit="degree")):
                        if twin_ax.get_xlim()[0] <= slope <= twin_ax.get_xlim()[1]:
                            twin_ax.text(self._xzs[i][0],
                                         slope + self._values_shift_degree,
                                         s=f"{round(slope, decimals)}°",
                                         fontsize=self._values_size,
                                         color=colors[self._values_color],
                                         alpha=self._opacity,
                                         horizontalalignment='center',
                                         verticalalignment='bottom',
                                         zorder=self._order)
                            
            
    def slopes(self, unit="percent"):
        if self._xzs == []:
            return None
        
        if unit not in ["percent", "degree"]:
            return None
        
        self.update_xzs()
        
        if unit == "percent":
            return [s*100 for x, z, s in self._xzs]
        else:
            s = [s for x, z, s in self._xzs]
            return list(np.degrees(np.arctan(np.array(s))))
        
    def update_xzs(self):
        if isinstance(self._zprofile, zProfile):
            x_zprofile = np.array(self._zprofile.x)
            z_zprofile = np.array(self._zprofile.z)

            x = list((x_zprofile[1:] + x_zprofile[:-1]) / 2)
            z = list((z_zprofile[1:] + z_zprofile[:-1]) / 2)
            s = list((z_zprofile[1:] - z_zprofile[:-1]) / (x_zprofile[1:] - x_zprofile[:-1]))

            self._xzs = [(x, z, s) for x, z, s in zip(x, z, s)]
            return True
        else:
            return False
        
            
    def update(self):
        if self.update_xzs():      
            self._line.set_data(self.x, self.z)
            self._line_percent.set_data(self.x, self.slopes(unit="percent"))
            self._line_degree.set_data(self.x, self.slopes(unit="degree"))

            self._line.set_label("")
            self._line_percent.set_label("")
            self._line_degree.set_label("")

            if self._active and self._markers_visible:
                self._trick_line.set_label(self._label)
            else:
                self._trick_line.set_label("")

            self._line.set_linestyle("None")
            self._line_percent.set_linestyle("None")
            self._line_degree.set_linestyle("None")
            self._trick_line.set_linestyle("None")

            self._line.set_marker(marker_styles[self._marker_style])
            self._line_percent.set_marker(marker_styles[self._marker_style])
            self._line_degree.set_marker(marker_styles[self._marker_style])
            self._trick_line.set_marker(marker_styles[self._marker_style])

            self._line.set_markeredgecolor(colors[self._marker_color])
            self._line_percent.set_markeredgecolor(colors[self._marker_color])
            self._line_degree.set_markeredgecolor(colors[self._marker_color])
            self._trick_line.set_markeredgecolor(colors[self._marker_color])

            self._line.set_markerfacecolor(colors[self._marker_color])
            self._line_percent.set_markerfacecolor(colors[self._marker_color])
            self._line_degree.set_markerfacecolor(colors[self._marker_color])
            self._trick_line.set_markerfacecolor(colors[self._marker_color])

            self._line.set_markersize(self._marker_size)
            self._line_percent.set_markersize(self._marker_size)
            self._line_degree.set_markersize(self._marker_size)
            self._trick_line.set_markersize(self._marker_size)

            self._line.set_alpha(self._opacity)
            self._line_percent.set_alpha(self._opacity)
            self._line_degree.set_alpha(self._opacity)
            self._trick_line.set_alpha(self._opacity)

            self._line.set_zorder(self._order)
            self._line_percent.set_zorder(self._order)
            self._line_degree.set_zorder(self._order)
            self._trick_line.set_zorder(self._order)

            self._line.set_visible(self._active and self._markers_visible)
            self._line_percent.set_visible(self._active and self._markers_visible)
            self._line_degree.set_visible(self._active and self._markers_visible)
            self._trick_line.set_visible(self._active and self._markers_visible)
    
    def __getstate__(self):
        attributes = dict(self.__dict__)
        attributes["_line"] = mpl_Line([], [])
        attributes["_line_percent"] = mpl_Line([], [])
        attributes["_line_degree"] = mpl_Line([], [])
        attributes["_trick_line"] = mpl_Line([], [])

        return attributes
    
    def __repr__(self):
        return f"{self._name}"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str):
            self._name = name

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        if isinstance(label, str):
            self._label = label

    @property
    def zprofile(self):
        return self._zprofile
    
    @zprofile.setter
    def zprofile(self, zprofile):
        if isinstance(zprofile, zProfile):
            self._zprofile = zprofile
            self.update()

    @property
    def xzs(self):
        return list(self._xzs)
    
    @property
    def x(self):
        return [x for x, z, s in self._xzs]
    
    @property
    def z(self):
        return [z for x, z, s in self._xzs]
    
    @property
    def s(self):
        return [s for x, z, s in self._xzs]

    @property
    def line(self):
        return str(self._line)

    @property
    def line_percent(self):
        return str(self._line_percent)

    @property
    def line_degree(self):
        return str(self._line_degree)

    @property
    def trick_line(self):
        return str(self._trick_line)

    @property
    def marker_style(self):
        return self._marker_style

    @marker_style.setter
    def marker_style(self, style):
        if style in marker_styles.keys():
            self._marker_style = style

    @property
    def marker_color(self):
        return self._marker_color

    @marker_color.setter
    def marker_color(self, color):
        if color in colors.keys():
            self._marker_color = color

    @property
    def marker_size(self):
        return self._marker_size

    @marker_size.setter
    def marker_size(self, size):
        if isinstance(size, (int, float)):
            if 0 <= size:
                self._marker_size = size

    @property
    def values_color(self):
        return self._values_color

    @values_color.setter
    def values_color(self, color):
        if color in colors.keys():
            self._values_color = color

    @property
    def values_size(self):
        return self._values_size

    @values_size.setter
    def values_size(self, size):
        if isinstance(size, (int, float)):
            if 0 <= size:
                self._values_size = size

    @property
    def values_shift(self):
        return self._values_shift

    @values_shift.setter
    def values_shift(self, shift):
        if isinstance(shift, (int, float)):
            self._values_shift = shift

    @property
    def values_shift_percent(self):
        return self.values_shift_percent

    @values_shift_percent.setter
    def values_shift_percent(self, shift):
        if isinstance(shift, (int, float)):
            self._values_shift_percent = shift

    @property
    def values_shift_degree(self):
        return self.values_shift_degree

    @values_shift_degree.setter
    def values_shift_degree(self, shift):
        if isinstance(shift, (int, float)):
            self._values_shift_degree = shift

    @property
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, opacity):
        if isinstance(opacity, (int, float)):
            if 0 <= opacity <= 1:
                self._opacity = opacity
    @property
    def order(self):
        return self._order
    
    @order.setter
    def order(self, order):
        if isinstance(order, int):
            if 0 < order:
                self._order = order

    @property
    def markers_visible(self):
        return self._markers_visible

    @markers_visible.setter
    def markers_visible(self, visible):
        if isinstance(visible, bool):
            self._markers_visible = visible

    @property
    def values_visible(self):
        return self._values_visible

    @values_visible.setter
    def values_visible(self, visible):
        if isinstance(visible, bool):
            self._values_visible = visible
    
    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, active):
        if isinstance(active, bool):
            self._active = active
