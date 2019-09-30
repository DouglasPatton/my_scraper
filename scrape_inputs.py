import urllib.request
url="https://raw.githubusercontent.com/quanted/hms_app/master/models/meteorology/meteorology_parameters.py"

import time
timestr = time.strftime("%Y%m%d-%H%M%S")

import os
dir_path=os.path.dirname(os.path.realpath(__file__))
base_filename=dir_path
filename, headers = urllib.request.urlretrieve(url, filename=dir_path+"\\data\\input_param_{}.py".format(timestr))
input_params=open(filename).read()
print(input_params[0:100])

