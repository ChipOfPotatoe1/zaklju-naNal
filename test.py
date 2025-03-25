from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# API ključ in povezava
API_KEY = "7482e2d4fb924a119eedc34862b5ce39"
BASE_URL = "https://api.rawg.io/api"

def search_game(game_name):
    """Iskanje igre v RAWG API."""
    url = f"{BASE_URL}/games?key={API_KEY}&search={game_name}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data.get("results", [])  # Vrni seznam rezultatov ali prazen seznam
    return []

def search_description(game_id):
    """Iskanje opisa igre glede na ID."""
    url = f"{BASE_URL}/games/{game_id}?key={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('description_raw', 'Opis ni na voljo.')
    return 'Napaka pri pridobivanju opisa igre.'

@app.route("/", methods=["GET", "POST"])
def index():
    informacije = []
    opis = None

    if request.method == "POST":
        game_name = request.form["game_name"]
        informacije = search_game(game_name)

        print("Pridobljene informacije:", informacije)  # DEBUG OUTPUT

        if informacije:  # Preveri, če API vrne vsaj eno igro
            game_id = informacije[0]["id"]
            opis = search_description(game_id)
            print("Opis igre:", opis)  # DEBUG OUTPUT

    return render_template("test.html", informacije=informacije, opis=opis)

if __name__ == "__main__":
    app.run(debug=True)
