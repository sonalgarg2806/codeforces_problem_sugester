import user_data as ud
import tags as tg
import verdict as vd
import level as lv
import language as lg
import some_number_about_users as dt

df = ud.load_user_data(handle='Ashishgup')  
# df = ud.user_rating_change(handle='Ashishgup')
# if df==3:
#     print("Error while loading data")
# else:
#     print(df.head())
# print(df.head())
df.to_csv('Ashishgup.csv')
tg.tags_chart(handle='Ashishgup')
vd.verdict_graph(handle='Ashishgup')
lv.levels(handle='Ashishgup')
lg.language_graph(handle='Ashishgup')
print ('all tried ',dt.tried(handle='Ashishgup'))
print ('all solved ',dt.solved(handle='Ashishgup'))
print ('all unsolved ',dt.unsolved_problem(handle='Ashishgup'))
print ('total contest ',dt.number_of_contest(handle='Ashishgup'))
print ('max_attempts_on_single_problem ',dt.max_attempts_on_single_problem(handle='Ashishgup'))
print ('ac_one_submission',dt.ac_one_submission(handle='Ashishgup'))