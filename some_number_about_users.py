import pandas as pd
def tried(username):
    csv_file=pd.read_csv(username+".csv")
    tried=csv_file[['contest_id', 'problem_index']].astype(str).sum(axis=1).unique()
    return (len(tried))

def solved(username):
    csv_file=pd.read_csv(username+".csv")
    filtered_file=csv_file[csv_file.verdict=='OK']
    unique_data=filtered_file[['contest_id', 'problem_index']].astype(str).sum(axis=1).unique()
    return (len(unique_data))
def unsolved_problem(username):
        csv_file=pd.read_csv(username+".csv")
        filtered_file=csv_file[csv_file.verdict=='OK']
        solved=filtered_file[['contest_id', 'problem_index']].astype(str).sum(axis=1).unique()
        all_=csv_file[['contest_id', 'problem_index']].astype(str).sum(axis=1).unique()
        unsolve=[]
        for prob in all_:
                if prob not in solved:
                        unsolve.append(prob)
        return (unsolve)
def number_of_contest(username):
        csv_file=pd.read_csv(username+".csv")
        filtered_file=csv_file[csv_file.participant_type=='CONTESTANT']
        all_cont=filtered_file['contest_id'].astype(str).unique()
        return (len(all_cont))


def max_attempts_on_single_problem(username):
        csv_file=pd.read_csv(username+".csv")
        dic={}
        maxi=0
        for index, row in csv_file.iterrows():
                problem=str(row.problem_name)+str(row.contest_id)
                dic[problem]=dic.get(problem,0)+1
                maxi=max(maxi,dic[problem])
        return (maxi)


def ac_one_submission(username):
        csv_file=pd.read_csv(username+".csv")
        dic={}
        coun=0
        for index, row in csv_file.iterrows():
                problem=str(row.problem_name)+str(row.contest_id)
                dic[problem]=[]

        for index, row in csv_file.iterrows():
                problem=str(row.problem_name)+str(row.contest_id)
                dic[problem].append(row.verdict)
        for id_ in dic:
                if dic[id_][len(dic[id_])-1]=='OK':coun+=1
        return (coun)



print (tried('kashyap_archit'))
print (solved('kashyap_archit'))
print (unsolved_problem('kashyap_archit'))
print (number_of_contest('kashyap_archit'))
print (max_attempts_on_single_problem('kashyap_archit'))
print (ac_one_submission('kashyap_archit'))

