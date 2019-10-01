import urllib.request
url="https://raw.githubusercontent.com/quanted/hms_app/master/models/meteorology/meteorology_parameters.py"
import re
import time
timestr = time.strftime("%Y%m%d-%H%M%S")

import os

#save version:
def pull_input_params(model=None,baseurl=None):
    """downloads model_parameters.py file
    downloads from master repo as default
    """
    if model==None:model='meteorology' #default to meterology model
    if baseurl==None: #default to master branch, but user can provide own url, such as for dev branch
        baseurl="https://raw.githubusercontent.com/quanted/hms_app/master/models/{}/{}_parameters.py".format(model,model)
    dir_path=os.path.dirname(os.path.realpath(__file__))
    base_filename=dir_path
    filename, headers = urllib.request.urlretrieve(baseurl, filename=dir_path+"\\data\\input_param_{}.py".format(timestr))
    with open(filename,'rU') as input_params:
        #use .strip() method to remove line-endings and whitespace
        all_lines=[line.strip() for line in input_params]
        print(all_lines)
               
        #extract submodel name and position in all_lines
        submodel_class_pos,submodel_class_line=zip(*[(i,line) for i,line in enumerate(all_lines) if re.search('^class',line)])
        print(submodel_class_pos,submodel_class_line    )
        submodel_name_end=[re.search('FormInput',line).start() for line in submodel_class_line]
        
        submodel_name_list=[line[6:end] for line,end in zip(submodel_class_line,submodel_name_end)]
        
        
        submodel_dict={}
        for i,name in enumerate(submodel_name_list):
            if i<len(submodel_name_list)-1:
                
                submodel_lines=all_lines[submodel_class_pos[i]:submodel_class_pos[i+1]]
                #print(name,submodel_lines)
            else:
                submodel_lines=all_lines[submodel_class_pos[i]:]
            formsdot_lines=[line for line in submodel_lines if re.findall('.+\s\=\sforms\..+',line)]
            #remove any commented out lines
            formsdot_lines=[line for line in formsdot_lines if not re.findall('^\#',line)]
            #formsdot_lines=[line for line in all_lines if re.findall('.+forms\..+',line)]
            param_end_pos=[re.search('\s\=',line).start() for line in formsdot_lines]
            param_name=[line[:end] for line,end in zip(formsdot_lines,param_end_pos)]
            #print(param_name)
            submodel_dict[name]=param_name
        print(submodel_dict)

if __name__=="__main__":
    pull_input_params()
    





