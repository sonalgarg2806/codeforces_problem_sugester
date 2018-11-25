import user.load_data as ld
import numpy as np
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go

def language_graph(handle='kashyap_archit'):
    data = ld.load_data(handle)
    if data is None:
        print ("Error while loading csv file")
        return None

    ver_count = data['language'].value_counts()

    labels = ver_count.keys()
    values = ver_count.values
    trace = go.Pie(labels=labels, values=values)
    fig = {'data':[trace], 'layout':{'title':"Count vs language"}}
    py.plot(fig, auto_open=False, filename=(handle+'-language.html'))
    return 0