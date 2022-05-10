from urllib.parse import urlparse
import psycopg2
import wordfreq
from pandas import read_csv
import requests
import re
from tqdm import tqdm
import time
import os

# 1000 most common english nouns:
df = read_csv('most-common-nouns-english.csv') # dataframe with three columns: id word plural

# connecting to the database from the uri:
result = urlparse(os.environ['DATABASE_URL'])

username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname
port = result.port

# Connecting to the database
connection = psycopg2.connect(
    database = database,
    user = username,
    password = password,
    host = hostname,
    port = port
)
cur = connection.cursor()

# # creating a file, to view the metadata (to input it into pycharm or pgAdmin)
# with open('database_meta.txt', 'w', encoding='utf-8') as outfile:
#     outfile.write(f"database: {database}\n"
#                   f"username: {username}\n"
#                   f"password: {password}\n"
#                   f"port: {port}\n"
#                   f"hostname: {hostname}")


# inserting into the database
cur.execute('''CREATE TABLE IF NOT EXISTS words_3 (id int PRIMARY KEY, word text, definition text, hint text, zipf_freq float)''')
sql = '''INSERT INTO words_3 (id, word, definition, hint, zipf_freq)
            Values (%s, %s, %s, %s, %s); '''

for i, word in tqdm(enumerate(df['Word']), total=1000):

    word = re.sub(r"['\.\?,!]", '', word)  # for some reason there is some words with punctuation in there.....

    if len(word) > 2:  # some weird words with one or two letters are weird, also not very useful for a crossword puzzle

        response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}') # awesome dictionary api :)
        json_data = response.json() if response and response.status_code == 200 else None

        # if we have too many api calls:
        counter = 0
        while not json_data and counter < 1:  # tried with multiple tries, but I think just one try with enough time is enough...
            print(f'"{word}" not found, try again in 20s')
            time.sleep(20)
            # try again
            json_data = response.json() if response and response.status_code == 200 else None
            counter += 1
        if not json_data:  # enough tries, the word does not exist in the api
            print(f'"{word}" not found and will not try again')
        else:
            # finding and checking the pos-tag (to prevent some weird words, which slipped in the data, like "no.")
            try:
                pos = json_data[0]['meanings'][0]['partOfSpeech']
                if pos != 'noun':
                    continue
            except: # this never happens so far
                print(f"couln't find pos for {word}")
                continue

            definition = json_data[0]['meanings'][0]['definitions'][0]['definition']
            try:
                # the hint is the example usage, with the word blanked out
                hint = re.sub(word.lower(), '***', json_data[0]['meanings'][0]['definitions'][0]['example'].lower())
            except KeyError:
                hint = ''
            zipf_freq = wordfreq.zipf_frequency(word, 'en')
            data = i, word, definition, hint, zipf_freq
            cur.execute(sql, data)

connection.commit()
cur.close()
connection.close()

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