#importi
from flask import Flask, render_template, request, redirect, url_for, flash, session #importi ki jih potrebujemo
import requests
from tinydb import TinyDB, Query #importas za podatkovno bazo

app = Flask(__name__) #ime aplikacije
app.secret_key = '123' #kljuc za admina

#linki do API-jev pa kljuci
API_kljuc_igre = "7482e2d4fb924a119eedc34862b5ce39"
URL_igre = "https://api.rawg.io/api"
URL_filmi = "https://api.tvmaze.com"

#podatkovna baza uporabniki
baza = TinyDB('uporabniki.json') #ustvars podatkovno bazo z imenom uporabniki
User = Query() #ustvars nov objekt za poizvedbe u bazi

#iskanje iger
def iskanje_iger(ime_igre):
    url = f"{URL_igre}/games?key={API_kljuc_igre}&search={ime_igre}" #link z formatiranimi podatki
    podatki = requests.get(url) #pridobivanje podatkov
    vrnjeno = podatki.json() #spreminjanje za lepsi pogled
    return vrnjeno #vračanje json datoteke


@app.route("/", methods=['POST', 'GET']) #ustvarjanje poti do glavne strani, nastavimo na POST in GET (po defaultu nastavljena na GET) za posiljanje in prejemanje/prikazovanje informacij
def index():
    informacije = None
    if request.method == 'POST':
        ime_igre = request.form.get('ime_igre')
        informacije = iskanje_iger(ime_igre)
        print(informacije)

    #return render_template("index.html", informacije=informacije)

if __name__ == "__main__":
    app.run(debug=True)