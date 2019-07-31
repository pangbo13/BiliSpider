@echo off
rmdir /S /Q dist
rmdir /S /Q build

python setup.py sdist bdist_wheel