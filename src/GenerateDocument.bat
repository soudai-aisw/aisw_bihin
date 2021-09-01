
cd ../
del /S /Q "./docs/_build"
sphinx-apidoc -F -H EquipmentBooking -A Helve -V v1.0 -o docs src


cd ./src
sphinx-build ../docs ../docs/_build

timeout 10
