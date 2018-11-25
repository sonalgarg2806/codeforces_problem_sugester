# Fetch user data and contest data from CF
import json
import urllib.request as url_req
import pandas as pd
import numpy as np
import user.load_data as ld
from datetime import datetime

MAX = 100000

base_url = 'http://codeforces.com/api/'
sep = '&'
tab = '    '
user_status_url = base_url + 'user.status?handle={handle}'+sep+'from={start}'+sep+'count={count}'
user_rating_url = base_url + 'user.rating?handle={handle}'


EXT = {'C++': 'cpp', 'C': 'c', 'Java': 'java', 'Python': 'py', 'Delphi': 'dpr', 'FPC': 'pas', 'C#': 'cs'}
EXT_keys = EXT.keys()

def get_EXT(lang):
    '''
    Returns the key of language in which it is written
    '''
    for key in EXT_keys:
        if key in lang:
            return EXT[key]
    return ''

def load_url(url):
    '''
    Given the url loads the json and returns the result
    '''
    try:
        json_obj = url_req.urlopen(url)
    except:
        print (tab + "Error while fetching data")
        return None

    data = json.load(json_obj)
    
    if data['status'] != 'OK':
        print (tab + "Error while fetching data: " + data['comment'])
        return None
    else:
        data = data['result']

    return data

def load_user_data(handle='kashyap_archit', start=1, count=MAX):
    '''
    Input : 
        handle name
        start (starting submission)
        count (number of submissions from start)\n
    Output : returns a dataframe containing
        1. solution_id
        2. contest_id
        3. submission_time (unix time at which submission was made)
        4. relative_time (unix time after contest at which submission was made)
        3. problem_index
        4. problem_name (if available)
        5. problem_type (Enum: PROGRAMMING, QUESTION)
        6. points (if the question is not rated then it is 0)
        7. tags
        8. team (individual or team)
        9. participant_type (CONTESTANT, PRACTICE, VIRTUAL, MANAGER, OUT_OF_COMPETITION)
        10.language
        11.verdict
        12.test_case (number of test cases passed)
        13.time (in milliseconds)
        14.memory (in kilo-bytes) 
    '''
    print("Loading user data for "+handle)
    url = user_status_url.format(handle=handle, start=start, count=count)
    data = load_url(url)
    if data is None:
        return None

    df = pd.DataFrame(columns=['solution_id','contest_id','submission_time','relative_time','problem_index','problem_name','problem_type','points','tags','team','participant_type','language','verdict','test_case','time','memory'])
    
    print(tab+"Creating DataFrame")
    i = 0
    for item in data:
        solution_id = item['id']
        try:
            contest_id = item['contestId']        
        except:
            contest_id = 0
        submission_time = item['creationTimeSeconds']
        relative_time = item['relativeTimeSeconds']
        # language = get_EXT(item['programmingLanguage'])
        language = item['programmingLanguage']
        try:
            verdict = item['verdict']
        except:
            verdict = ''
        test_case = item['passedTestCount']
        time = item['timeConsumedMillis']
        memory = item['memoryConsumedBytes']/1024
        
        # Problem Data
        problem = item['problem']
        problem_index = problem['index']
        try:
            problem_name = problem['name']
        except:
            problem_name = ''
        problem_type = problem['type']
        try:
            points = problem['points']
        except:
            points = 0
        tags = problem['tags']
        
        # Author data
        author = item['author']
        if len(author['members'])>1:
            team = 1
        else:
            team = 0        
        participant_type = author['participantType']

        # add row
        df.loc[i] = [solution_id,contest_id,submission_time,relative_time,problem_index,problem_name,problem_type,points,tags,team,participant_type,language,verdict,test_case,time,memory]
        i += 1

    return df

def user_rating_change(handle='kashyap_archit'):
    '''
    Input : 
        handle name\n
    Output : returns a dataframe containing
        1. contest_id
        2. conteat_name
        3. rank
        4. old (rating)
        5. new (rating)
    '''
    print("Loading user rating changes for "+handle)
    url = user_rating_url.format(handle=handle)
    data = load_url(url)
    if data is None:
        return None

    df = pd.DataFrame(columns=['contest_id','contest_name','rank','old','new'])
    
    print(tab+'Creating DataFrame')
    i = 0
    for item in data:
        contest_id = item['contestId']
        contest_name = item['contestName']
        rank = item['rank']
        old = item['oldRating']
        new = item['newRating']
        
        # add row
        df.loc[i] = [contest_id,contest_name,rank,old,new]
        i += 1
    return df

def data_process(handle):
    '''
    Results out a processed dataframe to work on futher.
    Contains:
        1. solution_id(as index)
        2. contest_id
        3. time (datetime, year-month-day)
        4. problem_index
        5. tags
        6. participant_type (CONTESTANT, PRACTICE, VIRTUAL, MANAGER, OUT_OF_COMPETITION)
        7. verdict 
    '''
    data = ld.load_data(handle)
    if data is None:
        return None
    
    
    data.set_index('solution_id', inplace=True)
    
    data.drop(columns=['time','memory','test_case','language','team','points','problem_type','problem_name','relative_time','Unnamed: 0'], inplace=True)
    data.rename(columns={"submission_time":"time"}, inplace=True)
    # data['time'] = data['time'].apply(lambda x: datetime.utcfromtimestamp(x).strftime('%Y-%m-%d'))
    # data['time'] = data['time'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').date())
    return data