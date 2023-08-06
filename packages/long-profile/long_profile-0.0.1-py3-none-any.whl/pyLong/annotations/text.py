import json

from matplotlib.text import Text as mpl_Text
from matplotlib.axes import Subplot

from pyLong.annotations.annotation import Annotation
from pyLong.dictionnaries.colors import colors
from pyLong.lists.fonts import font_styles, font_weights
from pyLong.profiles.zprofile import zProfile


class Text(Annotation):
    def __init__(self):
        Annotation.__init__(self)

        self._name = "new text"

        self._text = ""

        self._xy = (500., 500.)
        
        self._rotation = 0.

        self._annotation = mpl_Text(0,
                                    0,
                                    "",
                                    rotation=0,
                                    rotation_mode="anchor",
                                    horizontalalignment="left",
                                    verticalalignment="baseline")

        self._font_size = 11.

        self._font_color = "Black"

        self._font_style = "normal"

        self._font_weight = "normal"

    """
    Methods:
    - clear
    - copy_style
    - duplicate
    - export_style
    - import_style
    - plot
    - reverse
    - update
    """

    def clear(self):
        """
        clear annotation

        returns:
        - None - NoneType
        
        """
        self._annotation = mpl_Text(0,
                                    0,
                                    "",
                                    rotation=0,
                                    rotation_mode="anchor",
                                    horizontalalignment="left",
                                    verticalalignment="baseline")

    def copy_style(self, annotation):
        """
        copy the style of a text annotation

        arguments:
        - annotation: annotation whose style is to be copied - Text

        returns:
        - True if success - bool
        - False else - bool

        examples:
        >>> new_annotation.copy_style(annotation)
        
        """
        if isinstance(annotation, Text):
            self._font_size = annotation.font_size
            self._font_color = annotation.font_color
            self._font_style = annotation.font_style
            self._font_weight = annotation.font_weight
            self._rotation = annotation.rotation
            self._opacity = annotation.opacity
            self._order = annotation.order
            return True
        else:
            return False

    def duplicate(self):
        """
        duplicate the annotation

        returns:
        - new_annotation: duplicated annotation - Text

        examples:
        >>> new_annotation = annotation.duplicate()
        
        """
        new_annotation = Text()
        new_annotation.copy_style(self)

        new_annotation.name = f"{self._name} duplicated"
        new_annotation.text = self._text

        new_annotation.xy = self._xy
        new_annotation.rotation = self._rotation

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
        - new_annotation: reversed annotation - Text
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
        self._annotation.set_text(self._text)
        self._annotation.set_x(self._xy[0])
        self._annotation.set_y(self._xy[1])
        self._annotation.set_fontsize(self._font_size)
        self._annotation.set_fontstyle(self._font_style)
        self._annotation.set_color(colors[self._font_color])
        self._annotation.set_fontweight(self._font_weight)
        self._annotation.set_rotation(self._rotation)
        self._annotation.set_alpha(self._opacity)
        self._annotation.set_zorder(self._order)
        self._annotation.set_visible(self._visible and self._active)

    def __repr__(self):
        return f"{self._name}"

    def __getstate__(self):
        attributes = dict(self.__dict__)
        attributes["_annotation"] = mpl_Text(0,
                                             0,
                                             "",
                                             rotation=0,
                                             rotation_mode="anchor",
                                             horizontalalignment="left",
                                             verticalalignment="baseline")

        return attributes

    @property
    def xy(self):
        return self._xy

    @xy.setter
    def xy(self, xy):
        if not isinstance(xy, tuple):
            return

        if not len(xy) > 1:
            return

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
        if isinstance(z, (int, float)):
            self._xy = (self._xy[0], y)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        if isinstance(text, str):
            self._text = text
            
    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, rotation):
        if isinstance(rotation, (int, float)):
            if 0 <= rotation <= 360:
                self._rotation = rotation

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
