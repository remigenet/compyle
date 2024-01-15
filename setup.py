from setuptools import setup, Command
from Cython.Build import cythonize
import sys, os
from setuptools.extension import Extension
from Cython.Compiler import Options
import argparse

Options.docstrings = False


script_name = os.environ.get('SCRIPT_NAME')  # Replace 'default_script.py' with a default script name
module_name = script_name 
if not script_name:
    print('NO SCRIPT NAME')
    exit()
if '/' in script_name:
    module_name = module_name.split('/')[-1]
module_name = module_name.split('.')[0]
# Select the compiler (e.g., gcc, clang)
print('module -', module_name)
os.environ["CC"] = "gcc"

# Define custom compile arguments
extra_compile_args = ["-Ofast", "-shared", "-pthread", "-march=native", "-ffast-math", "-fopenmp", "-fPIC", "-Wmissing-profile", "-mtune=native", "-pipe",  "-fuse-linker-plugin", "-ffat-lto-objects", "-fexpensive-optimizations", "-floop-optimize", "-floop-nest-optimize", "-ftree-vectorize", "-fPIE", "-fbranch-probabilities", "-fbranch-target-load-optimize", "-fbranch-target-load-optimize2", "-fcrossjumping", "-fipa-profile", "-fpeel-loops", "-fpeephole"]
extra_link_args = []  # You can add custom link arguments here

# Define extensions
extensions = [
    Extension(module_name, [script_name],
              extra_compile_args=extra_compile_args,
              extra_link_args=extra_link_args)
]

class RunCommand(Command):
    """Custom command to build and run the module."""

    description = "Build and run the Cython module"
    user_options = []
 
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # Build the module
        self.reinitialize_command('build_ext', inplace=True)
        self.run_command('build_ext')

        # Import and run the module
        import module_name  # Replace with your module's name
        # module_name.main()  # Replace with your module's main function or desired entry point


compiler_directives = {
    'language_level': "3",
    'infer_types': True,
    'c_api_binop_methods': True,
}

setup(
    name=script_name,
    ext_modules=cythonize(extensions, annotate=True, compiler_directives=compiler_directives),
    zip_safe=False,
    cmdclass={
        'run': RunCommand,
    }
)
