import sqlite3

# подключение к базе данных и получение токенов
con = sqlite3.connect("database.db")
cur = con.cursor()

res = cur.execute("SELECT id_token from token")
TG_TOKEN = res.fetchone()[0]
AI_TOKEN = res.fetchone()[0]
print(res.fetchall())
print(f'{TG_TOKEN}\n{AI_TOKEN}')


cur.close()
con.close()