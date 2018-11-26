import user.load_data as ld
import numpy as np
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go

def verdict_graph(handle='kashyap_archit'):
    data = ld.load_data(handle)
    if data is None:
        return None

    ver_count = data['verdict'].value_counts()

    labels = ver_count.keys()
    values = ver_count.values
    trace = go.Pie(labels=labels, values=values)
    layout = go.Layout(title="Count vs verdict", paper_bgcolor='rgb(243, 243, 243)',plot_bgcolor='rgb(243, 243, 243)')
    fig = go.Figure(data=[trace], layout=layout)
    py.plot(fig, auto_open=False, filename=('data/'+handle+'-verdict.html'))
    return 0