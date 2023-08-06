from setuptools import setup, Extension

bitweb2_yescryptr16_module = Extension('bitweb2_yescryptr16',
                            sources = ['yespower-module.c',
                                       'yespower.c',
                                       'yespower-opt.c',
                                       'sha256.c'
                                       ],
                            extra_compile_args=['-O2', '-funroll-loops', '-fomit-frame-pointer'],
                            include_dirs=['.'])

setup (name = 'bitweb2_yescryptr16',
       version = '1.0.5',
       author_email = 'mraksoll4@gmail.com',
       author = 'mraksoll',
       url = 'https://github.com/bitweb-project/bitweb2_yescryptr16_python3',
       description = 'Bindings for yespower-0.5 or yescryptr16 proof of work used by bitweb at GPU enable update',
       ext_modules = [bitweb2_yescryptr16_module])
