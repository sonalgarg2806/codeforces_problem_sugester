# Fetch user data and contest data from CF
import json
import urllib.request as url_req
import pandas as pd
import numpy as np

ERROR_LOADING = 3
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
        return ERROR_LOADING

    data = json.load(json_obj)
    
    if data['status'] != 'OK':
        print (tab + "Error while loading user data: " + data['comment'])
        return ERROR_LOADING
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
        3. submission_time (time at which submission was made)
        4. realtive_time (time after contest at which submission was made)
        3. problem_index
        4. problem_name (if available)
        5. problem_type
        6. points (if the question is not rated then it is 0)
        7. tags
        8. team (individual or team)
        9. participant_type (virtual, contest, practice)
        10.language
        11.verdict
        12.test_case (number of test cases passed)
        13.time (in milliseconds)
        14.memory (in kilo-bytes) 
    '''
    print("Loading user data for "+handle)
    # try:
    #     json_obj = url_req.urlopen(user_status_url.format(handle=handle, start=start, count=count))
    # except:
    #     print(tab+"Error while loading user data: Either user handle is wrong or the start number is wrong.")
    #     return ERROR_LOADING

    # data = json.load(json_obj)
    
    # if data['status'] != 'OK':
    #     print (tab + "Error while loading user data: " + data['comment'])
    #     return ERROR_LOADING
    # else:
    #     data = data['result']
    url = user_status_url.format(handle=handle, start=start, count=count)
    data = load_url(url)


    df = pd.DataFrame(columns=['solution_id','contest_id','submission_time','realtive_time','problem_index','problem_name','problem_type','points','tags','team','participant_type','language','verdict','test_case','time','memory'])
    
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
    # try:
    #     json_obj = url_req.urlopen(user_rating_url.format(handle=handle))
    # except:
    #     print(tab+"Error while loading user data: Please enter valid user handle.")
    #     return ERROR_LOADING

    # data = json.load(json_obj)
    
    # if data['status'] != 'OK':
    #     print (tab + "Error while loading user data: " + data['comment'])
    #     return ERROR_LOADING
    # else:
    #     data = data['result']
    url = user_rating_url.format(handle=handle)
    data = load_url(url)

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