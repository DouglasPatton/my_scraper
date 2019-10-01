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
        #print(all_lines)
               
        #extract submodel name and position in all_lines
        submodel_class_pos,submodel_class_line=zip(*[(i,line) for i,line in enumerate(all_lines) if re.search('^class',line)])
        #print(submodel_class_pos,submodel_class_line    )
        submodel_name_end=[re.search('FormInput',line).start() for line in submodel_class_line]
        submodel_name_list=[line[6:end] for line,end in zip(submodel_class_line,submodel_name_end)]
        
        
        submodel_dict={}
        
        for i,submodel_name in enumerate(submodel_name_list):
            if i<len(submodel_name_list)-1:
                
                submodel_lines=all_lines[submodel_class_pos[i]:submodel_class_pos[i+1]]
                #print(name,submodel_lines)
            else:
                submodel_lines=all_lines[submodel_class_pos[i]:]
            print(submodel_lines)
            
            param_end_pos_tup_param_lines=[(i,line) for i,line in enumerate(submodel_lines) if re.search('\s\=\sforms\.',line)]
            if len(param_end_pos_tup_param_lines)>0:
                print("######",param_end_pos_tup_param_lines)
                parem_end_pos,param_lines=zip(*param_end_pos_tup_param_lines)
                print(zip(*param_end_pos_tup_param_lines))
                print('!!!!!!',param_end_pos)
            #param_end_pos,param_lines=zip(*[(i,line) for i,line in enumerate(submodel_lines) if re.search('\s\=\sforms\.',line) and not re.search('^\#',line)])
                param_name_list=[line[:end] for line,end in zip(param_lines,param_end_pos)]


                param_dict={}
                for ii,param_name in enumerate(param_name_list):
                    feature_end_pos,feature_lines=zip(*[(i,line) for ii,line in enumerate(param_lines) if re.search('\=',line) and not re.search('^\#',line)])
                    feature_name, feature_value=zip(*[(line[:end],line[end:]) for line,end in zip(feature_lines,feature_end_pos)])
                    param_feature_dict={}
                    for name,value in zip(feature_name,feature_value):
                        param_feature_dict[feature_name]=feature_value
                    param_dict[param_name]=param_feature_dict
                    #end for ii
            else: param_dict='no params'
            submodel_dict[submodel_name]=param_dict
        print(submodel_dict)

if __name__=="__main__":
    pull_input_params()
    





