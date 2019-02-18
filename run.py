

import os, sys
import linecache
import argparse


# dirpath = os.getcwd()
# print("current directory is : " + dirpath)
# foldername = os.path.basename(dirpath)
# print("Directory name is : " + foldername)
# scriptpath = os.path.realpath(__file__)
# print("Script path is : " + scriptpath)
# # os.chdir(os.path.dirname(__file__))
# # os_getcwd = os.getcwd()
# # print(os_getcwd)
#
# # for path_str in sys.path:
# #     print(path_str, " ,")
# Pi_switch_folder = dirpath + '/Pi_switch'
# print("dir:" + Pi_switch_folder)
# sys.path.append(dirpath + '/Pi_switch')
#
# print("Pyhton ver:" + sys.version)

try:
    from Pi_switch.Pi_switch_main import run
    # print(Pi_switch)
    # print("Pi_switch:", Pi_switch_main)
except ModuleNotFoundError:
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)

    print("\n\nfucn '{}' error: \n{}, {} \nline:{}- {}"
          .format('MAIN', exc_type, exc_obj, lineno, line))
    exit(0)
    pass

# email[send, no of emails each day, hr to send]
# taps : 1 or 2 (1 is the main water, 2 is the rain/ac collect)

parser = argparse.ArgumentParser()
parser.add_argument("--float_debug", help="FOR DEBUG: choose float on or off (default is on)",
                    type=str)
args = parser.parse_args()
if args.float_debug is None:
    args.float_debug = "float_on"

run(debug=[False, args.float_debug], email=[True, 1, 20], taps=1)
