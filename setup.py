from setuptools import setup, find_packages

setup(
    name="pyfluka",
    version="0.3.0",
    packages=find_packages(),

    # Only tested with version 4.7.
    install_requires=["antlr4-python2-runtime == 4.7"],
    python_requires="==2.7.*", # refer to pep440 for writing these correctly

    author="Stuart D. Walker",
    author_email="stuart.walker.2011@live.rhul.ac.uk",
    description='View FLUKA geometry meshes and convert to GDML.',
    url='https://bitbucket.org/jairhul/pyfluka/',
)
