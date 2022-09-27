import glob
import os
import sys
sys.dont_write_bytecode = True
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

    total = 0
    passed = 0
    failed = 0

    for name, module in modules:
        total += 1
        try:
            result = module.Test()
            passed +=1
        except Exception as e:
            print("------> Test {} FAILED with message {}".format(name, e))
            failed +=1
            continue
    print("{} tested.  {} passed.  {} failed.".format(total, passed, failed))


if __name__ == '__main__':
    main()
