import user.user_data as ud
import numpy as np
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
from datetime import datetime
from collections import defaultdict

def box_plot(handle):
    '''
    Results out a box-plot of question rating grouped by tags.
    '''
    data = ud.data_process(handle)
    if data is None:
        return None

    data = data[data.verdict=='OK']
    data.drop(columns=['verdict','time','participant_type'], inplace=True)
    data['qRating'] = [0]*len(data)
    # load question rating
    pr = pd.read_csv("problem_rating.csv")    
    pr.drop(columns='Unnamed: 0', inplace=True)
    pr['idx'] = pr['contestID'].map(str)+pr['problemID']
    pr.set_index('idx', inplace=True)
    # finding out the question rating
    for i in range(len(data)):
        try:
            ndx = str(int(data.iloc[i]['contest_id']))+data.iloc[i]['problem_index']
        except:
            continue
        try:
            data.iloc[i, data.columns.get_loc('qRating')] = pr.loc[ndx]['problemRating']
        except:
            continue

    data = data[data.qRating!=0]
    tagQrating = defaultdict(list)

    for i in range(len(data)):
        x = data.iloc[i]['tags']
        x = x.replace("[","")
        x = x.replace("]","")
        x = x.replace("'","")
        if not x:
            continue
        tag = x.split(', ')
        for t in tag:
            tagQrating[t].append(data.iloc[i]['qRating'])

    trace = []
    for t in tagQrating.keys():
        a = go.Box(y=tagQrating[t], name=t, stream=dict(maxpoints=10000), boxpoints='all', boxmean='sd', jitter=0.5, pointpos=0, marker=dict(size=2), line=dict(width=1))
        trace.append(a)
    
    layout = go.Layout(title='question rating grouped by tags', yaxis=dict(autorange=True, showgrid=True, gridcolor='rgb(255, 255, 255)', gridwidth=1), paper_bgcolor='rgb(243, 243, 243)',plot_bgcolor='rgb(243, 243, 243)', showlegend=False)
    fig = go.Figure(data=trace, layout=layout)
    py.plot(fig, auto_open=False, filename=('data/'+handle+'-box_plot.html'))
    return 0