import time as time_lib
from datetime import datetime

def unix_time():
    return int(round(time_lib.time()))


print(unix_time())
print(datetime.now().hour)