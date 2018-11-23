import load_data as ld
import pandas as pd

def tried(handle):
    data = ld.load_data(handle)
    if type(data) is int:
        print ("Error while loading csv file")
        return 0

    tried = data[['contest_id', 'problem_index']].astype(str).sum(axis=1).unique()
    return (len(tried))

def solved(handle):
    data = ld.load_data(handle)
    if type(data) is int:
        print ("Error while loading csv file")
        return 0

    filtered_file = data[data.verdict=='OK']
    unique_data = filtered_file[['contest_id', 'problem_index']].astype(str).sum(axis=1).unique()
    return (len(unique_data))
    
def unsolved_problem(handle):
    data=ld.load_data(handle)
    if type(data) is int:
        print ("Error while loading csv file")
        return 0

    filtered_file=data[data.verdict=='OK']
    solved=filtered_file[['contest_id', 'problem_index']].astype(str).sum(axis=1).unique()
    all_=data[['contest_id', 'problem_index']].astype(str).sum(axis=1).unique()
    unsolve=[]
    for prob in all_:
        if prob not in solved:
            unsolve.append(prob)
    return (unsolve)

def number_of_contest(handle):
    data=ld.load_data(handle)
    if type(data) is int:
        print ("Error while loading csv file")
        return 0

    filtered_file=data[data.participant_type=='CONTESTANT']
    all_cont=filtered_file['contest_id'].astype(str).unique()
    return (len(all_cont))


def max_attempts_on_single_problem(handle):
    data=ld.load_data(handle)
    if type(data) is int:
        print ("Error while loading csv file")
        return 0

    dic={}
    maxi=0
    for index, row in data.iterrows():
        problem=str(row.problem_name)+str(row.contest_id)
        dic[problem]=dic.get(problem,0)+1
        maxi=max(maxi,dic[problem])
    return (maxi)


def ac_one_submission(handle):
    data=ld.load_data(handle)
    if type(data) is int:
        print ("Error while loading csv file")
        return 0

    dic={}
    coun=0
    for index, row in data.iterrows():
        problem=str(row.problem_name)+str(row.contest_id)
        dic[problem]=[]

    for index, row in data.iterrows():
        problem=str(row.problem_name)+str(row.contest_id)
        dic[problem].append(row.verdict)
    for id_ in dic:
        if dic[id_][len(dic[id_])-1]=='OK':coun+=1
    return (coun)
