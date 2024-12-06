import sqlite3
import random
import json

# Database setup
db_locale = 'player.db'
conn = sqlite3.connect(db_locale)
c = conn.cursor()

# Load heroes from JSON
with open('heroes.json') as f:
    heroes = json.load(f)
hero_names = [hero['name'] for hero in heroes]
hero_classes = {hero['name']: hero['class'] for hero in heroes}
hero_data = [(hero['name'], hero['class']) for hero in heroes]
c.executemany("""INSERT INTO heroes (name, class) VALUES (?, ?)""", hero_data)

# Pool of actual names
names = [
    "Alice", "Bob", "Charlie", "Diana", "Ethan", "Fiona", "Greg", "Hannah",
    "Ivan", "Jill", "Kevin", "Laura", "Michael", "Natalie", "Oscar", "Paul",
    "Quincy", "Rachel", "Sam", "Tina", "Uma", "Victor", "Wendy", "Xavier",
    "Yvonne", "Zack"
]

# Generate random players
ranks = ['Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond', 'Master', 'Grandmaster']
player_count = 50  # Number of players to add
players = []

for name in random.sample(names, len(names)):
    for _ in range(2):  # Allow multiple players with same name but unique IDs
        player_id = f"{name}#{random.randint(1000, 9999)}"
        most_played_hero = random.choice(hero_names)
        average_KDA = round(random.uniform(1.0, 5.0), 1)
        win_rate = round(random.uniform(0.3, 0.8), 2)
        rank = random.choice(ranks)
        players.append((player_id, most_played_hero, average_KDA, win_rate, rank))

# Insert players into the database
c.executemany("""
    INSERT INTO player_details (player_id, most_played_hero, average_KDA, win_rate, rank)
    VALUES (?, ?, ?, ?, ?)
""", players)

# Generate random matches
maps = ["King's Row", "Hanamura", "Watchpoint: Gibraltar", "Ilios", "Route 66"]
match_count = 20  # Number of matches to add

for match_index in range(match_count):
    map_name = random.choice(maps)
    game_rank = random.choice(ranks)
    winner_team = random.choice([1, 2])

    # Randomly select 10 unique players
    match_players = random.sample([p[0] for p in players], 10)

    match_data = (
        map_name, game_rank, winner_team,
        match_players[0], match_players[1], match_players[2], match_players[3], match_players[4],
        match_players[5], match_players[6], match_players[7], match_players[8], match_players[9]
    )
    
    # Insert match into Matches table
    c.execute("""
        INSERT INTO Matches (
            map_name, game_rank, winner_team, 
            team1_player1, team1_player2, team1_player3, team1_player4, team1_player5,
            team2_player1, team2_player2, team2_player3, team2_player4, team2_player5
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, match_data)

    # Get match ID of inserted match
    match_id = c.lastrowid

    # Generate player_match_details for this match
    player_match_details = []
    for i, player_id in enumerate(match_players):
        hero_name = random.choice(hero_names)
        hero_class = hero_classes[hero_name]
        kills = random.randint(0, 25)
        deaths = random.randint(0, 15)
        assists = random.randint(0, 30)
        damage_done = random.randint(5000, 30000)
        damage_taken = random.randint(2000, 20000)
        healing_done = random.randint(0, 15000) if hero_class == "Healer" else 0
        player_match_details.append(
            (player_id, match_id, map_name, hero_name, hero_class, kills, deaths, assists, damage_done, damage_taken, healing_done)
        )

    # Insert player_match_details into the database
    c.executemany("""
        INSERT INTO player_match_details (
            player_id, match_id, map_name, hero_name, hero_class, kills, deaths, assists, damage_done, damage_taken, healing_done
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, player_match_details)

# Commit and close the database
conn.commit()
conn.close()
