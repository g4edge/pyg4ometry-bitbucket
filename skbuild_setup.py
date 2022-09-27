import sys

import setuptools_scm  # noqa: F401
from setuptools import find_packages
from Cython.Build import cythonize

try:
    from skbuild import setup
except ImportError:
    print(
        "Please update pip, you need pip 10 or greater,\n"
        " or you need to install the PEP 518 requirements in pyproject.toml yourself",
        file=sys.stderr,
    )
    raise

if sys.platform.startswith("win32"):
    raise RuntimeError("Windows not supported!")

# https://scikit-build.readthedocs.io/en/stable/usage.html#setup-options
setup(
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    # package_data={}, # TODO
    # cmake_install_dir="src/pyg4ometry/pyoce", # what does this do?
    ext_modules=cythonize(["src/pyg4ometry/pycsg/geom.pyx", "src/pyg4ometry/pycsg/core.pyx"]) # still needed?
)
