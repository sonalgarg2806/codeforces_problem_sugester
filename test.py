import user.user_data as ud
import user.tags as tg
import user.verdict as vd
import user.level as lv
import user.language as lg
import user.some_number_about_users as dt
import fetch as fd
import elo
import pandas as pd
import warnings
import os

warnings.filterwarnings("ignore")
handle = 'indian_ocean7'

df = ud.load_user_data(handle)  
df.to_csv(handle+'.csv')
tg.tags_chart(handle)
vd.verdict_graph(handle)
lv.levels(handle)
lg.language_graph(handle)
print ('all tried ',dt.tried(handle))
print ('all solved ',dt.solved(handle))
print ('all unsolved ',dt.unsolved_problem(handle))
print ('total contest ',dt.number_of_contest(handle))
print ('max_attempts_on_single_problem ',dt.max_attempts_on_single_problem(handle))
print ('ac_one_submission',dt.ac_one_submission(handle))

if os.path.isfile('problem_rating.csv')==False:
    contest_list = fd.list_all_contest()
    df = pd.DataFrame(columns=["contestID", "problemID", "problemRating"])

    for i in contest_list:
        temp = elo.get_contest_elo(i)
        if temp is not None:
            df = df.append(temp)
    df.to_csv('problem_rating.csv')
    df = elo.add_tags()
    df.to_csv('problem_rating.csv')

