import sys

class Colorizer:

    _colors = {
        "black": '\033[30m',
        "red": '\033[31m',
        "green": '\033[32m',
        "yellow": '\033[33m',
        "blue": '\033[34m',
        "magenta": '\033[35m',
        "cyan": '\033[36m',
        "white": '\033[37m',
        "light_gray": '\033[90m',
        "light_red": '\033[91m',
        "light_green": '\033[92m',
        "light_yellow": '\033[93m',
        "light_blue": '\033[94m',
        "light_magenta": '\033[95m',
        "light_cyan": '\033[96m',
        "light_white": '\033[97m'
    }

    def __init__(self, color='red'):
        self.__color = self.validator(color)


    @classmethod
    def validator(cls, color: str):
        if color.lower() not in cls._colors:
            raise ValueError(f'Color not supported. Select color {list(cls._colors.keys())}')
        return cls._colors.get(color.lower())


    def __enter__(self):
        sys.stdout.write(self.__color)
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.write('\033[0m')
        return False