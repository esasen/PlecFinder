rm cythonWM*.so
rm cythonWM*.c
python3 setup.py build_ext --inplace
mv *.so cythonWM.so




