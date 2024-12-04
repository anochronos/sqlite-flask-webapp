from flask import Flask, render_template, redirect, request
import sqlite3

app = Flask(__name__)
db_locale = 'player.db'

@app.route('/')
@app.route('/home', methods=['POST', 'GET'])
def home_page():
    return render_template('home.html')

@app.route('/all_players', methods=['POST', 'GET'])
def all_players():
    player_data = query_player_details()
    return render_template('all_players.html', player_data = player_data)

@app.route('/search_results', methods=['POST', 'GET'])
def search_player():
    user_id = request.form.get('user_id')
    print(user_id)
    player_data = query_player_details(user_id)
    return render_template('search_results.html', error=None, player_data=player_data)

def query_player_details(user_id=None):
    conn = sqlite3.connect(db_locale)
    c = conn.cursor()
    c.execute("""
        SELECT * FROM player_details
    """)
    player_info = c.fetchall()
    #print(user_id)
    if user_id:
        c.execute("""
            SELECT * FROM player_details WHERE id = ?
        """, (user_id,))
        player_info = c.fetchall()
    conn.close()
    return player_info

if __name__ == '__main__':
    app.run()
