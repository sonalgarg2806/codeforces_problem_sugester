import numpy as np
import pandas as pd

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
