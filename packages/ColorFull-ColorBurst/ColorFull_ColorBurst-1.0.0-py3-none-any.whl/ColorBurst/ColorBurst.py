__all__ = ['Colors', 'Decorations', 'ColorBurst']

class Colors:
    BLACK = 'BLACK'
    RED = 'RED'
    GREEN = 'GREEN'
    YELLOW = 'YELLOW'
    BLUE = 'BLUE'
    MAGENTA = 'MAGENTA'
    CYAN = 'CYAN'
    WHITE = 'WHITE'
class Decorations:
    NORMAL = 'NORMAL'
    BOLD = 'BOLD'
    DIM = 'DIM'
    ITALIC = 'ITALIC'
    UNDERLINE = 'UNDERLINE'
    DOUBLE_UNDERLINE = 'DOUBLE_UNDERLINE'
    SLOW_BLINK = 'SLOW_BLINK'
    RAPID_BLINK = 'RAPID_BLINK'
    REVERSED = 'REVERSED'
    TRANSPARENT = 'TRANSPARENT'
    STRIKE = 'STRIKE'
    NORMAL_INTENSITY = 'NORMAL_INTENSITY'
class ColorBurst:
    __START = '\u001b['
    __RESET = __START + '0m'
    class __Colors:
        BLACK = '30'
        RED = '31'
        GREEN = '32'
        YELLOW = '33'
        BLUE = '34'
        MAGENTA = '35'
        CYAN = '36'
        WHITE = '37'
    class __Background:
        BLACK = '40'
        RED = '41'
        GREEN = '42'
        YELLOW = '43'
        BLUE = '44'
        MAGENTA = '45'
        CYAN = '46'
        WHITE = '47'
    class __Decorations:
        NORMAL = '0'
        BOLD = '1'
        DIM = '2'
        ITALIC = '3'
        UNDERLINE = '4'
        DOUBLE_UNDERLINE = '21'
        SLOW_BLINK = '5'
        RAPID_BLINK = '6'
        REVERSED = '7'
        TRANSPARENT = '8'
        STRIKE = '9'
        NORMAL_INTENSITY = '22'
    def __init__(self) -> None:
        """Output Colored Text to STANDARD OUTPUT"""
        self.__reset = False
        self.__color = ''
        self.__background = ''
        self.__decoration = '0'
    def init(self, color: Colors = None, background: Colors = None, decoration: Decorations = None, autoreset = False):
        """
        This method is used to set or unset different parameter which are color, background and/or decoration as well as autoreset. 
        This method can be used to preserve value for above parameter so they can be used later without having to pass paramter 
        to colorize method explicitly
        
        When autoreset is set to True, it will immediately RESET the Colored Sequence right after line break otherwise current colored sequence remains as is unless updated
        Args:
            color (Colors, optional): represent foreground color. Defaults to None.
            background (Colors, optional): represent background color. Defaults to None.
            decoration (Decorations, optional): represent text style/decoration. Defaults to None.
            autoreset (bool, optional): represent condition to autoreset after line break or not. Defaults to False.
        """
        if autoreset:
            self.__reset = True
        if color:
            self.__color = ';' + getattr(self.__Colors, color)
        if background:
            self.__background = ';' + getattr(self.__Background, background)
        if decoration:
            self.__decoration = getattr(self.__Decorations, decoration)
            
    @property
    def RESET(self):
        print(f"{self.__RESET}", end='')
    def colorize(self, *args, color: Colors = None, background: Colors = None, decoration: Decorations = None, separator = None, end = None):
        """Output colorfull texts to Standard Output (Console)
        
        Args:
            Required
                args (any, required): set of strings; colorize("hello", "world",....n)
            Optional
                color (Colors, optional): Font (Foreground) color for texts. Defaults to Users' default.
                background (Colors, optional): Background color for texts. Defaults to Users' default.
                decoration (Decorations, optional): Font Style (Text Style) for text. Defaults to Decorations.NORMAL.
                separator (_type_, optional): Separator for different words (same as sep parameter in print function). Defaults to None.
                end (_type_, optional): What to print at the end of the line. Defaults to None.
        """
        color_ = ';' + getattr(self.__Colors, color) if color else self.__color
        background_ = ';' + getattr(self.__Background, background) if background else self.__background
        decoration_ = getattr(self.__Decorations, decoration) if decoration else self.__decoration
        separator = separator if separator else ' '
        if len(args) > 1:
            data = str(separator).join(args)
        else:
            data = args[0] if not len(args) == 0 else ''
        reset = ''
        if self.__reset:
            reset = self.__RESET
        print(f"{self.__START}{decoration_}{color_}{background_}m{data}", f"{reset}", end=end)

if __name__ == '__main__':
    color_print = ColorBurst()
    color_print.colorize("Hello", "World", color=Colors.RED, background=Colors.GREEN)
    color_print.RESET
    color_print.init(autoreset=True)
    color_print.colorize("Hello", "World", color=Colors.YELLOW)