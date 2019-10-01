import urllib.request
url="https://raw.githubusercontent.com/quanted/hms_app/master/models/meteorology/meteorology_parameters.py"

import time
timestr = time.strftime("%Y%m%d-%H%M%S")

import os

#save version:
def pull_input_params(submodule,baseurl=None):
    """downloads submodule_parameters.py file
    """
    if baseurl==None:
        baseurl="https://raw.githubusercontent.com/quanted/hms_app/master/models/{}/{}_parameters.py".format(submodule,submodule)
    dir_path=os.path.dirname(os.path.realpath(__file__))
    base_filename=dir_path
    filename, headers = urllib.request.urlretrieve(url, filename=dir_path+"\\data\\input_param_{}.py".format(timestr))
    with open(filename,'rU') as input_params:
        #use .strip() method to remove line-endings and whitespace
        all_lines=[line.strip() for line in input_params]

        import re
        formsdot_lines=[line for line in all_lines if re.findall('.+\s\=\sforms\..+',line)]
        #remove any commented out lines
        formsdot_lines=[line for line in formsdot_lines if not re.findall('^\#',line)]
        #formsdot_lines=[line for line in all_lines if re.findall('.+forms\..+',line)]
        param_end_pos=[re.search('\s\=',line).start() for line in formsdot_lines]
        param_name=[line[:end] for line,end in zip(formsdot_lines,param_end_pos)]
        print(param_name)

#if__name__=="__main__"
    





