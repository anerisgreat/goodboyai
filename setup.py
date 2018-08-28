#Setup script. Made with lazypackage

import setup_config
import fnmatch
import re
import os
from os.path import join as pathjoin
import ntpath
from glob import glob
from distutils.sysconfig import get_python_inc
import shutil
import sys
from setuptools import find_packages
from distutils.core import setup, Extension
from distutils.command.build_ext import build_ext as _build_ext

#Returns using tags in given a header file name.
def get_using_names(filename, include_dirs):
	ret_arr = []
	using_quotes_regex = re.compile(r"(?:#include\s*\")([^\s\">]*)\"") #Including ""
	using_brackets_regex = re.compile(r"(?:#include\s*<)([^\s\">]*)>") #Including <>
	found_flag = False
	for include_dir in include_dirs:
		full_path = pathjoin(include_dir, filename)
		if os.path.exists(full_path):
			found_flag = True
			with open(full_path) as header_file:
				contents = header_file.read()
				ret_arr += using_quotes_regex.findall(contents)
				ret_arr += using_brackets_regex.findall(contents)
	return ret_arr

#Checks if header A uses header B.
def check_does_use(headera, headerb):
	for usingheader in headera['using']:
		if ((usingheader != '') and (headerb['filename'] != '') and
			((usingheader == headerb['filename']) or
			(usingheader == ntpath.basename(headerb['filename']))
				)):
				return True
	return False

def get_ordered_header_names(header_names, include_dirs):
	using_file_map = [{	'filename' 	: header_name,
						'using' 	: get_using_names(header_name, include_dirs)}
		for header_name in header_names]

	for i in range(len(using_file_map)):
		for j in reversed(range(len(using_file_map))):
			for k in reversed(range(j)):
				if check_does_use(using_file_map[j], using_file_map[k]):
					tmp = using_file_map[j]
					using_file_map.remove(tmp)
					using_file_map.insert(k, tmp)

	return list(reversed([using_file['filename'] for using_file in using_file_map]))

def get_headers_from_lazypackage(package):
	pathname = pathjoin(get_python_inc(plat_specific='1'),package)
	print('Scanning headers of package: ' + package + ' in ' + pathname)
	headers = [pathjoin(package, ntpath.basename(headerfile)) for headerfile in glob(pathjoin(pathname, '*.h'))]
	headers += [pathjoin(package, ntpath.basename(headerfile)) for headerfile in glob(pathjoin(pathname, '*.hpp'))]

	return get_ordered_header_names(headers, [get_python_inc(plat_specific='1')])

def get_headers_from_local_package():
	header_names = [ntpath.basename(full_name) for full_name in glob(setup_config.package_name + '/include/*.h')]
	header_names += [ntpath.basename(full_name) for full_name in glob(setup_config.package_name + '/include/*.hpp')]
	return get_ordered_header_names(header_names, setup_config.build_include_dirs)

#Generates swig file
def gen_swig():
	print('Generating swig .i file.')

	#Loading local headers
	print('Detected package: ' + setup_config.package_name)
	package_header_names = get_headers_from_local_package()

	#Loading headers for all used packages
	lazypackage_header_vector = []
	for package in setup_config.referenced_lazypackages:
		lazypackage_header_vector.append({ 'package': package,
							'headers' : get_headers_from_lazypackage(package)})

	print('Lazypackage headers to include:')
	for package_headers_dict in lazypackage_header_vector:
		for header_name in package_headers_dict['headers']:
			print('<' + header_name + '>')
	print('Local package headers to include:')
	for header in package_header_names:
		print('<' + pathjoin(setup_config.package_name, header) + '>')

	print('Headers to include by order: ')
	for header_name in package_header_names:
		print(header_name)
	print('Starting..')

	i_file = open((setup_config.package_name + '/' + setup_config.package_name + '.i'), 'w')
	i_file.write("""%include <std_string.i>
%include <std_vector.i>
%template(StringVector) std::vector<std::string>;
%template(IntVector) std::vector<int>;
%template(DoubleVector) std::vector<double>;
%template(FloatVector) std::vector<float>;
%template(CharVector) std::vector<char>;
//Begin extra header code
""")
	i_file.write(setup_config.swig_header_code)
	i_file.write("//End extra header code\n")

	for package_headers_dict in lazypackage_header_vector:
		for header_name in package_headers_dict['headers']:
			i_file.write("%import(module=\"" + package_headers_dict['package'] + "\") <" + header_name + ">\n")

	i_file.write("""%feature("director");

%module(directors = "1") """ + setup_config.package_name + '\n')
	
	#Writing headers
	i_file.write('%{\n')

	for package_headers_dict in lazypackage_header_vector:
		for header_name in package_headers_dict['headers']:
			i_file.write('\t#include <' + header_name + '>\n')

	for header_name in package_header_names:
		i_file.write('\t#include <' + setup_config.package_name + '/' + header_name + '>\n')
	i_file.write('\tusing namespace ' + setup_config.package_name + ';\n')
	for namespace_name in setup_config.swig_extra_namespaces:
		i_file.write('\tusing namespace ' + namespace_name + ';\n')
	i_file.write('%}\n')
	
	i_file.write('\n')
	for header_name in package_header_names:
		i_file.write('%include <' + setup_config.package_name + '/' + header_name + '>\n')
	i_file.write('\n')
	i_file.write('//Begin extra footer code\n')
	i_file.write(setup_config.swig_footer_code)
	i_file.write('//End extra footer code\n')
	i_file.close()
	print('Swig .i file generation ended.')

def copy_headers():
	pathname = pathjoin(get_python_inc(plat_specific='1'),setup_config.package_name)
	print('Headers will go in: ' + pathname)
	if os.path.exists(pathname):
		shutil.rmtree(pathname)
	os.makedirs(pathname)
	package_include_path = pathjoin(setup_config.package_name, 'include')
	for filename in glob(pathjoin(package_include_path, '*')):
		print('Copying file \'' + filename + '\' to \'' + pathname + '\'.')
		shutil.copy(filename, pathname)


def copy_swig():
	pathname = pathjoin(get_python_inc(plat_specific='1'),setup_config.package_name)
	swigfile = pathjoin(setup_config.package_name, setup_config.package_name + '.i')
	print('Copying file \'' + swigfile + '\' to \'' + pathname + '\'.')
	shutil.copy(swigfile, pathname)

def get_all_files_from_dir(dirname):
	results = []
	for root, dirnames, filenames in os.walk(dirname):
		for filename in fnmatch.filter(filenames, '*'):
			results.append(pathjoin(root, filename))
	return results

def is_cpp():
	package_name = setup_config.package_name
	sources = setup_config.build_sources
	headers = get_headers_from_local_package()

	return ((len(sources) != 0) or (len(headers) != 0))

def get_sources():
	if(is_cpp()):
		return setup_config.build_sources + [(pathjoin(setup_config.package_name, setup_config.package_name) + '.i')]
	else:
		return setup_config.build_sources

class build_ext(_build_ext):
	def run(self):
		if (is_cpp()):
			copy_headers()
			gen_swig()
			_build_ext.run(self)
			copy_swig()
		else:
			_build_ext.run(self)

package_extention = Extension(('_' + setup_config.package_name),
	sources = get_sources(),
	include_dirs = setup_config.build_include_dirs,
	libraries = setup_config.libraries + [(':_' + lazym + '.so') for lazym in setup_config.referenced_lazypackages],
	library_dirs = setup_config.lib_dirs + sys.path,
	runtime_library_dirs = setup_config.lib_dirs + sys.path,
	extra_compile_args = setup_config.extra_compile_args,
	swig_opts = ['-c++', '-modern'] + ['-I'+build_include_dir for build_include_dir in setup_config.build_include_dirs]
	)

def get_extention():
	if (is_cpp()):
		return [package_extention]
	return []

setup(
	name = setup_config.package_name,
	version	= setup_config.version,
	author = setup_config.author,
	description = setup_config.description,
	ext_modules = get_extention(),
	packages = find_packages(),
	package_data = {'':get_all_files_from_dir(setup_config.package_name)},
	include_package_data = True,
	cmdclass = {
		'build_ext' : build_ext
	},
	entry_points = {
		'console_scripts': [
		(setup_config.package_name + '='+ setup_config.package_name + '.__main__:main'),
		],
	},
	install_requires=[],
	)
