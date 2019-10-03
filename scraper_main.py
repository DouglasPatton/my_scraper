#import scrape_tools as st
import scrape_tools as st

#input_parameters=st.pull_input_params('meteorology')

print('------------------------')
test=Documentation_check()
the_model='Meteorology';the_submodel='Precipitation';the_doc_type='input_parameters'
test.pull_overview(model=the_model,submodel=the_submodel,doc_type=the_doc_type)
test.pull_input_params(model=the_model)
test.do_doc_compare(model=the_model,submodel=the_submodel)
print(test.compare_submodel_input_param_doc_dict)
   
