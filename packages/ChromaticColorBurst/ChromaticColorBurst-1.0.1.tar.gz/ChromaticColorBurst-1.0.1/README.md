# ColorBurst - Stylish Output
  ColorBurst is a python module that provide method to print stylish text onto console without any setups. For example, you can print colored text or text with colored background or different styled text like bold, underlined, etc or with all these property with specified color and style for each

## Table of Contents
- [Installation](#installation "Installation")
- [Methods](#Methods "Methods")
  - [Colors](#Colors "Colors")
  - [Decorations](#Decorations "Decorations")
  - [TextProperty](#TextProperty "TextProperty")
  - [ColorBurst](#ColorBurst "ColorBurst")
- [Code](#Code "Code")
## Installation
  You can install this package using `pip` or directly from the github

  **Installing with `pip`**
  ```powershell
  pip install ChromaticColorBurst
  ```

  **Installing Directly from GitHub**
  ```powershell
  pip install git+https://github.com/sachin-acharya-projects/ColorBurst.git@master
  ```

  Or you can even download wheel file from [dist](/dist) folder and install it using
  ```powershell
  pip install wheel-file-name.whl
  ```
## Methods
  This package provide three classes which are Colors, Decorations and ColorBurst
#### Colors
  This is a namespace class that contains valid values for color and background parameter for ColorBurst.colorize method
  ````python
    Colors.RED # This equivalent to string 'RED'
  ````
#### Decorations
  This class contains valid values for decoration parameter for ColorBurst.colorize method
  ```python
  Decorations.BOLD # This equivalent to string 'BOLD'
  ```
#### TextProperty
  This is a dataclass that can contain values for different property for text like color, background and decoration
  *Usages*
  ```python
  # To access value
  TextProperty.color # returns default color value i.e. None if none assigned before

  # To change value
  TextPropery(color = 'RED').color # returns 'RED'
  ```
  There are three data kind it holds
  color of type `Colors`
  background of type `Colors`
  and decoration of type `Decorations`
#### ColorBurst
  This is the main class that can be used to print styled text onto console(Terminals). This class provides following three methods
1. **init(color: Colors = None, background: Colors = None, decoration: Decorations = None, autoreset = False)**  
      This method is used to set or unset different parameter which are color, background and/or decoration as well as autoreset. This method can be used to preserve value for above parameter so they can be used later without having to pass paramter to colorize method explicitly
*Example*
    ```python
    ColorBurst().init(
    	color = Colors.RED,
    	background = Colors.CYAN,
    	decoration = Decorations.DOUBLY_UNDERLINE,
    	autoreset = True
    )
    ```
    After calling init method like so, you can now simply call `ColorBurst().colorize("Hello", "World")` and it will print RED text with CYAN background with double underline. You can override these property for only one line by passing parameter explicitly or you can change these property for any next uses by re-using `init` method.  
    ```python
    """
    The code below will print YELLOW text with CYAN as background and DOUBLE UNDERLINE as Text Style
    CYAN as background and DOUBLE UNDERLINE as Text Style was stored in previous init method calls
    """
    ColorBurst.colorize("Hello", "World", color=Colors.YELLOW)
    ```
    Last parameter for this method, autoreset, if set to True, the color sequence will be terminated after line-break otherwise it will remains as is unless overriden or closing of terminal
    ```python
    c = ColorBurst()
    """
    The line below will print text with RED color but the foreground color will be kept RED even after the program is terminated. This can be override by using another color (New color will persist instead of RED) or closing the terminal.
    """
    c.colorize("Hello", "World", color = 'RED') # color = Colors.RED
    c.init(autoreset = True)
    """
    The line below will print text will CYAN color and terminated the coloring sequence. That means this CYAN color will only be available for current line/row (outputted row).
    """
    c.colorize("Hello", "There", color = 'CYAN') # Colors.CYAN
    ```
    **Parameters**
     - color  
     This parameter, type `Colors` represent foreground color. (Default: `None`)
     - background  
     This parameter, type `Colors` represent background color. (Default: `None`)
     - decoration  
     This parameter, type `Decorations` represent text style/decoration. (Default: `None`)
     - autoreset  
     This parameter, type `Boolean` represent condition to autoreset after line break or not. (Default: `False`)
2. **colorize(\*args, color: Colors = None, background: Colors = None, decoration: Decorations = None, separator = None, end = None)**  
    This method can be used to print stylish text onto screen.
    ````python
    ColorBurst().colorize(
    	"Hello", "World",
    	color = Colors.RED,
    	background = Colors.CYAN,
    	decoration = Decorations.BOLD,
    	separator = '-',
    	end = '\n'
    )
    ````
    Above code will print bold 'Hello-World\n' onto screen with color RED and background CYAN.
    __Parameters__
     - args (Type: `Tuple`)  
     These are the positional arguments which will be printed out onto screen. (Default: `''`)
     - color (Type: `Colors`)  
     Same as color parameter for `init` method. (Default: Terminals' default)
     - background (Type: `Colors`)  
     Same as background for `init` method. (Default: Terminals' default)
     - decoration (Type: `Decorations`)  
     Same as decoration parameter for `init` method. (Default: `Decorations.NORMAL`)
     - separator (Type: `String`)  
     This parameter represent separating character for each data in args parameter. (similar to `sep` parameter of `print` statement). (Default:  `' '`)
     - end (Type: `String`)  
     This parameter represent what to append at the end of the line. (Default: `\n`)
3. **RESET**  
    This method is used to reset any text formatting done. This is used when `autoreset` is set to `False` and need to terminate coloring sequence.
    *Example*
    The code below will print text will RED color and this foreground color will be persistent as autoreset is set to False
    ```python
    c = ColorBurst()
    c.colorize('Text', color = 'RED')
    ```
    Now if we use RESET method right after printing text, color sequence will be terminated and foreground color will be reverted to default
    ```python
    c = ColorBurst()
    c.colorize('Text', color = 'RED')
    c.RESET # Omit parenthesis
    ```
    This method is used to revert any formatting done to defaults.
4. **coloredInput**  
    This method is equivalent to input method but with colorfull prompt and/or input text
    *Example*
    Here is an example on how you can use this method  
    ```python
    c = ColorBurst()
    c.coloredInput(
      prompt = "What is your name? ", 
      promptProperty = c.getProperty(color = Colors.RED), # color = 'RED' 
      textProperty = TextPropery(color='YELLOW'), # color = Colors.YELLOW
      text_style = True
    )
    ```  
    The code above will prompt user with "What is your name? " in RED color and user can now write his name is YELLOW color. The way value are passed to parameter `promptProperty` and `textProperty`, you can use either way for any of them. If user-input is to be styled (textProperty to text effect), text_style must be set to True.
    __Parameters__  
    - prompt (str)  
    Question or Text to display as Input Prompt
    - promptProperty (Dict['color', 'background', 'decoration'] or TextProperty], optional)  
    Property (color, background and decoration) of prompt text. Defaults to TextProperty.
    - textProperty (Dict['color', 'background', 'decoration'] or TextProperty, optional)  
    Property (color, background, and decoration) of user-input texts. Defaults to TextProperty.
    - text_style (bool, optional)  
    Set True you you want user-input to be colorfull too. Defaults to False.
    - type_ (Callable, optional)  
    What type you want your user-input to be such as int, float or str (default). Defaults to None.
5. **getProperty**  
    This method is a wrapper of the value for parameter `promptProperty` and `textProperty` of `coloredInput` method. You can use this method in a alternative to TextProperty dataclass.  
    **Parameters**
    - color (Type: `Colors`)  
    Same as color parameter for `init` method. (Default: Terminals' default)
    - background (Type: `Colors`)  
    Same as background for `init` method. (Default: Terminals' default)
    - decoration (Type: `Decorations`)  
    Same as decoration parameter for `init` method. (Default: `Decorations.NORMAL`)

    _Returns TextProperty_
## Code
  ```python
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

  # To take the colorfull input from users
  color_print.coloredInput("What is your name? ", promptProperty = color_print.getProperty(color = Colors.RED), textProperty = TextProperty(color = 'YELLOW'), text_style = True)
  # Note: in above code, you can either use getProperty method from ColorBurst class or TextPropery dataclass for passing parameter to textPrompt and promptProperty and also text_style should be true inorder to textProperty take effects
  ```

[Go Up](#table-of-contents "Go Up")
