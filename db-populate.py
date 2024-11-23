import sqlite3

db_locale = 'player.db'
conn = sqlite3.connect(db_locale)
c = conn.cursor()

c.execute("""
    INSERT INTO player_details(
            character_name,
            character_class,
            kills,
            deaths,
            assists,
            damage_done,
            damage_taken,
            healing_done
        ) VALUES

        ('Reinhardt', 'Tank', 100, 10, 50, 10000, 5000, 1000),
        ('Roadhog', 'Tank', 200, 5, 100, 20000, 10000, 2000),
        ('Tracer', 'Damage', 150, 15, 75, 15000, 7500, 1500),
        ('Soldier 76', 'Damage', 75, 25, 25, 7500, 2500, 500),
        ('Kiriko', 'Healer', 25, 75, 10, 2500, 750, 250)
""")



conn.commit()
conn.close()