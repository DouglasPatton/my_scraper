import urllib.request
url="https://raw.githubusercontent.com/quanted/hms_app/master/models/meteorology/meteorology_parameters.py"
import re
import time
timestr = time.strftime("%Y%m%d-%H%M%S")

import os


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
        
               
        #extract submodel name and position in all_lines
        submodel_class_pos=[]
        submodel_class_pos,submodel_class_line=my_unzip([(i,line) for i,line in enumerate(all_lines) if re.search('^class',line)and not re.search('^\#',line)])
        assert not submodel_class_pos==[],'there are no classes defined in this file'
        
        submodel_name_end=[re.search('FormInput',line).start() for line in submodel_class_line]
        submodel_name_list=[line[6:end] for line,end in zip(submodel_class_line,submodel_name_end)]
        #print('submodel_class_pos',submodel_class_pos)
              
        submodel_dict={}
        
        for i,submodel_name in enumerate(submodel_name_list):
            if i<len(submodel_name_list)-1:
                submodel_lines=all_lines[submodel_class_pos[i]+1:submodel_class_pos[i+1]] #this one is from i to i+1(next clump of lines)
            else:
                submodel_lines=all_lines[submodel_class_pos[i]+1:] #this one goes to the end
            #print('submodel_line len',len(submodel_lines))
            #for the range of lines for each submodel, find the parameters
            param_line_pos, param_lines=my_unzip([(i,line) for i,line in enumerate(submodel_lines) if re.search('\s\=\sforms\.',line) and not re.search('^\#',line)])
            param_name_end=[re.search('\s\=\sforms\.',line).start() for line in param_lines]
            features_start=[i+1 for i in param_line_pos]
            features_end=[]
            for j in features_start:
                ij=0
                while True:
                    print(ij)
                    if re.search('^\)$',submodel_lines[j+ij]):
                        #end_found==True
                        features_end.append(j+ij)
                        break
                    else:ij+=1
                #features_end.append=[i for i,line in enumerate(feature_end_search_lines) if re.search('^\)$',line)]

            
            #some submodels may not have parameters, so start if statement for submodels with non-empty lists of parameters.
            if param_name_end==[]:param_dict='no_parameters'
            else: 
                param_name_list=[line[:end] for line,end in zip(param_lines,param_name_end)]
                print(submodel_name,'param_name_list:',param_name_list)
                param_dict={}#initialize and then build param_dict
                for ii,param_name in enumerate(param_name_list):
                    #define range for featuers of each parameter
                    paramfeaturelines=submodel_lines[features_start[ii]:features_end[ii]]#list of lines for each paramter's potential features
                    feature_line_pos,feature_lines=my_unzip([(ii,line) for ii,line in enumerate(paramfeaturelines) if re.search('\=',line) and not re.search('^\#',line)])
                    feature_name_end=[re.search('\=',line).start() for line in feature_lines]
                    feature_name, feature_value=my_unzip([(line[:end],line[end:]) for line,end in zip(feature_lines,feature_name_end)])
                    param_feature_dict={}
                    for key,value in zip(feature_name,feature_value):
                        param_feature_dict[key]=value
                    param_dict[param_name]=param_feature_dict
                    #end for ii
            
            submodel_dict[submodel_name]=param_dict
        #print(submodel_dict)

    print(submodel_dict)





def my_unzip(list_of_tups):
    #returns a tupple of 2 empty lists rather than just an empty list if I used zip(*...) on ([])
    unzipped=zip(*list_of_tups)
    if len([i for i in unzipped])==0:#easier way to unpack and check if zip object is empty?
        return [],[]
    else:return zip(*list_of_tups)

        
if __name__=="__main__":
    pull_input_params()
    





