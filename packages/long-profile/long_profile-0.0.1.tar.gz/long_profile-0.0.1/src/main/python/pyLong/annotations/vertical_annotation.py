import json

from matplotlib.text import Annotation as mpl_Annotation
from matplotlib.axes import Subplot

from pyLong.annotations.annotation import Annotation
from pyLong.dictionnaries.styles import line_styles
from pyLong.dictionnaries.colors import colors
from pyLong.lists.arrows import arrow_styles
from pyLong.lists.fonts import font_styles, font_weights
from pyLong.profiles.zprofile import zProfile


class VerticalAnnotation(Annotation):
    def __init__(self):
        Annotation.__init__(self)

        self._name = "new vertical annotation"

        self._text = ""

        self._xy = (500., 500.)

        self._text_rotation = 90
        
        self._arrow_length = 100.

        self._vertical_shift = 0.
        
        self._annotation = mpl_Annotation("",
                                          xy=(0, 0),
                                          xytext=(0, 0),
                                          xycoords='data',
                                          rotation=90,
                                          horizontalalignment='center',
                                          verticalalignment='bottom',
                                          arrowprops=dict(arrowstyle='->'))

        self._font_size = 11.

        self._font_color = "Black"

        self._font_style = "normal"

        self._font_weight = "normal"

        self._arrow_style = "-|>"

        self._arrow_line_style = "solid"

        self._arrow_color = "Black"
        
        self._arrow_thickness = 1.        

    """
    Methods:
    - adjust
    - clear
    - copy_style
    - duplicate
    - export_style
    - import_style
    - plot
    - reverse
    - update
    """

    def adjust(self, zprofile):
        """
        adjust the annotation position on a zprofile

        arguments:
        - zprofile: profile on which the annotation is to be adjusted

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> annotation.adjust(zprofile)
        
        """
        if not isinstance(zprofile, zProfile):
            return False
        elif zprofile.interpolate(self.x):
            self.y = zprofile.interpolate(self.x)
            return True
        else:
            return False

    def clear(self):
        """
        clear annotation

        returns:
        - None - NoneType
        
        """
        self._annotation = mpl_Annotation("",
                                          xy=(0, 0),
                                          xytext=(0, 0),
                                          xycoords='data',
                                          rotation=90,
                                          horizontalalignment='center',
                                          verticalalignment='bottom',
                                          arrowprops=dict(arrowstyle='->'))

    def copy_style(self, annotation):
        """
        copy the style of a vertical annotation

        arguments:
        - annotation: annotation whose style is to be copied - VerticalAnnotation

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> new_annotation.copy_style(annotation)
        
        """
        if isinstance(annotation, VerticalAnnotation):
            self._font_size = annotation.font_size
            self._font_color = annotation.font_color
            self._font_style = annotation.font_style
            self._font_weight = annotation.font_weight
            self._arrow_style = annotation.arrow_style
            self._line_style = annotation.line_style
            self._arrow_color = annotation.arrow_color
            self._arrow_thickness = annotation.arrow_thickness
            self._opacity = annotation.opacity
            self._order = annotation.order
            return True
        else:
            return False

    def duplicate(self):
        """
        duplicate the annotation

        returns:
        - new_annotation: duplicated annotation - VerticalAnnotation

        examples:
        >>> new_annotation = annotation.duplicate()
        
        """
        new_annotation = VerticalAnnotation()
        new_annotation.copy_style(self)

        new_annotation.name = f"{self._name} duplicated"
        new_annotation.text = self._text

        new_annotation.xy = self._xy

        return new_annotation

    def export_style(self, filename):
        """
        export annotation style to a .json file

        arguments:
        - filename: .json file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> annotation.export_style("style.json")
        
        """
        if not isinstance(filename, str):
            return False
        elif not len(filename) > 0:
            return False
        else:
            style = {'font_size': self._font_size,
                     'font_color': self._font_color,
                     'font_style': self._font_style,
                     'font_weight': self._font_weight,
                     'arrow_style': self._arrow_style,
                     'line_style': self._line_style,
                     'arrow_color': self._arrow_color,
                     'arrow_thickness': self._arrow_thickness,
                     'opacity': self._opacity,
                     'order': self._order}
            try:
                with open(filename, 'w') as file:
                    json.dump(style, file, indent=0)
                    return True
            except:
                return False

    def import_style(self, filename):
        """
        import annotation style from a .json file

        arguments:
        - filename: .json file path - str

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> annotation.import_style("style.json")

        """
        if not isinstance(filename, str):
            return False
        elif not len(filename) > 0:
            return False
        else:
            try:
                with open(filename, 'r') as file:
                    style = json.load(file)
            except:
                return False

        if isinstance(style, dict):
            if 'font_size' in style.keys():
                self.font_size = style['font_size']
            if 'font_color' in style.keys():
                self.font_color = style['font_color']
            if 'font_style' in style.keys():
                self.font_style = style['font_style']
            if 'font_weight' in style.keys():
                self.font_weight = style['font_weight']
            if 'arrow_style' in style.keys():
                self.arrow_style = style['arrow_style']
            if 'line_style' in style.keys():
                self.line_style = style['line_style']
            if 'arrow_color' in style.keys():
                self.arrow_color = style['arrow_color']
            if 'arrow_thickness' in style.keys():
                self.arrow_thickness = style['arrow_thickness']
            if 'opacity' in style.keys():
                self.opacity = style['opacity']
            if 'order' in style.keys():
                self.order = style['order']
            return True
        else:
            return False

    def plot(self, ax):
        """
        plot annotation on a matplotlib subplot

        arguments:
        - ax: matplotlib subplot - matplotlib.axes._subplots.AxesSubplot

        returns:
        - None - NoneType
        
        examples:
        >>> from matplotlib import pyplot as plt
        >>> fig, ax = plt.subplots()
        >>> annotation.plot(ax)
        >>> plt.show()
        
        """
        if isinstance(ax, Subplot):
            self.clear()
            self.update()

            ax.add_artist(self._annotation)

    def reverse(self, zprofile):
        """
        reverse the annotation according to a reference profile

        arguments:
        - zprofile: reference profile to perform the reversing - zProfile

        returns:
        - new_annotation: reversed annotation - VerticalAnnotation
        or
        - None - NoneType

        examples:
        >>> new_annotation = annotation.reverse(zprofile)

        """
        if not isinstance(zprofile, zProfile):
            return
        else:
            new_annotation = self.duplicate()
            new_annotation.name = f"{self._name} reversed"

            x_mean = (min(zprofile.x) + max(zprofile.x)) / 2
            new_annotation.x = 2 * x_mean - self.x

            return new_annotation

    def update(self):
        """
        update annotation properties

        returns:
        - None - NoneType

        examples:
        >>> annotation.update()
        
        """  
        self._annotation.arrow_patch.set_arrowstyle(self._arrow_style)
        self._annotation.arrow_patch.set_linestyle(line_styles[self._arrow_line_style])
        self._annotation.arrow_patch.set_linewidth(self._arrow_thickness)
        self._annotation.arrow_patch.set_color(colors[self._arrow_color])
        self._annotation.arrow_patch.set_alpha(self._opacity)
        self._annotation.arrow_patch.set_zorder(self._order)        
        
        self._annotation.set_text(self._text)
        self._annotation.xy = (self._xy[0], self._xy[1] + self._vertical_shift)
        self._annotation.set_x(self._xy[0])
        self._annotation.set_y(self._xy[1] + self._arrow_length + self._vertical_shift)
        self._annotation.set_fontsize(self._font_size)
        self._annotation.set_color(colors[self._font_color])
        self._annotation.set_fontweight(self._font_weight)
        self._annotation.set_fontstyle(self._font_style)
        self._annotation.set_rotation(self._text_rotation)
        self._annotation.set_alpha(self._opacity)
        self._annotation.set_zorder(self._order)

        if self._arrow_length >= 0 :
            self._annotation.set_verticalalignment('bottom')
        else:
            self._annotation.set_verticalalignment('top')

        self._annotation.set_visible(self._visible and self._active)

    def __repr__(self):
        return f"{self._name}"

    def __getstate__(self):
        attributes = dict(self.__dict__)
        attributes["_annotation"] = mpl_Annotation("",
                                                   xy=(0, 0),
                                                   xytext=(0, 0),
                                                   xycoords='data',
                                                   rotation=90,
                                                   horizontalalignment='center',
                                                   verticalalignment='bottom',
                                                   arrowprops=dict(arrowstyle='->'))

        return attributes
    
    @property
    def xy(self):
        return self._xy

    @xy.setter
    def xy(self, xy):
        if not isinstance(xy, tuple):
            return
        elif not len(xy) > 1:
            return
        else:
            for value in xy:
                if not isinstance(value, (int, float)):
                    return

            self._xy = xy[0:2]

    @property
    def x(self):
        return self._xy[0]

    @x.setter
    def x(self, x):
        if isinstance(x, (int, float)):
            self._xy = (x, self._xy[1])

    @property
    def y(self):
        return self._xy[1]

    @y.setter
    def y(self, y):
        if isinstance(y, (int, float)):
            self._xy = (self._xy[0], y)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        if isinstance(text, str):
            self._text = text

    @property
    def text_rotation(self):
        return self._text_rotation

    @text_rotation.setter
    def text_rotation(self, rotation):
        if isinstance(rotation, (int)):
            if rotation in [0, 90]:
                self._text_rotation = rotation
                
    @property
    def arrow_length(self):
        return self._arrow_length

    @arrow_length.setter
    def arrow_length(self, length):
        if isinstance(length, (int, float)):
            self._arrow_length = length

    @property
    def vertical_shift(self):
        return self._vertical_shift

    @vertical_shift.setter
    def vertical_shift(self, shift):
        if isinstance(shift, (int, float)):
            self._vertical_shift = shift
                
    @property
    def annotation(self):
        return self._annotation

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, size):
        if isinstance(size, (int, float)):
            if 0 <= size:
                self._font_size = size

    @property
    def font_color(self):
        return self._font_color

    @font_color.setter
    def font_color(self, color):
        if color in colors.keys():
            self._font_color = color

    @property
    def font_style(self):
        return self._font_style

    @font_style.setter
    def font_style(self, style):
        if style in font_styles:
            self._font_style = style

    @property
    def font_weight(self):
        return self._font_weight

    @font_weight.setter
    def font_weight(self, weight):
        if weight in font_weights:
            self._font_weight = weight

    @property
    def arrow_style(self):
        return self._arrow_style

    @arrow_style.setter
    def arrow_style(self, style):
        if style in arrow_styles:
            self._arrow_style = style

    @property
    def arrow_line_style(self):
        return self._arrow_line_style

    @arrow_line_style.setter
    def arrow_line_style(self, style):
        if style in line_styles.keys():
            self._arrow_line_style = style

    @property
    def arrow_color(self):
        return self._arrow_color

    @arrow_color.setter
    def arrow_color(self, color):
        if color in colors.keys():
            self._arrow_color = color

    @property
    def arrow_thickness(self):
        return self._arrow_thickness

    @arrow_thickness.setter
    def arrow_thickness(self, thickness):
        if isinstance(thickness, (int, float)):
            if 0 <= thickness:
                self._arrow_thickness = thickness
