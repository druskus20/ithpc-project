
rm __pycache__ -rf
rm *.so
rm *.c
python setup.py build_ext --inplace
