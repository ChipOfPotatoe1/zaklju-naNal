import requests
from flask import Flask, render_template, request, redirect, url_for, session
from tinydb import TinyDB, Query

#pip install requests
#pip install flask
#pip insatll tinydb

API_kljuc_igre = "7482e2d4fb924a119eedc34862b5ce39"
URL_igre = "https://api.rawg.io/api"

app = Flask(__name__)
app.secret_key = '123'

#podatkovna baza: tinydb
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

@app.route('/login', methods=['POST', 'GET']) #login
def login():
    if request.method == 'POST':
        #dobi vnešene podatke
        username = request.form.get('username')
        password = request.form.get('password')

        uporabnik =db.get(User.username == username)

        if uporabnik: #ta vrstica prever ce uporabnik sploh obstaja
            if uporabnik['password'] == password: #tuki se prever ce je geslo pravilno, ce je pravilno userja da v session in preuredi na index
                session['username'] = username
                return redirect(url_for('index'))
    return render_template('login.html') #ce se to pojavi, je neki narobe

@app.route('/logout') #logout
def logout():
    session.pop('username') #userjva da vn iz sessiona pa te vrne nazaj na login
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST']) #registracija
def register():
    if request.method == 'POST':
        username = request.form.get('username', "NONO")
        password = request.form.get('password', "NONOPASS")
        print(username, password)
        db.insert({'username': username, 'password': password})
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/', methods=['GET'])
def index():
    #preveri če je uporabnik prijavljen notri, če ni ga vrže na login
    if 'username' not in session:
        return redirect(url_for('login'))
    
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
    
    else: # če ni vnešeno (else) se prikaže samo vrstica za iskanje, če tega if stavka ni se prikažejo privzete vrednosti"""
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
