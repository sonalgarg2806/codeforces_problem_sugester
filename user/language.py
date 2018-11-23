import user.load_data as ld
import numpy as np
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go

def language_graph(handle='kashyap_archit'):
    data = ld.load_data(handle)
    if type(data) is int:
        print ("Error while loading csv file")
        return 0

    ver_count = data['language'].value_counts()

    labels = ver_count.keys()
    values = ver_count.values
    trace = go.Pie(labels=labels, values=values)
    py.plot([trace], image='png', image_filename=handle+'-language', auto_open=False, filename=(handle+'-language.html'))
    return 0