install:
	pip install . --user

uninstall:
	pip uninstall pyg4ometry

develop:
	pip install --editable . --user

build_ext:
	python setup.py build_ext --inplace

# bumpversion is a python utility available via pip.  Make sure to add
# your pip user install location's bin directory to your PATH.
bump-major:
	bumpversion major setup.py setup.cfg

bump-minor:
	bumpversion minor setup.py setup.cfg

bump-patch:
	bumpversion patch setup.py setup.cfg

pypi-upload:
	python setup.py sdist bdist_wheel; \
	twine upload --repository pypi dist/*

