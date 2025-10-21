"""
 - write coloured message on screen.

 https://misc.flogisoft.com/bash/tip_colors_and_formatting

"""
#
#   @date   : February 2020
#   @author : Christophe.airiau@imft.fr
#   correction : october 2021, august 2022


import sys

BLACK = "\033[1;30m"
RED = "\033[1;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
MAGENTA = "\033[1;35m"
CYAN = "\033[1;36m"
WHITE = "\033[1;37m"

LIGHT_BLACK = "\033[1;90m"
LIGHT_RED = "\033[1;91m"
LIGHT_GREEN = "\033[0;92m"
LIGHT_YELLOW = "\033[1;93m"
LIGHT_BLUE = "\033[1;94m"
LIGHT_MAGENTA = "\033[1;95m"
LIGHT_CYAN = "\033[1;96m"
LIGHT_WHITE = "\033[1;97m"

RESET = "\033[0;0m"
BOLD = "\033[;1m"
REVERSE = "\033[;7m"
COLOR = ("\033[1;91m", "\033[1;92m", "\033[1;93m", "\033[1;94m", "\033[1;95m",
         "\033[1;96m", "\033[1;97m")

__dic_color__ = {"black": BLACK, "red": RED,  "green": GREEN,
                 "yellow": YELLOW, "blue": BLUE, "magenta": MAGENTA,
                 "cyan": REVERSE + CYAN, "white": WHITE, "bold": BOLD,
                 "light_black": LIGHT_BLACK, "light_red": LIGHT_RED,
                 "light_green": LIGHT_GREEN, "light_yellow": LIGHT_YELLOW,
                 "light_blue": LIGHT_BLUE, "light_magenta": LIGHT_MAGENTA,
                 "light_cyan": LIGHT_CYAN, "light_white": LIGHT_WHITE
                 }


def color_s(msg, color):
    """
    to get a colored message
    Parameters
    ----------
    msg : string
        a message
    color : string
        message color.

    Returns
    -------
    string
        the colored message

    """
    start = __dic_color__[color]
    end = "\x1b[0m"
    return start + msg + end


def set_title(msg):
    """Set a title"""
    sys.stdout.write(BLUE)
    print('#', 60 * '*')
    print('# %s' % msg)
    print('#', 60 * '*', '\n')
    sys.stdout.write(RESET)


def set_question(msg):
    """Set a question """
    print()
    print('#', 50 * '=')
    print('# Question n° %s' % msg)
    print('#', 50 * '=', '\n')


def set_section(msg):
    """Set an section message"""
    print()
    sys.stdout.write(GREEN)
    print('#', 50 * '=')
    print('# Section :  %s' % msg)
    print('#', 50 * '=', '\n')
    sys.stdout.write(RESET)


def set_alert(msg):
    """Set an alert message"""
    print()
    sys.stdout.write(LIGHT_RED)
    print('#', 50 * '=')
    print('# ALERT :  %s' % msg)
    print('#', 50 * '=', '\n')
    sys.stdout.write(RESET)


def set_info(msg, char="=", color="red"):
    """Set a information"""
    print()

    sys.stdout.write(__dic_color__[color])
    print('#', 50 * char)
    print('# INFO :  %s' % msg)
    print('#', 50 * char, '\n')
    sys.stdout.write(RESET)


def set_msg(msg, color="magenta"):
    """ display a colored message """
    sys.stdout.write(__dic_color__[color])
    print(msg)
    sys.stdout.write(RESET)


def set_line(char="-", n=50, color="red"):
    """Set a information"""
    sys.stdout.write(__dic_color__[color])
    print('#', n * char)
    sys.stdout.write(RESET)


def test_color(msg):
    """
    test of possible foreground colors in a terminal
    """
    set_title("test colored text")
    set_info("bold:", color="green")
    for i in range(1, 8):
        COLOR = "\033[1;3%im" % i
        sys.stdout.write(COLOR)
        print(msg + "\n")
        sys.stdout.write(RESET)

    print("="*50)
    set_info("light colored, bold:", color="green")
    set_msg("sometimes it does not work !")
    for i in range(1, 8):
        COLOR = "\033[1;9%im" % i
        sys.stdout.write(COLOR)
        print(msg + "\n")
        sys.stdout.write(RESET)

    set_info("normal:", color="green")

    for i in range(1, 8):
        COLOR = "\033[2;3%im" % i
        sys.stdout.write(COLOR)
        print(msg + "\n")
        sys.stdout.write(RESET)

    print("=" * 50)

    set_info("underlined:", color="green")

    for i in range(1, 8):
        COLOR = "\033[4;3%im" % i
        sys.stdout.write(COLOR)
        print(msg + "\n")
        sys.stdout.write(RESET)

    print("=" * 50)
    set_info("blink:", color="green")
    for i in range(1, 8):
        COLOR = "\033[5;3%im" % i
        sys.stdout.write(COLOR)
        print(msg + "\n")
        sys.stdout.write(RESET)
    print("=" * 50)

    set_info("reversed:", color="green")
    for i in range(1, 8):
        COLOR = "\033[7;3%im" % i
        sys.stdout.write(COLOR)
        print(msg + "\n")
        sys.stdout.write(RESET)
    print("=" * 50)

    set_info("an information", color="magenta")
    set_msg(" a message ", color="cyan")
    set_alert("an alert")
    set_section("a section")
    set_title("a title")
    set_line()


if __name__ == '__main__':
    test_color("color tests")
