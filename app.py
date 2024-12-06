from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import re

app = Flask(__name__)
db_locale = 'player.db'

@app.route('/')
@app.route('/home', methods=['POST', 'GET'])
def home_page():
    return render_template('home.html')

@app.route('/all_players', methods=['POST', 'GET'])
def all_players():
    player_data = query_player_details()
    return render_template('all_players.html', player_data=player_data)

@app.route('/search_results', methods=['POST', 'GET'])
def search_player():
    user_id = request.form.get('user_id', '').strip()
    filter_option = request.form.get('filter_option')
    selected_class = request.form.get('class_select')
    selected_rank = request.form.get('rank_select')
    selected_map = request.form.get('map_select')

    player_data = query_player_details(
        user_id=user_id if user_id else None,
        hero_class=selected_class,
        rank=selected_rank,
        map_name=selected_map
    )
    matches_data = query_matches(
        user_id=user_id if user_id else None,
        map_name=selected_map,
        selected_rank=selected_rank
    )

    if filter_option == 'player':
        return render_template('player_results.html',
                               player_data=player_data,
                               matches_data=matches_data,
                               selected_filter=filter_option,
                               selected_map=selected_map,
                               selected_class=selected_class,
                               selected_rank=selected_rank)
    elif filter_option == 'matches':
        all_ranks = ["Bronze","Silver","Gold","Platinum","Diamond","Master","Grandmaster"]
        all_maps = ["King's Row","Watchpoint: Gibraltar","Hollywood","Eichenwalde"]
        all_players = query_all_players()
        return render_template('match_results.html',
                               player_data=player_data,
                               matches_data=matches_data,
                               selected_filter=filter_option,
                               selected_map=selected_map,
                               selected_class=selected_class,
                               selected_rank=selected_rank,
                               all_players=all_players,
                               all_ranks=all_ranks,
                               all_maps=all_maps
                               )
    else:
        # If no filter selected, just show all players by default
        all_players_data = query_player_details()
        return render_template('player_results.html',
                               player_data=all_players_data,
                               matches_data=[],
                               selected_filter=None,
                               selected_map="",
                               selected_class="",
                               selected_rank="")

@app.route('/get_player_match_stats')
def get_player_match_stats():
    player_id = request.args.get('player_id')
    match_id = request.args.get('match_id')
    player_match_data = query_player_match_stats(player_id, match_id)

    result = {}
    if player_match_data:
        row = player_match_data[0]
        # Assuming schema: player_id, match_id, map_name, hero_name, hero_class, kills, deaths, assists, damage_done, damage_taken, healing_done
        result = {
            "player_id": row[0],
            "match_id": row[1],
            "map_name": row[2],
            "hero_name": row[3],
            "hero_class": row[4],
            "kills": row[5],
            "deaths": row[6],
            "assists": row[7],
            "damage_done": row[8],
            "damage_taken": row[9],
            "healing_done": row[10]
        }

    return jsonify(result)

def delete_match(match_id):
    conn = sqlite3.connect(db_locale)
    c = conn.cursor()
    c.execute("DELETE FROM Matches WHERE id = ?", (match_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('search_player'))

@app.route('/add_match', methods=['POST'])
def add_match():
    map_name = request.form.get('map_name', '').strip()
    game_rank = request.form.get('game_rank', '').strip()
    winner_team = request.form.get('winner_team', '').strip()

    team1_player1 = request.form.get('team1_player1', '').strip()
    team1_player2 = request.form.get('team1_player2', '').strip()
    team1_player3 = request.form.get('team1_player3', '').strip()
    team1_player4 = request.form.get('team1_player4', '').strip()
    team1_player5 = request.form.get('team1_player5', '').strip()

    team2_player1 = request.form.get('team2_player1', '').strip()
    team2_player2 = request.form.get('team2_player2', '').strip()
    team2_player3 = request.form.get('team2_player3', '').strip()
    team2_player4 = request.form.get('team2_player4', '').strip()
    team2_player5 = request.form.get('team2_player5', '').strip()

    conn = sqlite3.connect(db_locale)
    c = conn.cursor()
    c.execute("""
        INSERT INTO Matches (map_name, game_rank, winner_team, 
        team1_player1, team1_player2, team1_player3, team1_player4, team1_player5,
        team2_player1, team2_player2, team2_player3, team2_player4, team2_player5)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (map_name, game_rank, winner_team, team1_player1, team1_player2, team1_player3, team1_player4, team1_player5,
          team2_player1, team2_player2, team2_player3, team2_player4, team2_player5))
    conn.commit()
    conn.close()

    return redirect(url_for('search_player'))

@app.route('/update_match/<int:match_id>', methods=['POST'])
def update_match(match_id):
    map_name = request.form.get('map_name', '').strip()
    game_rank = request.form.get('game_rank', '').strip()
    winner_team = request.form.get('winner_team', '').strip()

    team1_player1 = request.form.get('team1_player1', '').strip()
    team1_player2 = request.form.get('team1_player2', '').strip()
    team1_player3 = request.form.get('team1_player3', '').strip()
    team1_player4 = request.form.get('team1_player4', '').strip()
    team1_player5 = request.form.get('team1_player5', '').strip()

    team2_player1 = request.form.get('team2_player1', '').strip()
    team2_player2 = request.form.get('team2_player2', '').strip()
    team2_player3 = request.form.get('team2_player3', '').strip()
    team2_player4 = request.form.get('team2_player4', '').strip()
    team2_player5 = request.form.get('team2_player5', '').strip()

    conn = sqlite3.connect(db_locale)
    c = conn.cursor()
    c.execute("""
        UPDATE Matches
        SET map_name = ?, game_rank = ?, winner_team = ?,
            team1_player1 = ?, team1_player2 = ?, team1_player3 = ?, team1_player4 = ?, team1_player5 = ?,
            team2_player1 = ?, team2_player2 = ?, team2_player3 = ?, team2_player4 = ?, team2_player5 = ?
        WHERE id = ?
    """, (map_name, game_rank, winner_team,
          team1_player1, team1_player2, team1_player3, team1_player4, team1_player5,
          team2_player1, team2_player2, team2_player3, team2_player4, team2_player5,
          match_id))
    conn.commit()
    conn.close()

    return redirect(url_for('search_player'))

@app.route('/delete_player/<player_id>', methods=['POST'])
def delete_player(player_id):
    conn = sqlite3.connect(db_locale)
    c = conn.cursor()
    c.execute("DELETE FROM player_details WHERE player_id = ?", (player_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('search_player'))

@app.route('/add_player', methods=['POST'])
def add_player():
    player_id = request.form.get('player_id', '').strip()
    most_played_hero = request.form.get('most_played_hero', '').strip()
    average_KDA = request.form.get('average_KDA', '')
    win_rate = request.form.get('win_rate', '')
    rank = request.form.get('rank', '')

    conn = sqlite3.connect(db_locale)
    c = conn.cursor()
    c.execute("""
        INSERT INTO player_details (player_id, most_played_hero, average_KDA, win_rate, rank)
        VALUES (?, ?, ?, ?, ?)
    """, (player_id, most_played_hero, average_KDA, win_rate, rank))
    conn.commit()
    conn.close()

    return redirect(url_for('search_player'))

@app.route('/update_player/<player_id>', methods=['POST'])
def update_player(player_id):
    most_played_hero = request.form.get('most_played_hero', '').strip()
    average_KDA = request.form.get('average_KDA', '')
    win_rate = request.form.get('win_rate', '')
    rank = request.form.get('rank', '')

    conn = sqlite3.connect(db_locale)
    c = conn.cursor()
    c.execute("""
        UPDATE player_details
        SET most_played_hero = ?, average_KDA = ?, win_rate = ?, rank = ?
        WHERE player_id = ?
    """, (most_played_hero, average_KDA, win_rate, rank, player_id))
    conn.commit()
    conn.close()

    return redirect(url_for('search_player'))

def query_player_match_stats(player_id, match_id):
    conn = sqlite3.connect(db_locale)
    c = conn.cursor()
    c.execute("""
        SELECT *
        FROM player_match_details
        WHERE player_id = ? AND match_id = ?
    """, (player_id, match_id))
    data = c.fetchall()
    conn.close()
    return data

def query_player_details(user_id=None, hero_class=None, rank=None, map_name=None):
    conn = sqlite3.connect(db_locale)
    c = conn.cursor()

    base_query = "SELECT * FROM player_details"
    conditions = []
    params = []

    if user_id:
        if re.match(r'.+#\d{4}$', user_id):
            conditions.append("player_id = ?")
            params.append(user_id)
        else:
            conditions.append("player_id LIKE ?")
            params.append(user_id + "#____")
    print(hero_class)
    if hero_class and hero_class != "":
        conditions.append("most_played_hero IN (SELECT name FROM heroes WHERE class = ?)")
        params.append(hero_class)

    if rank and rank != "":
        conditions.append("rank = ?")
        params.append(rank)

    if map_name and map_name != "":
        base_query = """
            SELECT pd.*
            FROM player_details pd
            JOIN player_match_details pmd ON pd.player_id = pmd.player_id
            JOIN Matches m ON m.id = pmd.match_id
        """
        conditions.append("m.map_name = ?")
        params.append(map_name)

    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)

    print(base_query, params)
    c.execute(base_query, params)
    player_info = c.fetchall()
    conn.close()
    return player_info

def query_all_players():
    conn = sqlite3.connect(db_locale)
    c = conn.cursor()
    c.execute("SELECT player_id FROM player_details")
    players = [row[0] for row in c.fetchall()]
    conn.close()
    return players


def query_matches(user_id=None, map_name=None, selected_rank=None):
    conn = sqlite3.connect(db_locale)
    c = conn.cursor()

    base_query = "SELECT * FROM Matches"
    conditions = []
    params = []

    if user_id:
        condition_parts = []
        for col in ["team1_player1","team1_player2","team1_player3","team1_player4","team1_player5",
                    "team2_player1","team2_player2","team2_player3","team2_player4","team2_player5"]:
            condition_parts.append(f"{col} = ?")
        conditions.append("(" + " OR ".join(condition_parts) + ")")
        params.extend([user_id]*10)

    if map_name and map_name != "":
        conditions.append("map_name = ?")
        params.append(map_name)
    
    if selected_rank and selected_rank != "":
        conditions.append("game_rank = ?")
        params.append(selected_rank)

    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)

    c.execute(base_query, params)
    matches_info = c.fetchall()
    conn.close()
    return matches_info

if __name__ == '__main__':
    app.run(debug=True)
