#Setup bash script. Made with lazypackage
#At this point, install dependencies
sudo apt-get install -y python-pip swig

#These lines builds and installs your package
sudo python setup.py build_ext --inplace
sudo python -m pip uninstall -y goodboyai
sudo python -m pip install . --upgrade --verbose

#Cleanup
sudo rm -rf build
sudo rm *.pyc
sudo rm *.so
