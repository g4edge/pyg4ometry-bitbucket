import glob
import os
import sys
import importlib

def getAllTestModules():

    modules = []
    # for module in os.listdir(os.path.dirname(__file__)):
    for f in glob.glob("./*.py"):
        module_name = os.path.basename(f[:-3])

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
            print "------> Test {} FAILED with message {}".format(name, e)
            continue


if __name__ == '__main__':
    main()
