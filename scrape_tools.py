import urllib.request
url="https://raw.githubusercontent.com/quanted/hms_app/master/models/meteorology/meteorology_parameters.py"
import re
import time
timestr = time.strftime("%Y%m%d-%H%M%S")

import os


def pull_overview(model=None,submodel=None,baseurl=None):
    """
    """
    if model==None:model='Meteorology' #default to meterology model
    if submodel==None:submodel='Precipitation'
    if baseurl==None: #default to dev branch, but user can provide own url, such as for master branch
        #may be assuming wrong structure since other models have overview in "views.py"
        baseurl="https://raw.githubusercontent.com/quanted/hms_app/dev/models/{}/{}_overview.py".format(model.lower(),submodel.lower())
    dir_path=os.path.dirname(os.path.realpath(__file__))
    base_filename=dir_path
    filename, headers = urllib.request.urlretrieve(baseurl, filename=dir_path+"\\data\\{}_overview_{}.py".format(submodel.lower(),timestr))
    
    with open(filename,'rU') as input_params:
        #use .strip() method to remove line-endings and whitespace
        all_lines=[line.strip() for line in input_params]
        all_lines=[line for line in all_lines if not re.search('^\#',line)]#remove all lines that have been commented out
    



def pull_input_params(model=None,baseurl=None):
    """downloads model_parameters.py file
    downloads from master repo as default
    """
    if model==None:model='Meteorology' #default to meterology model
    if baseurl==None: #default to dev branch, but user can provide own url, such as for master branch
        baseurl="https://raw.githubusercontent.com/quanted/hms_app/dev/models/{}/{}_parameters.py".format(model.lower(),model.lower())
    dir_path=os.path.dirname(os.path.realpath(__file__))
    base_filename=dir_path
    filename, headers = urllib.request.urlretrieve(baseurl, filename=dir_path+"\\data\\{}_input_param_{}.py".format(model.lower(),timestr))

    with open(filename,'rU') as input_params:
        #use .strip() method to remove line-endings and whitespace
        all_lines=[line.strip() for line in input_params]
        all_lines=[line for line in all_lines if not re.search('^\#',line)]#remove all lines that have been commented out
               
        #extract submodel name and position in all_lines
        submodel_class_pos=[]
        submodel_class_pos,submodel_class_line=my_unzip([(i,line) for i,line in enumerate(all_lines) if re.search('^class',line)])
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
            param_line_pos, param_lines=my_unzip([(i,line) for i,line in enumerate(submodel_lines) if re.search('\s\=\sforms\.',line)])
            param_name_end=[re.search('\s\=\sforms\.',line).start() for line in param_lines]
            features_start=[i+1 for i in param_line_pos]
            features_end=[]

            for j in features_start:
                line,pos_in_line=parenth_counter(submodel_lines[j+1:])#returns the line (and position in the line)
                

            '''
            for j in features_start:
                ij=0
                while True:
                    if re.search('^\)$',submodel_lines[j+ij]):
                        #end_found==True
                        features_end.append(j+ij)
                        break
                    else:ij+=1
                #features_end.append=[i for i,line in enumerate(feature_end_search_lines) if re.search('^\)$',line)]
''' 
            
            #some submodels may not have parameters, so start if statement for submodels with non-empty lists of parameters.
            if param_name_end==[]:param_dict='no_parameters'
            else: 
                param_name_list=[line[:end] for line,end in zip(param_lines,param_name_end)]
                print(submodel_name,'param_name_list:',param_name_list)
                param_dict={}#initialize and then build param_dict
                for ii,param_name in enumerate(param_name_list):
                    #define range for featuers of each parameter
                    paramfeaturelines=submodel_lines[features_start[ii]:features_end[ii]]#list of lines for each paramter's potential features
                    feature_line_pos,feature_lines=my_unzip([(ii,line) for ii,line in enumerate(paramfeaturelines) if re.search('\=',line)])
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

def parenth_counter(text_after_open_p,open_type='(')
    '''takes a list of strings and 
    '''
    if open_type=='(':close_type=')'
    if open_type=='[':close_type=']'
    if open_type=='{':close_type='}'
    open_count_from_zero=1
    line_count=0
    while open_count_from_zero>0:
        line=text_after_open[line_count]
        char_count=0
        for i in line:
            if i==close_type:
                open_count_from_zero-=1  
            if i==open_type:
                open_count_from_zero+=1
            if open_count_from_zero==0:break;break#twice since nested loop
            char_count+=1
        line_count+=1    
     return line_count,char_count       



if __name__=="__main__":
    pull_input_params()
    





