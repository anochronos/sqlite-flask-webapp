import sqlite3

db_locale = 'player.db'
conn = sqlite3.connect(db_locale)
c = conn.cursor()

c.execute("""
    CREATE TABLE player_details
        (
            id INTEGER PRIMARY KEY,
            character_name TEXT,
            character_class TEXT,
            kills INTEGER,
            deaths INTEGER,
            assists INTEGER,
            damage_done INTEGER,
            damage_taken INTEGER,
            healing_done INTEGER
        )
""")



conn.commit()
conn.close()