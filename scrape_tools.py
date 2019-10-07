import urllib.request
import re
from time import strftime
timestr = strftime("%Y%m%d-%H%M%S")
url="https://raw.githubusercontent.com/quanted/hms_app/dev/models/"
import os


class Documentation_Check():
    """gathers parameters, gathers existing documentation, compares
    methods
        pull_overview
            creates pull_overview_dict
        pull_input_params
            creates submodel_dict
        do_doc_compare
    """
    def __init__(self,doc_type=None,model=None,submodel=None,branch=None):
        if doc_type==None:doc_type='input_parameters'
        self.doc_type=doc_type
        if model==None:model='Meteorology'
        self.model=model
        if submodel==None:submodel='Precipitation'
        self.submodel=submodel
        if branch==None:branch='dev'
        self.url="https://raw.githubusercontent.com/quanted/hms_app/{}/models/".format(branch)
        if not os.path.exists('data'):
            os.mkdir('data')
            
    def doc_compare_to_table(self,submodel_comparison_dict=None):
        import pandas as pd;pd.set_option('display.max_colwidth', -1)
        if submodel_comparison_dict==None:
            try:
                self.compare_submodel_input_param_doc_dict
            except:
                print('self.compare_submodel_input_param_doc_dict does not exist, running with defaults')
                self.do_doc_compare()
            submodel_comparison_dict=self.compare_submodel_input_param_doc_dict
        #extract title(key):value from inputs that have that widget
        #then extract type and description from docs
        simplified_submodel_dict={}

        multi_line_blank="__________________________________ "\
            "__________________________________ "\
            "__________________________________ "\
            "__________________________________ "
            
        
        for param,param_dict in submodel_comparison_dict.items():
            simplified_param_dict={}
            try:
                simplified_param_dict['widget_title']=param_dict['from_input']['widget_title']
            except:
                simplified_param_dict['widget_title']='N/A'
            try:
                simplified_param_dict['type']=param_dict['from_doc']['type']
            except:
                simplified_param_dict['type']="________________"
            try:
                simplified_param_dict['description']=param_dict['from_doc']['description']
            except:
                simplified_param_dict['description']=multi_line_blank
            simplified_submodel_dict[param]=simplified_param_dict
        self.compare_doc_simple_dict=simplified_submodel_dict
        #print(simplified_submodel_dict)
        self.compare_doc_simple_table=pd.DataFrame(simplified_submodel_dict).T
        
        self.compare_doc_simple_table.to_html('output/doc_check1.html')

        self.orphan_table=pd.DataFrame(self.orphan_dict, index=['status']).T
        
        with open("output/doc_check1.html",'w') as _file:
            _file.write(self.compare_doc_simple_table.to_html() + "<br><br>" + self.orphan_table.to_html())
         
    
    def do_doc_compare(self, model=None,submodel=None):
        '''
        attributes created:
        self.orphaned_documentation are parameters that show up in the
            documentation that don't match any inputs
        self.compare_orphaned_input_parameters are input parameters with no
            corresponding documentation
        self.compare_submodel_input_param_doc_dict for each input parameter,
            has all features and values including for any matching (identical) parameter from the documentation( _overrview.py file)
        '''
        if model==None:
            model="Meteorology"
        self.compare_model=model
        if submodel==None:
            submodel=='Precipitation'
        self.compare_submodel=submodel
        try:
            self.pull_overview_dict
        except:
            print('no pull_overview_dict. running default param values')
            self.pull_overview(model=model,submodel=submodel)
        try:
            self.submodel_dict
        except:
            print('no submodel_dict. running default param values')
            self.pull_input_params(model=model)
                
        #for each input_parameter, merge info from the two sources
        
        submodel_input_param_doc_dict={}
        orphaned_input_parameters=[]
        docs_with_inputs=[]#otherwise they would be orphans
        for input_parameter,input_feature_dict in self.submodel_dict[submodel].items():#key,value pair
            
            input_param_has_doc=0
            param_dict={}
            
            param_dict['from_input']=input_feature_dict
                #param_dict['input_{}'.format(feature_name)]=feature_value
            for doc_parameter,doc_feature_dict in self.pull_overview_dict.items():
                if input_parameter.lower()==doc_parameter.lower():
                    param_dict['from_doc']=doc_feature_dict
                    docs_with_inputs.append(doc_parameter)#doc_parameter matches \\
                    #input_parameter, so they interchangeable here
                    submodel_input_param_doc_dict[doc_parameter]=param_dict
                    input_param_has_doc=1
                    break#stop loop since outer loop has found its documentation,\\
                    #move to next input_parameter
            if input_param_has_doc==0:
                print(input_parameter,'doesn\'t have doc')
                param_dict['from_doc']='documentation not found'
                submodel_input_param_doc_dict[input_parameter]=param_dict
                orphaned_input_parameters.append(input_parameter)#the dictionary will also be missing \\
                #key:value for the doc side but not the input side
        print('docs_with_inputs:',docs_with_inputs)
        orphaned_documentation=[
            doc_parameter 
            for doc_parameter,doc_feature_dict 
            in self.pull_overview_dict.items() 
            if not doc_parameter.lower() in [item.lower() for item in docs_with_inputs]
            ]
        #self.compare_orphaned_input_parameters=orphaned_input_parameters
        self.compare_submodel_input_param_doc_dict=submodel_input_param_doc_dict
        orphan_dict={}
        for key in orphaned_input_parameters:
            orphan_dict[key]='no documentation found'
        for key in orphaned_documentation:
            orphan_dict[key]='no input_parameter found'
        self.orphan_dict=orphan_dict
        
        
                    
                    
                    
                
        

    def pull_overview(self,model=None,submodel=None,baseurl=None,doc_type='input_parameters'):
        """creates self.pull_overview_dict 
        """
        if model==None:model='Meteorology' #default to meterology model
        if submodel==None:submodel='Precipitation'
        if baseurl==None: #default to dev branch, but user can provide own url, such as for master branch
            #may be assuming wrong structure since other models have overview in "views.py"
            baseurl=self.url+"{}/{}_overview.py".format(model.lower(),submodel.lower())
        dir_path=os.path.dirname(os.path.realpath(__file__))
        base_filename=dir_path
        try:
            filename, headers = urllib.request.urlretrieve(
                baseurl,
                filename=dir_path+"\\data\\{}_overview_{}.py".format(submodel.lower(),timestr)
                )
        except:
            print('url error. url:',baseurl)
        with open(filename,'rU') as pulled_pydoc:
            #use .strip() method to remove line-endings and whitespace
            all_lines=[line.strip() for line in pulled_pydoc]
        #remove all lines that have been commented out
        all_lines=[line for line in all_lines if not re.search('^\#',line)]#assuming \\
        #just one occurrence of line in all_lines, make flexible later
        doc_pull_start=[i for i,line in enumerate(all_lines) if re.search('^'+doc_type+'\s\=\s\[',line)][0]
        doc_pull_end,end_char_position_in_line=self.parenth_counter(all_lines[doc_pull_start+1:],'[')
        doc_pull_end+=1+doc_pull_start#add 1 because we did not give parentheses_counter \\
        #the rest of the line that the open parenth started on
        doc_pull_lines=all_lines[doc_pull_start+1:doc_pull_end-1]


        #trying to condense string that spill over to next line into single line.
        #doesn' seem to work
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
        
        if doc_type=='input_parameters':
            pull_overview_dict={}
            for line in doc_pull_lines_condensed:
                param_dict={}
                #print(line)
                line=line[1:-2]#drop extra characters at start and end

                start_quote_loc=[0]
                end_quote_loc=[]#add ending location at the end of loop
                for i,char in enumerate(line[:-1]):
                    if char=="\"":
                        if line[i+1]==",":#if next item is a comma
                            end_quote_loc.append(i)
                        if (i>2 and (line[i-2]=="," or line[i-1]==",")):
                            start_quote_loc.append(i)
                end_quote_loc.append(len(line))#as mentioned above
                
                keylist=['name','type','description','child_elements']
                for i in range(len(end_quote_loc)-1):#-1 b/c first item is name
                    param_dict[keylist[i+1]]=line[start_quote_loc[i+1]+1:end_quote_loc[i+1]]
                pull_overview_dict[line[start_quote_loc[0]+1:end_quote_loc[0]]]=param_dict
        self.pull_overview_dict=pull_overview_dict
                    
            

    def condense_widgets(self,all_lines):
        
        widget_lines_start_pos,widget_lines=self.my_unzip([
            (ii,line) for ii,line
            in enumerate(all_lines)
            if re.search('widget\=.+\{$',line)
            ])
        widget_lines_end_shift, char=self.my_unzip([
            self.parenth_counter(all_lines[i+1:],'{')
            for i in widget_lines_start_pos
            ])
        
        widget_lines_condensed=[]
        for i,line in enumerate(widget_lines):
            for ii in range(widget_lines_end_shift[i]):
                line=line+all_lines[widget_lines_start_pos[i]+1+ii]
            widget_lines_condensed.append(line)        
        
        for i,pos in enumerate(widget_lines_start_pos):
            all_lines[pos]=widget_lines_condensed[i]
            for ii in range(widget_lines_end_shift[i]):
                all_lines[pos+ii+1]=""
            if re.search('\'title\'\:',widget_lines_condensed[i]):
                all_lines[pos+1]='widget_title='+all_lines[pos][
                    re.search('\'title\'\:',widget_lines_condensed[i]).start()+10:-3
                    ]
        return all_lines
    
    def pull_input_params(self,model=None,baseurl=None):
        """downloads model_parameters.py file
        downloads from master repo as default
        creates self.submodel_dict, a dictionary
        containing dictionaries of parameters
        for each submodel in the specified model
        """
        if model==None:model='Meteorology' #default to meterology model
        if baseurl==None: #default to dev branch, but user can provide own url, such as for master branch
            baseurl=self.url+"/{}/{}_parameters.py".format(model.lower(),model.lower())
        dir_path=os.path.dirname(os.path.realpath(__file__))
        base_filename=dir_path

        filename, headers = urllib.request.urlretrieve(baseurl, filename=dir_path+"\\data\\{}_input_param_{}.py".format(model.lower(),timestr))

        with open(filename,'rU') as input_params:
            #use .strip() method to remove line-endings and whitespace
            all_lines=[line.strip() for line in input_params]
        #remove all lines that have been commented out
        all_lines=[line for line in all_lines if not re.search('^\#',line)]

        #put widgets that span multiple lines on single line
        all_lines=self.condense_widgets(all_lines)
                     
        #extract submodel name and position in all_lines
        submodel_class_pos=[]
        submodel_class_pos,submodel_class_line=self.my_unzip([
            (i,line) for i,line
            in enumerate(all_lines)
            if re.search('^class',line)
            ])
        assert not submodel_class_pos==[],'there are no classes defined in this file'
        submodel_name_end=[re.search('FormInput',line).start() for line in submodel_class_line]
        submodel_name_list=[line[6:end] for line,end in zip(submodel_class_line,submodel_name_end)]

        #check which submodels inherit prameters from hydrology submodel
        self.input_ischildofhydrology=[submodel_name_list[i] for i,line in enumerate(submodel_class_line) if re.search('^class.+\(HydrologyFormInput\)\:$',line)]

                      
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
                #close on the same line. 
                line_count_after_open+=1#add 1 since line with opening parenth not given to parenth_counter
                features_end.append(j+line_count_after_open)
         
            
            #some submodels may not have parameters, so start if statement for submodels with non-empty lists of parameters.
            if param_name_end==[]:
                param_dict='no_parameters'
            else: 
                param_name_list=[line[:end] for line,end in zip(param_lines,param_name_end)]
                
                param_dict={}#initialize and then build param_dict
                for ii,param_name in enumerate(param_name_list):
                    #define range for featuers of each parameter
                    paramfeaturelines=submodel_lines[features_start[ii]:features_end[ii]]#list of lines for each paramter's potential features
                    feature_line_pos,feature_lines=self.my_unzip([
                        (ii,line) for ii,line
                        in enumerate(paramfeaturelines)
                        if re.search('\=',line)
                        ])
                    feature_name_end=[re.search('\=',line).start() for line in feature_lines]
                    feature_name, feature_value=self.my_unzip([
                        (line[:end],line[end+1:]) for line,end
                        in zip(feature_lines,feature_name_end)
                        ])
                    param_feature_dict={}
                    for key,value in zip(feature_name,feature_value):
                        param_feature_dict[key]=value
                    param_dict[param_name]=param_feature_dict
                    
            submodel_dict[submodel_name]=param_dict

        #add parameters and feature_dict from hydrology inputs to child inputs
            #not flexible to other inheritance patterns
        for submodel_name,param_dict in submodel_dict.items():
            if submodel_name in self.input_ischildofhydrology:
                for param,param_feature_dict in submodel_dict['Hydrology'].items():
                    submodel_dict[submodel_name][param]=param_feature_dict
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
    test=Documentation_Check()
    the_model='Meteorology';the_submodel='Precipitation';the_doc_type='input_parameters'
    test.pull_overview(model=the_model,submodel=the_submodel,doc_type=the_doc_type)
    test.pull_input_params(model=the_model)
    test.do_doc_compare(model=the_model,submodel=the_submodel)
    test.doc_compare_to_table()
    

