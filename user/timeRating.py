import user.user_data as ud
import numpy as np
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
from datetime import datetime

def time_graph(handle):
    '''
    Results out a time graph based on qRating and participant_type w.r.t time
    '''
    data = ud.data_process(handle)
    if data is None:
        return None

    data['time'] = data['time'].apply(lambda x: datetime.utcfromtimestamp(x).strftime('%Y-%m-%d'))
    data['time'] = data['time'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').date())
    data = data[data.verdict=='OK']
    data.drop(columns='verdict', inplace=True)
    data['qRating'] = [0]*len(data)

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
    contest = data[data.participant_type=='CONTESTANT']
    practice = data[data.participant_type=='PRACTICE']
    virtual = data[data.participant_type=='VIRTUAL']
    ouc = data[data.participant_type=='OUT_OF_COMPETITION']
    
    t0 = go.Scatter(x=contest['time'], y=contest['qRating'], mode='lines+markers', name='CONTESTANT')
    t1 = go.Scatter(x=practice['time'], y=practice['qRating'], mode='markers', name='PRACTICE',opacity=0.5)
    t2 = go.Scatter(x=virtual['time'], y=virtual['qRating'], mode='markers', name='VIRTUAL',opacity=0.7)
    t3 = go.Scatter(x=ouc['time'], y=ouc['qRating'], mode='markers', name='OUT_OF_COMPETITION',opacity=0.5)
    fig = {'data':[t0,t1,t2,t3], 'layout':{'title':"Problem Rating vs time(grouped by participant type)"}}
    py.plot(fig, auto_open=False, filename=('data/'+handle+'-timeQRating.html'))
    return 0

# time_graph(handle='kashyap_archit')