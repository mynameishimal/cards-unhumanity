from flask import Flask, render_template, request, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate("cards-unhumanity-firebase-adminsdk-4muf7-b19030a37f.json")
firebase_admin.initialize_app(cred)

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
        username = request.form['email']  # Make sure the form field is 'email', not 'username'
        password = request.form['password']

        try:
            # Create user in Firebase Authentication
            user = auth.create_user(email=username, password=password)

            # Registration successful
            # Optionally perform further actions or redirects

            # You can set session here if needed
            session['username'] = username

            # Redirect to a dashboard or success page
            return redirect(url_for('dashboard'))

        except Exception as e:
            # Handle registration errors
            print("Registration failed:", str(e))
            return render_template('registration_error.html')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            user = auth.get_user_by_email(username)
            # Sign in the user using Firebase Authentication
            logged_in_user = auth.sign_in_with_email_and_password(username, password)
            session['username'] = username
            return redirect(url_for('dashboard'))
        except auth.AuthError as e:
            # Handle authentication error
            print(f"Authentication failed: {str(e)}")
            return redirect(url_for('login'))

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
