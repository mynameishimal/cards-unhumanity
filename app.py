import hashlib
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os

from transformers import AutoModelForSequenceClassification

from cards_manager import CardManager
from cards_manager import sample_card_list
from prompts_manager import PromptManager
from prompts_manager import prompts
from humor_algo import calculate_emotion_score
import random

app = Flask(__name__)

app.secret_key = os.urandom(24)


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
    return prompts


"""NOTE TO SELF TO RESET DATA AT THE BEGINNING OF EVERY SESSION!!!"""


@app.route('/question')
def display_question():
    prompt_num = session.get('prompt_num', 1)  # Retrieve prompt_num from the session or default to 0
    prompt_list = random.sample(prompts, 10)
    if 0 <= prompt_num < len(prompt_list):
        prompt = prompt_list[prompt_num]
        next_prompt_num = prompt_num + 1  # Increment prompt_num for the next question
    else:
        print("DONE")
        my_game_data = session.get("game_data")
        results = end_game(my_game_data)
        stats = results[0]
        total = results[1]
        return render_template('game_data.html', game_data=stats, total_score=total)

    # Gets cards
    # This is a sample and should be replaced with something legit!
    cards = sample_card_list
    # card_manager = CardManager(cards)
    # drawn_cards = card_manager.get_cards(num_cards=6)
    # print(drawn_cards)
    drawn_cards = random.sample(cards, 6)
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

    total_score = 0
    for prompt, user_answer, score in zip(prompts, user_answers, humor_scores):
        total_score += score

    update_user_stats(session['username'], total_score)

    # Clear game_data after calculating scores
    game_data.clear()

    temp = [game_data_with_scores, total_score]

    return [game_data_with_scores, total_score]
    # return game_data_with_scores


@app.route('/instructions')
def instructions():
    return render_template('instructions.html')


def update_user_stats(username, total_score):
    conn = sqlite3.connect('user_stats.db')
    cursor = conn.cursor()

    # Fetch the user's current stats
    cursor.execute("SELECT * FROM user_stats WHERE username=?", (username,))
    user_stats = cursor.fetchone()

    if user_stats:
        # Update games played
        games_played = int(user_stats[2]) + 1  # Assuming 'games_played' is at index 2

        # Calculate new average score
        if user_stats[4]:  # Check if 'past_scores' exists
            past_scores = user_stats[4].split(',')  # Assuming 'past_scores' is at index 4
        else:
            past_scores = []
        past_scores.append(str(total_score))
        average_score = sum(map(int, past_scores)) / len(past_scores)

        # Update the 'user_stats' table
        cursor.execute("UPDATE user_stats SET games_played=?, average_score=?, past_scores=?, total_score=? WHERE "
                       "username=?",
                       (games_played, average_score, ','.join(past_scores), int(user_stats[5]) + total_score, username))
    else:
        # User doesn't exist, create a new record
        cursor.execute(
            "INSERT INTO user_stats (username, games_played, average_score, past_scores, total_score) VALUES (?, ?, ?, ?, ?)",
            (username, 1, total_score, str(total_score), total_score))

    print("updated!!!")
    conn.commit()
    conn.close()


# Function to fetch user statistics from the database
def fetch_user_stats(username):
    conn = sqlite3.connect('user_stats.db')
    cursor = conn.cursor()

    # Assuming you have a table named 'user_stats' with columns 'username', 'games_played', 'average_score', etc.
    cursor.execute("SELECT * FROM user_stats WHERE username = ?", (username,))
    user_stats = cursor.fetchone()
    conn.close()

    return user_stats


# Route for displaying the user profile page
@app.route('/profile')
def profile():
    # Get the username from the session or any other source
    username = 'example_user'

    # Fetch user statistics from the database
    user_stats = fetch_user_stats(session['username'])

    if user_stats:
        games_played = user_stats[2]  # Assuming 'games_played' is at index 2
        average_score = user_stats[3]  # Assuming 'average_score' is at index 3
        total_score = user_stats[5]  # Assuming 'total_score' is at index 5
        past_scores_str = user_stats[4]  # Assuming 'past_scores' is at index 4
        past_scores = list(map(int, past_scores_str.split(',')))
    else:
        # Initialize statistics for new users
        games_played = 0
        average_score = 0
        total_score = 0
        past_scores = []

    # Pass fetched user statistics to the profile_page.html template
    return render_template('profile_page.html', username=session['username'], games_played=games_played,
                           average_score=average_score, total_score=total_score, past_scores=past_scores)


@app.route('/about')
def about():
    return render_template('aboutUs.html')


if __name__ == '__main__':
    app.run(debug=True)
