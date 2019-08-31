@echo off
rmdir /S /Q dist
rmdir /S /Q build
cd bilispider
rmdir /S /Q __pycache__
del tempCodeRunnerFile.py
cd ..

python setup.py sdist bdist_wheel
