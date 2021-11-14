from urllib.parse import urlparse
import psycopg2

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