from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
from tinydb import TinyDB, Query

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Za uporabo seje

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

# Funkcija za preverjanje prijave
def check_login():
    if 'username' not in session:
        return False
    return True

# Domača stran - izbira prijave ali registracije
@app.route("/", methods=['GET'])
def home():
    if check_login():  # Preveri, če je uporabnik prijavljen
        return redirect(url_for('izbira'))  # Če je uporabnik prijavljen, ga preusmeri na izbiro
    return render_template('home.html')  # Če ni prijavljen, prikaži domačo stran

# Registracija
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Preveri, ali uporabnik že obstaja
        if db.search(User.username == username):
            flash('Uporabniško ime je že zasedeno!')
            return redirect(url_for('register'))

        # Shrani novega uporabnika
        db.insert({'username': username, 'password': password})
        return redirect(url_for('login'))

    return render_template('register.html')

# Prijava
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Preveri uporabnika v bazi
        user = db.search((User.username == username) & (User.password == password))
        if user:
            session['username'] = username
            return redirect(url_for('izbira'))  # Preusmeri na izbira.html
        else:
            flash('Nepravilen uporabnik ali geslo!')
            return redirect(url_for('login'))

    return render_template('login.html')

# Odjava
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))  # Po odjavi se vrni na domačo stran

# Izbira stran po prijavi
@app.route("/izbira", methods=["GET", "POST"])
def izbira():
    if not check_login():  # Preveri, če je uporabnik prijavljen
        return redirect(url_for('login'))  # Preusmeri na prijavo, če ni prijavljen
    return render_template("izbira.html", username=session.get('username'))  # Prikaz izbire, če je prijavljen

if __name__ == "__main__":
    app.run(debug=True)
