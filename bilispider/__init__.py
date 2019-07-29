#from __future__ import absolute_import

def main():
    from .start import start
    start()

with open('verson','r') as f:
    version = f.read()
name = 'bilispider'

from .bilispider import *
