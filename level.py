import load_data as ld
import numpy as np
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go

def levels(handle):
    data = ld.load_data(handle)
    if type(data) is int:
        print ("Error while loading csv file")
        return 0

    ver_count = data['problem_index'].value_counts()
    labels = ver_count.keys()
    values = ver_count.values
    trace = go.Bar(x=labels, y=values)
    py.plot([trace], image='png', image_filename=handle+'problem_level', auto_open=False, filename=(handle+'-problem_level.html'))
    return 0