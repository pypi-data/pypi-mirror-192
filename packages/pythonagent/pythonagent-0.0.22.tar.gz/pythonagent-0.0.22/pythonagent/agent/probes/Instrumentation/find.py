import os
import ast
import json
import ctypes
import sys
import time
import pyclbr
import psutil
import datetime
import hashlib


def newmodulefinder():
    import sys
    from modulefinder import ModuleFinder

    finder = ModuleFinder()
    finder.run_script(sys.argv[0])
    a = finder.modules.items()
    modulelist = []
    # print('Loaded modules:')
    for name, mod in finder.modules.items():
        if mod.__file__ is None:
            pass
        else:
            modulelist.append(mod.__file__)
    return modulelist


def find():
    complete_output_str = ""
    p = psutil.Process(os.getpid())
    procname = p.name()
    nd_home = os.environ.get("ND_HOME")
    pathforfile = nd_home + "/python/logs/"
    filename = str(procname + "_AD.txt")
    file_to_open = os.path.join(pathforfile, filename)
    f = open(file_to_open, "w")
    f.writelines(
        "************************************  AUTO-DISCOVERY  **************************************** \n"
    )
    nylist = newmodulefinder()
    num_of_modules = len(nylist)
    num_of_methods = 0

    for path in nylist:
        
        module_path = os.path.split(os.path.abspath(path))[0]
        modulefullname = os.path.split(os.path.abspath(path))[1]
        module_name = modulefullname.split(".")[0]

        try:
            modleres = pyclbr.readmodule(module_name, path=[module_path])
        except Exception as e:
            print("module_path", module_path)
            print("module_name", module_name)
            print(e)

        # f.writelines("************************************  AUTO-DISCOVERY  **************************************** \n")
        if len(modleres) > 0:
            import sys

            sys.path
            for i in modleres.items():
                aa = modleres[str(i[0])].methods.keys()
                if aa:
                    num_of_methods += len(aa)
                    #print("if len(aa) >= 0: xxx{}yyy".format(aa))
                    joined_string = ",".join(aa)
                    outputfromad = module_name + "|" + i[0] + "|" + joined_string
                    complete_output_str += f"{outputfromad}  \n"
                    f.writelines(f"{outputfromad}  \n")
                else:
                    pass
        else:
            pass

        modleres_ex = pyclbr.readmodule_ex(module_name, path=[module_path])
        li = []
        for k, v in modleres_ex.items():
            if str(v) != None and "pyclbr.Function" in str(v):
                li.append(k)
            else:
                pass

        if li:
            num_of_methods += len(li)
            #print("if len(li) >= 0: xxx{}yyy".format(li))
            joined_stringf = ",".join(li)
            outputfromadf = module_name + "||" + joined_stringf
            complete_output_str += f"{outputfromadf}  \n"
            f.writelines(f"{outputfromadf} \n")

    return complete_output_str, num_of_modules, num_of_methods



if __name__ == "__main__":
    find()
