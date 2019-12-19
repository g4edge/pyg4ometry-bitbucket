import glob
import os
import sys
import importlib

# Skip modules with this string inside.  They are placeholder files
# for future tests and will trivially fail, so don't test them.
_PLACEHOLDER_STRINGS = ["QUA", "lattice"]

def checkIfPlaceholders(module_name):
    for s in _PLACEHOLDER_STRINGS:
        if s.lower() in module_name.lower():
            return True
    return False

def getAllTestModules():

    modules = []
    # for module in os.listdir(os.path.dirname(__file__)):
    for f in glob.glob("./*.py"):
        module_name = os.path.basename(f[:-3])

        if checkIfPlaceholders(module_name):
            print "Skipping placeholder test module", module_name
            continue

        if module_name[0] != "T": # tests start with T here..
            continue
        module = importlib.import_module(module_name)
        modules.append((module_name, module))
    return modules


def main():
    modules = getAllTestModules()
    for name, module in modules:
        try:
            result = module.Test()
        except Exception as e:
            print "-------TEST FAILED IN: ", name
            raise


if __name__ == '__main__':
    main()
