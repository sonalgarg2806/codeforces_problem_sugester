import numpy as np
import pandas as pd

def load_data(handle):
    '''
    Loads user data from csv file given the handle name 
    '''
    try:
        df = pd.read_csv(handle+'.csv')
    except:
        print("    Error while loading data")
        return None
    return df
