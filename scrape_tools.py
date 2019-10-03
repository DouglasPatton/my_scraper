import urllib.request
url="https://raw.githubusercontent.com/quanted/hms_app/master/models/meteorology/meteorology_parameters.py"
import re
import time
timestr = time.strftime("%Y%m%d-%H%M%S")

import os


class Documentation_check():
    def __init__(self,doc_type=None,model=None,submodel=None,url=None):
        if doc_type==None:doc_type='input_parameters'
        self.doc_type=doc_type
        if model==None:model='Meteorology'
        self.model=model
        if submodel==None:submodel='Precipitation'
        self.submodel=submodel
        self.url=url#not very flexible with urls

    #def doc_compare(    

    def pull_overview(self,model=None,submodel=None,baseurl=None,doc_type='input_parameters'):
        """creates self.pull_overview_dict 
        """
        if model==None:model='Meteorology' #default to meterology model
        if submodel==None:submodel='Precipitation'
        if baseurl==None: #default to dev branch, but user can provide own url, such as for master branch
            #may be assuming wrong structure since other models have overview in "views.py"
            baseurl="https://raw.githubusercontent.com/quanted/hms_app/dev/models/{}/{}_overview.py".format(model.lower(),submodel.lower())
        dir_path=os.path.dirname(os.path.realpath(__file__))
        base_filename=dir_path
        try:
            filename, headers = urllib.request.urlretrieve(baseurl, filename=dir_path+"\\data\\{}_overview_{}.py".format(submodel.lower(),timestr))
        except:print('url error. url:',baseurl)
        with open(filename,'rU') as pulled_pydoc:
            #use .strip() method to remove line-endings and whitespace
            all_lines=[line.strip() for line in pulled_pydoc]
        #remove all lines that have been commented out
        all_lines=[line for line in all_lines if not re.search('^\#',line)]#assuming \\
        #just one occurrence of line in all_lines, make flexible later
        #doc_pull_start=[i for i,line in enumerate(all_lines) if re.search('^'+doc_type+'\s\=\s\[',line)];print(doc_pull_start)
        doc_pull_start=[i for i,line in enumerate(all_lines) if re.search('^'+doc_type+'\s\=\s\[',line)][0]
        doc_pull_end,end_char_position_in_line=self.parenth_counter(all_lines[doc_pull_start+1:],'[')#changing \\
        #default open parenth to square bracket, make flexible later
        doc_pull_end+=1+doc_pull_start#add 1 because we did not give parentheses_counter \\
        #the rest of the line that the open parenth started on
        doc_pull_lines=all_lines[doc_pull_start+1:doc_pull_end-1]
        #print(doc_pull_start,doc_pull_end)
        #print(len(doc_pull_lines))
        doc_pull_lines_condensed=[]
        for i,line in enumerate(doc_pull_lines):
            if re.search('^\[',line):
                doc_pull_lines_condensed.append(line)
            else:
                if line[-2:]=="\s\"":
                    line=line[1:-2];print('here?')
                if line[-1]=="\"":
                    line=line[1:-1];print('here!')
                doc_pull_lines_condensed[-1]=doc_pull_lines_condensed[-1]+line
        #print(len(doc_pull_lines_condensed))
        '''feature_doc_pos,feature_doc_lines=myunzip([(i,line) for i,line in enumerate(doc_pull_lines)if re.search('^\[',line)])
        if len(doc_pull_lines)>len(feature_doc_lines):'''
        if doc_type=='input_parameters':
            pull_overview_dict={}
            for line in doc_pull_lines_condensed:
                param_dict={}
                print(line)
                line=line[1:-2]#drop extra characters at start and end

                start_quote_loc=[0]
                end_quote_loc=[]#add ending location at the end of loop
                #line=line[1:-1]#drop first and last since already accounted for in start and end quote loc vars
                for i,char in enumerate(line[:-1]):
                    if char=="\"":
                        if line[i+1]==",":#if next item is a comma
                            end_quote_loc.append(i)
                        if (i>2 and (line[i-2]=="," or line[i-1]==",")):
                            start_quote_loc.append(i)
                end_quote_loc.append(len(line))
                print('start',start_quote_loc)
                print('end',end_quote_loc)
                
                keylist=['name','type','description','child_elements']
                for i in range(len(end_quote_loc)-1):#-1 b/c first item is name
                    print(i)
                    print(keylist[i])
                    param_dict[keylist[i+1]]=line[start_quote_loc[i+1]+1:end_quote_loc[i+1]]
                pull_overview_dict[line[start_quote_loc[0]+1:end_quote_loc[0]]]=param_dict
        self.pull_overview_dict=pull_overview_dict
                    
            



    def pull_input_params(self,model=None,baseurl=None):
        """downloads model_parameters.py file
        downloads from master repo as default
        creates self.submodel_dict, a dictionary
        containing dictionaries of parameters
        for each submodel in the specified model
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
        #remove all lines that have been commented out
        all_lines=[line for line in all_lines if not re.search('^\#',line)]

        #put widgets that span multiple lines on single line
        widget_lines_start_pos,widget_lines=self.my_unzip([(ii,line) for ii,line in enumerate(all_lines) if re.search('widget\=.+\{$',line)])
        widget_lines_end_shift, char=self.my_unzip([self.parenth_counter(all_lines[i+1:],'{') for i in widget_lines_start_pos])
        
        #print(widget_lines_end_shift)
        widget_lines_condensed=[line+all_lines[widget_lines_start_pos[i]+1+ii] for i,line in enumerate(widget_lines) for ii in range(widget_lines_end_shift[i]+1)]
        #print('full widget line',widget_lines_condensed)
        for i,pos in enumerate(widget_lines_start_pos):
            all_lines[pos]=widget_lines_condensed[i]
            for ii in range(widget_lines_end_shift[i]):
                #print('line to be deleted:',all_lines[i+ii+1])
                all_lines[i+ii+1]=""
        #print([all_lines[widget_lines_start_pos[i]] for i in range(len(widget_lines_start_pos))])
        
               
        #extract submodel name and position in all_lines
        submodel_class_pos=[]
        submodel_class_pos,submodel_class_line=self.my_unzip([(i,line) for i,line in enumerate(all_lines) if re.search('^class',line)])
        assert not submodel_class_pos==[],'there are no classes defined in this file'
        submodel_name_end=[re.search('FormInput',line).start() for line in submodel_class_line]
        submodel_name_list=[line[6:end] for line,end in zip(submodel_class_line,submodel_name_end)]
        #print('submodel_class_pos',submodel_class_pos)
              
        submodel_dict={}#this will be a collection of dictionaries for each submodel
        
        for i,submodel_name in enumerate(submodel_name_list):
            if i<len(submodel_name_list)-1:
                submodel_lines=all_lines[submodel_class_pos[i]+1:submodel_class_pos[i+1]] #this one is from i to i+1(next clump of lines)
            else:
                submodel_lines=all_lines[submodel_class_pos[i]+1:] #this one goes to the end

            
            #for the range of lines for each submodel, find the parameters
            param_line_pos, param_lines=self.my_unzip([(i,line) for i,line in enumerate(submodel_lines) if re.search('\s\=\sforms\.',line)])
            param_name_end=[re.search('\s\=\sforms\.',line).start() for line in param_lines]


            features_start=[i+1 for i in param_line_pos]
            features_end=[]#initialize and then find the end of each feature based on line containing closing parenth
            for j in features_start:
                line_count_after_open,pos_in_line=self.parenth_counter(submodel_lines[j+1:]) #returns the line
                #(and position in the line which I'm not using) of the closing partenth, assuming it doesn't
                #close on the same line. modify this line to make flexible,
                #parenth_counter already flexible
                line_count_after_open+=1#add 1 since line with opening parenth not given to parenth_counter
                features_end.append(j+line_count_after_open)
         
            
            #some submodels may not have parameters, so start if statement for submodels with non-empty lists of parameters.
            if param_name_end==[]:param_dict='no_parameters'
            else: 
                param_name_list=[line[:end] for line,end in zip(param_lines,param_name_end)]
                #print(submodel_name,'param_name_list:',param_name_list)
                param_dict={}#initialize and then build param_dict
                for ii,param_name in enumerate(param_name_list):
                    #define range for featuers of each parameter
                    paramfeaturelines=submodel_lines[features_start[ii]:features_end[ii]]#list of lines for each paramter's potential features
                    feature_line_pos,feature_lines=self.my_unzip([(ii,line) for ii,line in enumerate(paramfeaturelines) if re.search('\=',line)])
                    feature_name_end=[re.search('\=',line).start() for line in feature_lines]
                    feature_name, feature_value=self.my_unzip([(line[:end],line[end:]) for line,end in zip(feature_lines,feature_name_end)])
                    param_feature_dict={}
                    for key,value in zip(feature_name,feature_value):
                        param_feature_dict[key]=value
                    param_dict[param_name]=param_feature_dict
                    #end for ii
            
            submodel_dict[submodel_name]=param_dict
        #print(submodel_dict)

        #print(submodel_dict)
        self.submodel_dict=submodel_dict




    def my_unzip(self,list_of_tups):
        #returns a tupple of 2 empty lists rather than just an empty list if I used zip(*...) on ([])
        unzipped=zip(*list_of_tups)
        if len([i for i in unzipped])==0:#easier way to unpack and check if zip object is empty?
            return [],[]
        else:return zip(*list_of_tups)

    def parenth_counter(self,text_after_open_p,open_type=None):
        '''takes a list of strings and returns a tuple with the
        line and character position in text_after of the closing parenth
        '''
        #print('open_type:',open_type)
        if open_type==None:open_type='('
        if open_type=='(':close_type=')'
        if open_type=='[':close_type=']'
        if open_type=='{':close_type='}'
        open_count_from_zero=1
        line_count=0
        while open_count_from_zero>0:
            line=text_after_open_p[line_count]
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
    test=Documentation_check()
    the_model='Meteorology';the_submodel='Precipitation';the_doc_type='input_parameters'
    test.pull_overview(model=the_model,submodel=the_submodel,doc_type=the_doc_type)
    test.pull_input_params(model=the_model)
    print('=============================')
    print('=============================')
    print('submodel_dict:',test.submodel_dict)
    print('##########################')
    print('pull_overview_dict:',test.pull_overview_dict)





