import user_data 

df = user_data.load_user_data()  
# df = user_data.user_rating_change(handle='Mindjolt')
# if df==3:
#     print("Error while loading data")
# else:
#     print(df.head())
print(df.head())
df.to_csv('kashyap.csv')