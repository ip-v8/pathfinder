from distutils.core import setup
from Cython.Build import cythonize
from Cython.Compiler import Options
from distutils.extension import Extension
from Cython.Distutils import build_ext



Options.docstrings = False


setup(
    name = 'Pathfinder',
    ext_modules=[
        Extension('test',
            sources=['pathfinder.pyx'],
            extra_compile_args=['-O3'],
            language='c',
            compiler_directives={
                "c_string_type":True,
                "infer_types":True,
            },
        ),
    ],
    cmdclass = {'build_ext': build_ext}
),

