import sqlite3

db_locale = 'player.db'
conn = sqlite3.connect(db_locale)
c = conn.cursor()
c.execute('PRAGMA foreign_keys = ON')

# Heroes table
c.execute("""
    CREATE TABLE IF NOT EXISTS heroes (
        name TEXT PRIMARY KEY NOT NULL,
        class TEXT NOT NULL CHECK (class IN ('Tank', 'Damage', 'Healer'))
    );
""")

# Player details table
c.execute("""
    CREATE TABLE IF NOT EXISTS player_details (
        player_id TEXT PRIMARY KEY NOT NULL,
        most_played_hero TEXT NOT NULL,
        average_KDA REAL NOT NULL,
        win_rate REAL NOT NULL,
        rank TEXT NOT NULL CHECK (rank IN ('Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond', 'Master', 'Grandmaster')),
        CHECK (player_id GLOB '*#[0-9][0-9][0-9][0-9]')
    );
""")

# Matches table
c.execute("""
    CREATE TABLE IF NOT EXISTS Matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        map_name TEXT NOT NULL,
        game_rank TEXT NOT NULL,
        winner_team INTEGER NOT NULL CHECK (winner_team IN (1,2)),
        team1_player1 TEXT NOT NULL,
        team1_player2 TEXT NOT NULL,
        team1_player3 TEXT NOT NULL,
        team1_player4 TEXT NOT NULL,
        team1_player5 TEXT NOT NULL,
        team2_player1 TEXT NOT NULL,
        team2_player2 TEXT NOT NULL,
        team2_player3 TEXT NOT NULL,
        team2_player4 TEXT NOT NULL,
        team2_player5 TEXT NOT NULL,
        FOREIGN KEY(team1_player1) REFERENCES player_details(player_id),
        FOREIGN KEY(team1_player2) REFERENCES player_details(player_id),
        FOREIGN KEY(team1_player3) REFERENCES player_details(player_id),
        FOREIGN KEY(team1_player4) REFERENCES player_details(player_id),
        FOREIGN KEY(team1_player5) REFERENCES player_details(player_id),
        FOREIGN KEY(team2_player1) REFERENCES player_details(player_id),
        FOREIGN KEY(team2_player2) REFERENCES player_details(player_id),
        FOREIGN KEY(team2_player3) REFERENCES player_details(player_id),
        FOREIGN KEY(team2_player4) REFERENCES player_details(player_id),
        FOREIGN KEY(team2_player5) REFERENCES player_details(player_id)
    );
""")

# Player match details table
c.execute("""
    CREATE TABLE IF NOT EXISTS player_match_details (
        player_id TEXT NOT NULL,
        match_id INTEGER NOT NULL,
        map_name TEXT NOT NULL,
        hero_name TEXT NOT NULL,
        hero_class TEXT NOT NULL,
        kills INTEGER NOT NULL,
        deaths INTEGER NOT NULL,
        assists INTEGER NOT NULL,
        damage_done INTEGER NOT NULL,
        damage_taken INTEGER NOT NULL,
        healing_done INTEGER NOT NULL,
        FOREIGN KEY (player_id) REFERENCES player_details(player_id) ON DELETE CASCADE,
        FOREIGN KEY (match_id) REFERENCES Matches(id) ON DELETE CASCADE,
        FOREIGN KEY (hero_name) REFERENCES heroes(name) ON DELETE CASCADE,
        -- Removed foreign key for hero_class as 'class' in heroes is not unique
        PRIMARY KEY (player_id, match_id)
    );
""")

conn.commit()
conn.close()
