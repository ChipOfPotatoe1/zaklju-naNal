from flask import Flask, render_template, request
import requests
#git config --global user.name "Mona Lisa"
#https://api.rawg.io/api/games?key=7482e2d4fb924a119eedc34862b5ce39&search=world of warcraft
#iskalnik serij, filmov - Tvmaze API

app = Flask(__name__)
#lalala
#API ključ in link do apija
API_KEY = "7482e2d4fb924a119eedc34862b5ce39"
BASE_URL = "https://api.rawg.io/api"
URL_FILMI = "https://api.tvmaze.com"

#iskanje iger
def search_game(game_name):
    url = f"{BASE_URL}/games?key={API_KEY}&search={game_name}"
    response = requests.get(url)
    data = response.json()
    return data["results"]

#iskanje opisa iger
def search_description(game_id):
    url = f"{BASE_URL}/games/{game_id}?key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        opis = data.get('description_raw', 'Opis ni na voljo.')
        return opis
    else:
        return 'napaka pri pridobivanju opisa igre'
    
#iskanje serij
def search_show(show_name):
    url = f"{URL_FILMI}/search/shows?q={show_name}"
    response = requests.get(url)
    data = response.json()
    return [item["show"] for item in data] if data else []

@app.route("/", methods=["GET", "POST"])
def index():
    informacije = None
    opis = None
    informacije_serija = None
    
    if request.method == "POST":
        search_type = request.form.get("search_type")
        search_query = request.form.get("search_query")
        
        informacije = search_game(search_query)
        if search_type == "game":
            
            if informacije:
                game_id = informacije[0]["id"]
                opis = search_description(game_id)
        #game_name = request.form["game_name"]
        elif search_type == "show":
            informacije_serija = search_show(search_query)
        
        #print(game_name)
        print(informacije)
        
    return render_template("index.html", informacije = informacije, opis = opis)

if __name__ == "__main__":
    app.run(debug=True)