from flask import Flask, jsonify, request, render_template
from database import cards_collection

app = Flask(__name__)

# In-memory 'database' structures
users = {}  # This will store user data
games = {}  # This will store game data


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Check if password matches confirm password
        if password != confirm_password:
            return 'Passwords do not match!'

        # Implement logic to store user details in your database
        # For example:
        # Store user details in a dictionary (this is just for demonstration)
        user = {
            'username': username,
            'password': password  # In a real application, hash the password before storing it
            # Add other user details if needed
        }
        # Store user data in your database or user management system

        return f"Registration successful for user {username}!"

    return render_template('register.html')


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
    cards = cards_collection.find()  # Retrieve cards from MongoDB
    return render_template('cards.html', cards=cards)


if __name__ == '__main__':
    app.run(debug=True)
