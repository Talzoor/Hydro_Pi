
import os
import datetime as dt

# common time string - change this and it will change folder and files names
str_time = str(dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
# find user folder
userhome = os.path.expanduser('~')
desktop = userhome + '/Desktop/'
# full path for saving folder - change this to control folder name
dir_to_save = desktop + 'experimental_results/' + str_time

# uncomment next 2 lines to check Desktop and saving folder are correct
#   print("userhome:{}, desktop:{}".format(userhome, desktop))
#   print("dir_to_save:{}".format(dir_to_save))

# now to check if this folder already there
dir_exists = os.path.isdir(dir_to_save)
if not dir_exists:              # if not - create it
    os.makedirs(dir_to_save)

# finally adding dir_to_save to all three files
VIDEO_FILE_NAME = dir_to_save + "cam" + camId + "_output_" + str_time + ".h264"
TIMESTAMP_FILE_NAME = dir_to_save + "cam" + camId + "_timestamp_" + str_time + ".csv"
TTL_FILE_NAME = dir_to_save + "cam"+ camId + "_ttl_" + str_time + ".csv"
