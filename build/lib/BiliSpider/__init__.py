from .bilispider import *
def main():
    from .start import start
    start()

from .version import version
__version__ = version
name = 'bilispider'
__all__ = ['bilispider']
