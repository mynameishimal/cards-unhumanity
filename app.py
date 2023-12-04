import hashlib
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os

from transformers import AutoModelForSequenceClassification

from cards_manager import CardManager
from humor_algo import calculate_emotion_score

app = Flask(__name__)

app.secret_key = os.urandom(24)

# In-memory 'database' structures
users = {}  # This will store user data
games = {}  # This will store game data


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

        print("Username:", username)
        print("Hashed Password:", hashed_password)

        conn = sqlite3.connect('new_user_database.db')
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.Error as e:
            print("SQLite error:", e)
            conn.rollback()  # Rollback any changes if there's an error
            conn.close()
            return "Error occurred while registering"

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_password(password)

        conn = sqlite3.connect('new_user_database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", (username, hashed_password))
        user = cursor.fetchone()

        conn.close()

        if user:
            # User authenticated, perform login actions
            session['username'] = username
            return render_template("dashboard.html", username=username)
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


@app.route('/cards')
def get_cards():
    # cards = cards_collection.find()  # Retrieve cards from MongoDB
    return render_template('cards.html', cards=cards)


# Needs Better implementation!! Dummy function for now
def get_prompts():
    return ["ur mom", "starbucks", "pasta", "youre losing me", "david malan on his birthday", "happy go lucky irky",
            "dorm decor", "lol"]


"""NOTE TO SELF TO RESET DATA AT THE BEGINNING OF EVERY SESSION!!!"""


@app.route('/question')
def display_question():
    prompt_num = session.get('prompt_num', 1)  # Retrieve prompt_num from the session or default to 0
    prompts = get_prompts()
    if 0 <= prompt_num < len(prompts):
        prompt = prompts[prompt_num]
        next_prompt_num = prompt_num + 1  # Increment prompt_num for the next question
    else:
        return render_template('game_data.html', game_data=session.get('game_data'))

    # Gets cards
    # This is a sample and should be replaced with something legit!
    cards = ["crystals", "cs50", "the duck", "mit", "dean khurana", "blank street coffee",
             "random bank of america info sessions", "racist tourists", "your roommates hair clogging the bathroom"]
    card_manager = CardManager(cards)
    drawn_cards = card_manager.get_cards(num_cards=6)
    print(drawn_cards)

    return render_template('question.html', prompt_num=prompt_num, prompt=prompt, next_prompt_num=next_prompt_num,
                           drawn_cards=drawn_cards)


@app.route('/collect_answers', methods=['POST'])
def collect_answers():
    prompt = request.form.get('prompt')  # Get the prompt from the form
    user_answer = request.form.get('selected_card')  # Get the user's answer from the form

    # Retrieve the existing game data from the session or initialize an empty list
    game_data = session.get('game_data', [])

    # Store the prompt and user answer in the game data list
    game_data.append({'prompt': prompt, 'user_answer': user_answer})

    # Update the game data in the session
    session['game_data'] = game_data

    # Increment the prompt number stored in the session by 1
    next_prompt_num = session.get('prompt_num', 1) + 1
    session['prompt_num'] = next_prompt_num

    # Redirect to the next question prompt route
    return redirect(url_for('display_question', prompt_num=next_prompt_num))


@app.route('/end_game')
def end_game(game_data):
    model = AutoModelForSequenceClassification.from_pretrained(
        "bdotloh/distilbert-base-uncased-go-emotion-empathetic-dialogues-context-v2")

    # Extract prompts and user answers for humor score calculation
    prompts = [data['prompt'] for data in game_data]
    user_answers = [data['user_answer'] for data in game_data]

    # Calculate humor scores for all prompt-answer pairs at the end of the game
    humor_scores = calculate_emotion_score(prompts, user_answers, model)

    # Combine game_data with humor_scores for further processing or storage
    game_data_with_scores = [{'prompt': prompt, 'user_answer': user_answer, 'emotion_score': score}
                             for prompt, user_answer, score in zip(prompts, user_answers, humor_scores)]

    print(game_data_with_scores)

    # Clear game_data after calculating scores
    game_data.clear()

    print(game_data_with_scores)

    return render_template('end_game.html', game_data_with_scores=game_data_with_scores)


@app.route('/instructions')
def instructions():
    return render_template('instructions.html')


@app.route('/about')
def about():
    return render_template('aboutUs.html')


if __name__ == '__main__':
    app.run(debug=True)
