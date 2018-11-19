import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.offline as py
import plotly.graph_objs as go
def verdict_graph(handle):
    csv_file=pd.read_csv(handle+".csv")
    # print (csv_file.head())
    ver_count=csv_file['verdict'].value_counts()

    labels = ver_count.keys()
    values = ver_count.values
    trace = go.Pie(labels=labels, values=values)
    py.plot([trace], image='png', image_filename="verdict of "+handle, auto_open=False, filename=("verdict of "+handle+'-tag.html'))
    return 0

def language_graph(handle):
    csv_file=pd.read_csv(handle+".csv")
    # print (csv_file.head())
    ver_count=csv_file['language'].value_counts()
#     print (ver_count)
#     print (ver_count.keys())
#     print (ver_count.values)
    labels = ver_count.keys()
    values = ver_count.values
    trace = go.Pie(labels=labels, values=values)
    py.plot([trace], image='png', image_filename="language of "+handle, auto_open=False, filename=("language of "+handle+'-tag.html'))
    return 0
def levels(handle):
    csv_file=pd.read_csv(handle+".csv")
    ver_count=csv_file['problem_index'].value_counts()
    labels = ver_count.keys()
    values = ver_count.values
    trace = go.Bar(x=labels, y=values)
    py.plot([trace], image='png', image_filename="problem_index "+handle, auto_open=False, filename=("problem_index "+handle+'-tag.html'))
    return 0

verdict_graph('kashyap_archit')
language_graph('kashyap_archit')
levels('kashyap_archit')
