import requests
from flask import Flask, render_template, request, redirect, url_for
from tinydb import TinyDB, Query

API_kljuc_igre = "7482e2d4fb924a119eedc34862b5ce39"
URL_igre = "https://api.rawg.io/api"

app = Flask(__name__)

#podatkovna baza
db = TinyDB('users.json')
User = Query()

#iskanje iger
def iskanje_iger(ime_igre):
    url = f"{URL_igre}/games?key={API_kljuc_igre}&search={ime_igre}" #link z formatiranimi podatki
    podatki = requests.get(url) #pridobivanje podatkov
    vrnjeno = podatki.json() #spreminjanje v json datoteko
    return vrnjeno #vračanje json datoteke

#iskanje opisa igre
def iskanje_opisa(ID):
    url = f"{URL_igre}/games/{ID}?key={API_kljuc_igre}"
    podatki = requests.get(url)
    vrnjeno = podatki.json()
    return vrnjeno

@app.route('/', methods=['GET'])
def redirect():
    return render_template('login.html')

@app.route('/register', methods=['GET']) #registracija
def register():
    username = request.args.get['username']
    geslo = request.args.get['password']
    return render_template('register.html')

@app.route('/index', methods=['GET'])
def index():
    #pridobivanje podatkov
    ime_igre = request.args.get('ime')
    podatki = iskanje_iger(ime_igre)
    
    if ime_igre: #če je vnešeno ime igre se prikažejo podatki
        #podatki
        ime = podatki['results'][0]['name']
        datum = podatki['results'][0]['released']
        ocena = podatki['results'][0]['rating']
        slika = podatki['results'][0]['background_image']
        ID = podatki['results'][0]['id']

        #podatki o opisu igre
        podatkiOpis = iskanje_opisa(ID)
        opis = podatkiOpis['description']
        print(ime, datum, ocena, slika, ID)
        return render_template('index.html', ime = ime, datum = datum, ocena = ocena, slika = slika, opis = opis)
    
    else: # če ni vnešeno (else) se prikaže samo vrstica za iskanje, če tega if stavka ni se prikažejo privzete vrednosti
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
