from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
from tinydb import TinyDB, Query

app = Flask(__name__)
app.secret_key = '123'  # Za uporabo seje

# API ključ in link do API-ja
API_KEY = "7482e2d4fb924a119eedc34862b5ce39"
BASE_URL = "https://api.rawg.io/api"
URL_FILMI = "https://api.tvmaze.com"

# TinyDB za uporabnike
db = TinyDB('users.json')
User = Query()

# Iskanje iger
def search_game(game_name):
    url = f"{BASE_URL}/games?key={API_KEY}&search={game_name}"
    response = requests.get(url)
    data = response.json()
    return data.get("results", [])

# Iskanje opisa iger
def search_description(game_id):
    url = f"{BASE_URL}/games/{game_id}?key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        opis = data.get('description_raw', 'Opis ni na voljo.')
        return opis
    return 'Napaka pri pridobivanju opisa igre'

# Iskanje serij
def search_show(show_name):
    url = f"{URL_FILMI}/search/shows?q={show_name}"
    response = requests.get(url)
    data = response.json()
    return [item["show"] for item in data] if data else []

@app.route("/", methods=['GET'])
def home():
    if 'username' in session:
        return redirect(url_for('izbira')) 
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if db.search(User.username == username):
            flash('Uporabniško ime je že zasedeno!')
            return redirect(url_for('register'))

        db.insert({'username': username, 'password': password})
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

       
        user = db.search((User.username == username) & (User.password == password))
        if user:
            session['username'] = username
            return redirect(url_for('izbira'))
        else:
            flash('Nepravilen uporabnik ali geslo!')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route("/izbira", methods=["GET", "POST"])
def izbira():
    if 'username' not in session:
        return redirect(url_for('home'))
    return render_template("index.html", username=session.get('username'))

@app.route("/index", methods=["GET", "POST"])
def index():
    informacije = None
    opis = None
    if request.method == "POST":
        game_name = request.form["game_name"]
        informacije = search_game(game_name)
        
        if informacije:
            game_id = informacije[0]["id"]
            opis = search_description(game_id)

    return render_template("index.html", informacije=informacije, opis=opis)

if __name__ == "__main__":
    app.run(debug=True)
