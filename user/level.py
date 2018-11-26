import user.load_data as ld
import numpy as np
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go

def levels(handle):
    data = ld.load_data(handle)
    if data is None:
        return None

    ver_count = data['problem_index'].value_counts()
    labels = ver_count.keys()
    values = ver_count.values
    trace = go.Bar(x=labels, y=values)
    layout = go.Layout(title="Count vs problem index", yaxis=dict(autorange=True, showgrid=True, gridcolor='rgb(255, 255, 255)', gridwidth=1), paper_bgcolor='rgb(243, 243, 243)',plot_bgcolor='rgb(243, 243, 243)')
    fig = go.Figure(data=[trace], layout=layout)
    py.plot(fig, auto_open=False, filename=('data/'+handle+'-problem_level.html'))
    return 0