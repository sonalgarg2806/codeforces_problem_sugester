import numpy as np
import pandas as pd
import fetch as fd
import user.user_data as ud
import math
from collections import defaultdict

MIN = 0.0
MAX = 5000.0
url_base = 'https://codeforces.com/api/'

def get_win_prob(ri, rj): # probability that rating ri beats rating rj
    return 1.0 / (1.0 + math.pow(10, (rj-ri) / 400.0))

def process_row(r):
    return get_win_prob(r["rating"], r["problemRating"])

def get_problem_elo(problem_df):
    # rowCnt = problem_df.shape[0]
    solveCnt = np.sum(problem_df.success)

    lo = MIN
    hi = MAX

    for i in range(50):
        mid = (lo + hi) / 2.0
        problem_df["problemRating"] = mid 
        expSolve = np.sum(problem_df.apply(process_row, axis = 1))

        if solveCnt > expSolve:
            hi = mid
        else:
            lo = mid
    return int(round((lo + hi) / 2.0))

def get_contest_elo(contestID):
    try:
        data = fd.get_solved(contestID)
    except:
        return None
    
    if (data is None) or (data.shape[0] < 20):
        return None
    # print("Calculating elo rating for",contestID)
    print(3, contestID)

    contestID = data.contestID[0]
    problem = data.problemID.unique()

    res = defaultdict(list)

    for p in problem:
        problemRating = get_problem_elo(data[data.problemID==p]) 

        res["contestID"].append(contestID)
        res["problemID"].append(p)
        res["problemRating"].append(problemRating)

    return pd.DataFrame(res)

def add_tags():
    '''
    Add tags to the question rating.
    '''
    data = pd.read_csv("problem_rating.csv")
    data.drop(columns=['Unnamed: 0'], inplace=True)
    data['tag'] = [None]*len(data)
    url_standings = url_base +'contest.standings?contestId={contestID}&from=1&count=1&showUnofficial=false'

    for i in range(len(data)):
        print(i)
        url = url_standings.format(contestID=data.ix[i, 'contestID'])
        problem = ud.load_url(url)
        problem = problem['problems']

        for p in problem:
            if p['index']==data.ix[i,'problemID']:
                data.at[i,'tag'] = p['tags']
                break
    return data

# print(add_tags().head())
# print(get_contest_elo(1063))