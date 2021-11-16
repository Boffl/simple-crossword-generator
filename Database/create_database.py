from urllib.parse import urlparse
import psycopg2
from PyDictionary import PyDictionary
import wordfreq
from pandas import read_csv

dictionary = PyDictionary()

df = read_csv('most-common-nouns-english.csv') # id word plural
# for word in df['Word']:
#     print(word, dictionary.meaning(word)['Noun'][0], wordfreq.zipf_frequency(word, 'en'))


# same definitions as in PyDictionary, but could be useful for hints (Exampl usage)
# from nltk.corpus import wordnet
# syns = wordnet.synsets("walk")
# print("Defination of the said word:")
# print(syns[0].definition())
# print("\nExamples of the word in use::")
# print(syns[0].examples())



# Words to use: ca 1000, nouns and verbs

# for i, word in enumerate(wordfreq.iter_wordlist('en', wordlist='best')):
#     print(word, wordfreq.zipf_frequency(word, 'en'))
#     print(dictionary.meaning(word))
#     if i > 10:
#         break



# Todo:
    # get the words from the Pydictionary and feed them into the db
    # https://github.com/geekpradd/PyDictionary


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
cur.execute('''CREATE TABLE IF NOT EXISTS words (id int PRIMARY KEY, word text, definition text, Zipf_freq float)''')
sql = '''INSERT INTO words (id, word, definition, zipf_freq)
            Values (%s, %s, %s, %s); '''

for i, word in enumerate(df['Word']):
    try:
        data = i, word, dictionary.meaning(word)['Noun'][0], wordfreq.zipf_frequency(word, 'en')

        cur.execute(sql, data)
    except:
        continue

connection.commit()
cur.close()
connection.close()
# for i, word in enumerate(df['Word']):
#     cur.execute('''INSERT INTO words''')
# # df.to_sql('characters', connection, if_exists='replace', index=False)