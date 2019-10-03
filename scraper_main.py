#import scrape_tools as st
import scrape_tools as st

#input_parameters=st.pull_input_params('meteorology')

print('------------------------')
test=st.Documentation_check()
test.pull_overview(model='Meteorology',submodel='Precipitation',doc_type='input_parameters')

test.pull_input_params(model='Meteorology')
