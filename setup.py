from setuptools import setup, find_packages


setup(
    name="pyg4ometry",
    version="0.1.2",
    packages=find_packages(exclude=["docs", "tests"]),

    # Only tested with version 4.7.
    install_requires=["antlr4-python2-runtime == 4.7",
                      "matplotlib",
                      "networkx",
                      "numpy",
                      "vtk"],
    python_requires="==2.7.*", # refer to pep440 for writing these correctly

    author="Stuart D Walker",
    author_email="stuart.walker.2011@live.rhul.ac.uk",
    description='View FLUKA geometry meshes and convert to GDML.',
    license='GPL3',
    url='https://bitbucket.org/jairhul/pyfluka/',
    keywords='geometry bdsim particle physics accelerators',
)
