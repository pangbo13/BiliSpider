@echo off
rmdir /S /Q dist
rmdir /S /Q build
rmdir /S /Q "./bilisplider/__pycache__"
del /Q "./bilisplider/tempCodeRunnerFile.py"

python setup.py sdist bdist_wheel
