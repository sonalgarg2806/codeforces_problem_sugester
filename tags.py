import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ERROR_LOADING_DATA = 1

def load_data(handle):
    '''
    Loads user data from csv file given the handle name 
    '''
    try:
        df = pd.read_csv(handle+'.csv')
    except:
        return ERROR_LOADING_DATA
    return df

def tags_chart(handle='kashyap_archit'):
    '''
    Results out pie chart containing tags based submissions
    '''
    data = load_data(handle)
    if type(data) is int:
        print ("Error while loading csv file")
        return 0

    data = data[data.verdict=='OK']
    data.drop_duplicates(subset=['contest_id','problem_index'], inplace=True)
    data = data.tags
    tag = {}

    for item in data:
        item = item.replace("'","")
        item = item.replace("]","")
        item = item.replace("[","")
        item = item.split(", ")
        for x in item:
            tag[x] = tag.get(x, 0) + 1
    
    print (tag)
    return 0
