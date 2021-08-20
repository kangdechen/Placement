import pandas as pd
import re
import pandas as pd

df = pd.read_csv("C:\\Users\\a0023\\PycharmProjects\\MasterProject\\Dataset\\food_table.csv", encoding='utf-8',
                 thousands=',')

df["title"]

for string in df["title"]:
    encoded_string = string.encode("ascii", "ignore")
    decode_string = encoded_string.decode()

    df.loc[df['title'] == string, 'title'] = decode_string
    print(string)
for string in df["title"] :

    print(string)


df.to_csv('C:\\Users\\a0023\\PycharmProjects\\MasterProject\\Dataset\\food_table.csv', index=False)
