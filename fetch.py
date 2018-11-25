import json
import urllib.request as url_req
import pandas as pd

tab = '    '
url_base = 'https://codeforces.com/api/'

def list_all_contest():
    '''
    Gives a list of all contest uptill now, excluding the gym.
    '''
    url = url_base+'contest.list?gym=false'
    print("Fetching contest list")
    try:
        json_obj = url_req.urlopen(url)
    except:
        return None
    data = json.load(json_obj)

    if data['status'] != 'OK':
        print (tab + "Error while fetching data: " + data['comment'])
        return None
    else:
        data = data['result']

    data = pd.DataFrame.from_dict(data)
    data = data[data.phase=='FINISHED']['id']
    return list(data)

def get_solved(contestID):
    '''
    Retuns the questions done by each contestant in the given contest and the rating of the user.
    '''
    url = url_base +'contest.standings?contestId=' + str(contestID) + '&from=1&count=99999&showUnofficial=false'
    # print("Loading contest data", contestID)
    print(1, contestID)
    try:
        json_obj = url_req.urlopen(url)
    except:
        return None
    data = json.load(json_obj)

    if data['status'] != 'OK':
        print (tab + "Error while fetching data: " + data['comment'])
        return None
    else:
        data = data['result']

    # contest = data['contest'] # contest description
    problems = data['problems'] # all the problems in the contest
    rows = data['rows'] # ranklist

    # considering only the first user if the contest is given in team
    member = [] # consists of the handle name
    solved = [] # shows whether the quesiton was solved or not

    for x in rows:
        member.append(x['party']['members'][0]['handle'])
        flag = [0]*len(problems) # quesiton solved or not
        for p in range(len(problems)):
            # for the p'th question
            if x['problemResults'][p]['points'] > 0:
                flag[p] = 1
        solved.append(flag) 
        
    # get rating of users who attempted the contest 
    url = url_base + 'contest.ratingChanges?contestId=' + str(contestID)
    # print("Loading ratings of user who attempted the contest")
    print(2)
    try:
        json_obj = url_req.urlopen(url)
    except:
        return None
    data = json.load(json_obj)

    if data['status'] != 'OK':
        print (tab + "Error while fetching data: " + data['comment'])
        return None
    else:
        data = data['result']
    
    if len(data)==0:
        print(tab+'Contest data not available',contestID)
        return None

    rating = {}
    for x in data:
	    rating[x['handle']] = x['oldRating']

    df = []
    for i in range(len(member)): 
	    user = member[i]
	    r = rating[user]
	    for j, p in enumerate(problems): 
	        dt = dict.fromkeys(['handle', 'rating', 'contestID', 'problemID', 'success'])
	        dt['handle'] = user
	        dt['contestID'] = contestID
	        dt['problemID'] = p['index']
	        dt['success'] = solved[i][j]
            # rating before the contest
	        dt['rating'] = r
	        df.append(dt)

    return (pd.DataFrame.from_dict(df))

# print(get_solved(1078).head(20))
# print(list_all_contest())
