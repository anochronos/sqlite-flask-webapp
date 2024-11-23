import sqlite3

db_locale = 'player.db'
conn = sqlite3.connect(db_locale)
c = conn.cursor()

c.execute("""
    SELECT * FROM player_details
""")

player_info = c.fetchall()
for player in player_info:
    print(player)

conn.commit()
conn.close()