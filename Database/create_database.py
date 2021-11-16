from urllib.parse import urlparse
import psycopg2
import wordfreq
from pandas import read_csv
import requests
import re
from tqdm import tqdm
import time

# 1000 most common english nouns:
df = read_csv('most-common-nouns-english.csv') # dataframe with three columns: id word plural

# same definitions as in PyDictionary, but could be useful for hints (Exampl usage)
# from nltk.corpus import wordnet
# syns = wordnet.synsets("walk")
# print("Defination of the said word:")
# print(syns[0].definition())
# print("\nExamples of the word in use::")
# print(syns[0].examples())



# Words to use: ca 1000, nouns

# for i, word in enumerate(wordfreq.iter_wordlist('en', wordlist='best')):
#     print(word, wordfreq.zipf_frequency(word, 'en'))
#     print(dictionary.meaning(word))
#     if i > 10:
#         break



# getting the database from the uri:
result = urlparse("postgres://postgres:22b216c54a2bd9c527c5d340b5b9901f@172.23.115.113:55079/team_a_db")

username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname
port = result.port


# # creating a file, to view the data (to input it into pycharm)
# with open('database_meta.txt', 'w', encoding='utf-8') as outfile:
#     outfile.write(f"database: {database}\n"
#                   f"username: {username}\n"
#                   f"password: {password}\n"
#                   f"port: {port}\n"
#                   f"hostname: {hostname}")

# Connecting to the database
connection = psycopg2.connect(
    database = database,
    user = username,
    password = password,
    host = hostname,
    port = port
)
cur = connection.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS words_2 (id int PRIMARY KEY, word text, definition text, hint text, zipf_freq float)''')
sql = '''INSERT INTO words_3 (id, word, definition, hint, zipf_freq)
            Values (%s, %s, %s, %s, %s); '''

for i, word in tqdm(enumerate(df['Word']), total=1000):
    # if i > 10:
    #     break
    if len(word) > 2:  # some weird words,
        # try:
        response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
        json_data = response.json() if response and response.status_code == 200 else None

        # if we have too many api calls:
        counter = 0
        while not json_data and counter < 1: # tried with multiple tries, but I think just one try with enough time is enough...
            print(f'"{word}" not found, try again in 20s')
            time.sleep(20)
            # try again
            json_data = response.json() if response and response.status_code == 200 else None
            counter += 1
        if not json_data: # if the word is just not existent in the api data base
            print(f'"{word}" not found and will not try again')
        else:
            # finding and checking the pos-tag (to prevent some weird words, which slipped in the data, like "no.")
            try:
                pos = json_data[0]['meanings'][0]['partOfSpeech']
                if pos != 'noun':
                    continue
            except:
                print(f"couln't find pos for {word}")
                continue

            definition = json_data[0]['meanings'][0]['definitions'][0]['definition']
            try:
                hint = re.sub(word.lower(), '***', json_data[0]['meanings'][0]['definitions'][0]['example'].lower())
            except KeyError:
                hint = ''
            zipf_freq = wordfreq.zipf_frequency(word, 'en')
            data = i, word, definition, hint, zipf_freq
            # data = i, word, dictionary.meaning(word)['Noun'][0], wordfreq.zipf_frequency(word, 'en')

            cur.execute(sql, data)
        # except TypeError:
        #     print('TypeError')
        #     print(data)
        #     continue

connection.commit()
cur.close()
connection.close()


# for i, word in enumerate(df['Word']):
#     cur.execute('''INSERT INTO words''')
# # df.to_sql('characters', connection, if_exists='replace', index=False)