def main():
    from .start import start
    start()

from .version import version
name = 'bilispider'

__all__ = ['bilispider']

from .bilispider import *
