from distutils.core import setup, Extension

ctime_ext_module = Extension('ctime_binding', sources = ['ctime-binding.c'])

setup (name = 'ctime_binding', version = '1.0', description = 'A binding of the ctime library', ext_modules = [ctime_ext_module])