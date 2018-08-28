#Setup configuration. Made with lazypackage
from distutils.sysconfig import get_python_inc
from glob import glob

package_name = 'goodboyai'
version = '0.1'

#General_Configuration_________________________________________________
author = 'AUTHOR NAME HERE'
description = """ENTER DESCRIPTION HERE
Should include anything you want about your project.
"""

#Source_Configuration__________________________________________________
#Include directories:
build_include_dirs = ['goodboyai/include', get_python_inc(plat_specific='1')]
#Add this line to use another include directory
#build_include_dirs += ['path/to/include']

#Source files
build_sources = glob('goodboyai/lib/*.cpp')
build_sources += glob('goodboyai/lib/*.cxx')
#To add more sources, use this line 
	#to include all cpp files from a directory
#build_sources += glob('some/relative/path/*.cpp')

#Compiler arguments for compiling C++
extra_compile_args = ['-std=c++11']

#External_Libraries____________________________________________________
#Fully link to another C++ Lazypackage library
referenced_lazypackages = []

#Extra library directories
lib_dirs = ['/usr/local/lib']
#Add this line to use another library directory
#lib_dirs += ['/path/to/library']

#Referenced external libraries
libraries = []
#Add libraries to use to this list
#If the shared object is named libMyLibrary.so, write MyLibrary
#For example: libraries = ['MyLibrary', 'AnotherLibrary']

#Swig_Configuration____________________________________________________

#Swig header code
swig_header_code = """
"""
#Use this to write extra swig code at the head of the file.

#Swig footer code
swig_footer_code = """
"""
#Use this to add additional code at the end.

#Swig extra namespaces
swig_extra_namespaces = []
#Use this to use extra namespaces in the swig wrapper code.
