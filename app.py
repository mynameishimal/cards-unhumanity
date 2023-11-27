from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from database import cards_collection


app = Flask(__name__)
CORS(app)

# In-memory 'database' structures
users = {}  # This will store user data
games = {}  # This will store game data


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    # In a real app, you'd want to hash the password - NEVER store them as plaintext
    username = request.json['username']
    password = request.json['password']  # Please use something like bcrypt in a real app

    if username in users:
        return jsonify({'error': 'Username already exists'}), 409

    # Store the new user
    users[username] = {
        'username': username,
        'password': password,  # Again, store hashed passwords, not plaintext
        'games_played': 0,
        'funny_points': 0
    }

    return jsonify(users[username]), 201


@app.route('/game//play', methods=['POST'])
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
    cards = cards_collection.find()  # Retrieve cards from MongoDB
    return render_template('cards.html', cards=cards)


if __name__ == '__main__':
    app.run(debug=True)
