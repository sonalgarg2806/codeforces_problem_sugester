import user.load_data as ld
import numpy as np
import pandas as pd
import plotly
import plotly.offline as py
import plotly.graph_objs as go  

def tags_chart(handle='kashyap_archit'):
    '''
    Results out pie chart containing tags based submissions
    '''
    data = ld.load_data(handle)
    if data is None:
        print ("Error while loading csv file")
        return None

    data = data[data.verdict=='OK']
    data.drop_duplicates(subset=['contest_id','problem_index'], inplace=True)
    data = data.tags
    tag = {}

    for item in data:
        item = item.replace("'","")
        item = item.replace("]","")
        item = item.replace("[","")
        item = item.split(", ")
        for x in item:
            tag[x] = tag.get(x, 0) + 1
    
    labels = [x for x in tag.keys()]
    values = [tag[x] for x in tag.keys()]
    trace = go.Pie(labels=labels, values=values)
    py.plot([trace], image='png', image_filename='tag_count_chart', auto_open=False, filename=(handle+'-tag.html'))
    return 0
