from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
db_locale = 'player.db'

@app.route('/')
@app.route('/home')
def home_page():
    player_data = query_player_details()
    return render_template('home.html', player_data = player_data)


def query_player_details():
    conn = sqlite3.connect(db_locale)
    c = conn.cursor()
    c.execute("""
        SELECT * FROM player_details
    """)
    player_info = c.fetchall()
    return player_info

if __name__ == '__main__':
    app.run()
