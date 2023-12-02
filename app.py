import hashlib
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

from database import init_db

# In-memory 'database' structures
users = {}  # This will store user data
games = {}  # This will store game data

init_db()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cards')
def cards():
    return render_template('cards.html')


# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_password(password)

        conn = sqlite3.connect('user_database.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password))

        conn.commit()
        conn.close()

        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_password(password)

        conn = sqlite3.connect('user_database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", (username, hashed_password))
        user = cursor.fetchone()

        conn.close()

        if user:
            # User authenticated, perform login actions
            return "Login successful"
        else:
            return "Invalid credentials"

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in before rendering the dashboard
    if 'username' in session:
        username = session['username']
        # Fetch user data or perform necessary operations for the dashboard
        return render_template('dashboard.html', username=username)
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    # Clear the session and log the user out
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/game/<game_id>/play', methods=['POST'])
def play_card(game_id):
    data = request.json
    player = data['player']
    card = data['card']

    # Simulate playing a card in a game
    if game_id not in games:
        games[game_id] = {
            'players': [],
            'played_cards': []
        }
    game = games[game_id]

    # Add the card to the played cards for the game
    game['played_cards'].append({
        'player': player,
        'card': card
    })

    # Update the user's funny points
    users[player]['funny_points'] += 1  # You'll have more complex logic here

    return jsonify(game), 200


@app.route('/cards')
def get_cards():
    # cards = cards_collection.find()  # Retrieve cards from MongoDB
    return render_template('cards.html', cards=cards)


if __name__ == '__main__':
    app.run(debug=True)
