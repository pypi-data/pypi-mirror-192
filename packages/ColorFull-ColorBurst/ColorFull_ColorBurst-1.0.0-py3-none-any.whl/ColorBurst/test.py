# Importing required modules
from ColorBurst import ColorBurst, Colors, Decorations

# Initializing ColorBurst
color_print = ColorBurst()

# Printing Hello World in RED with GREEN background and ITALIC as style onto Terminal
color_print.colorize("Hello", "World", color=Colors.RED, background=Colors.GREEN, decoration=Decorations.ITALIC)

# RESETTING above text style
color_print.RESET

# Enabling AUTORESET
color_print.init(autoreset=True)

# RAPID BLINKING YELLOW colored Hello World on to Console
color_print.colorize("Hello", "World", color=Colors.YELLOW, decoration=Decorations.RAPID_BLINK)