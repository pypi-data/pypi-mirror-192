from typing import Dict, Literal, Union, Callable
from dataclasses import dataclass
__all__ = ['Colors', 'Decorations', 'ColorBurst', 'TextProperty']
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
@dataclass
class TextProperty:
    color: Colors = None
    background: Colors = None
    decoration: Decorations = None
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
    def coloredInput(self, prompt: str = '', promptProperty: Union[Dict[str, Literal['color', 'background', 'decoration']], TextProperty] = TextProperty, textProperty: Union[TextProperty, Dict[str, Literal['color', 'background', 'decoration']]] = TextProperty, text_style: bool =  False, type_: Callable = None):
        """You can now take ask colorfull question to your users

        Args:
            prompt (str): Question or Text to display as Input Prompt
            promptProperty (Union[Dict[str, Literal[&#39;color&#39;, &#39;background&#39;, &#39;decoration&#39;]], TextProperty], optional): Property (color, background and decoration) of prompt text. Defaults to TextProperty.
            textProperty (Union[TextProperty, Dict[str, Literal[&#39;color&#39;, &#39;background&#39;, &#39;decoration&#39;]]], optional): Property (color, background, and decoration) of user-input texts. Defaults to TextProperty.
            text_style (bool, optional): Set True you you want user-input to be colorfull too. Defaults to False.
            type_ (Callable, optional): What type you want your query to such as int, float or str (default). Defaults to None.

        Returns:
            any: String if not type_ passed otherwise the type passed will be returned
        """
        if (isinstance(promptProperty, type)):
            promptProperty = promptProperty()
        if isinstance(promptProperty, TextProperty):
            prompt_color = promptProperty.color
            prompt_back = promptProperty.background
            prompt_decc = promptProperty.decoration
        else:
            prompt_color = promptProperty.get('color', None)
            prompt_back = promptProperty.get('background', None)
            prompt_decc = promptProperty.get('decoration', None)
        
        prompt_color = ';' + getattr(self.__Colors, prompt_color) if prompt_color else self.__color
        prompt_back = ';' + getattr(self.__Background, prompt_back) if prompt_back else self.__background
        prompt_decc = getattr(self.__Decorations, prompt_decc) if prompt_decc else self.__decoration
        
        text_code = ''
        if text_style:
            if (isinstance(textProperty, type)):
                textProperty = textProperty()
            if isinstance(textProperty, TextProperty):
                text_color = textProperty.color
                text_back = textProperty.background
                text_decc = textProperty.decoration
            else:
                text_color = textProperty.get('color', None)
                text_back = textProperty.get('background', None)
                text_decc = textProperty.get('decoration', None)
            
            text_color = ';' + getattr(self.__Colors, text_color) if text_color else self.__color
            text_back = ';' + getattr(self.__Background, text_back) if text_back else self.__background
            text_decc = getattr(self.__Decorations, text_decc) if text_decc else self.__decoration

            text_code = self.__RESET + f"{self.__START}{text_decc}{text_color}{text_back}m"
        query = input(f"{self.__START}{prompt_decc}{prompt_color}{prompt_back}m{prompt}{text_code}")
        self.RESET
        return type_(query) if type_ else query
    def getProperty(self, color: Colors = None, background: Colors = None, decoration: Decorations = None) -> dict:
        """Generate Argument for the coloredInput's promptProperty or textProperty

        Args:
            color (Colors, optional): Color for the text. Defaults to None.
            background (Colors, optional): Background for the text. Defaults to None.
            decoration (Decorations, optional): Decoration for the text. Defaults to None.

        Returns:
            TextProperty: Property for the text
        """
        return TextProperty(color=color, background=background, decoration=decoration)
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
    print(color_print.coloredInput("What is your name? ", promptProperty={
        "color": "RED"
    }))
    print(color_print.coloredInput("What? ", TextProperty(background='RED'), color_print.getProperty(color='CYAN'), text_style=True))