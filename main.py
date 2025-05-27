import requests, random
from flask import Flask, render_template, request, redirect, url_for, session
from tinydb import TinyDB, Query

#pip install requests
#pip install flask
#pip insatll tinydb

API_kljuc_igre = "7482e2d4fb924a119eedc34862b5ce39"
URL_igre = "https://api.rawg.io/api"
URL_serije = 'https://api.tvmaze.com/search/shows?'
#https://api.tvmaze.com/search/shows?q=supernatural

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

#iskanje serije
def iskanje_serije(ime_serije):
    url = f"{URL_serije}q={ime_serije}"
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
                return redirect(url_for('izbira'))
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
        #print(ime, datum, ocena, slika, ID)
        return render_template('index.html', ime = ime, datum = datum, ocena = ocena, slika = slika, opis = opis)
    
    else: # če ni vnešeno (else) se prikaže samo vrstica za iskanje, če tega if stavka ni se prikažejo privzete vrednosti"""
        return render_template('index.html')

@app.route('/izbira')
def izbira(): #tuki ns preusmer da izberemo stvar k jo hocemo iskat
    return render_template('izbira.html')

@app.route('/serije', methods=['GET']) #route za iskanje serij, na isto foro k za igre
def serije():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    ime_serije = request.args.get('ime')
    podatki = iskanje_serije(ime_serije)

    if ime_serije:
        #print(podatki)
        ime = podatki[0]['show']['name']
        jezik = podatki[0]['show']['language']
        slika = podatki[0]['show']['image']['medium']
        ocena = podatki[0]['show']['rating']['average']
        opis = podatki[0]['show']['summary']
        datum = podatki[0]['show']['premiered']
        #print(opis)
        return render_template('serije.html', ime = ime, jezik = jezik, slika = slika, ocena = ocena, opis = opis, datum = datum)
    else:
        return render_template('serije.html')

#kviz o igrah, da stran ne bo tako dougočasna
@app.route('/kviz', methods=['GET', 'POST'])
def kviz():
    rezultat = ''
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Dobimo odgovore uporabnika
        odgovor1 = request.form['ime1'].strip().lower()
        odgovor2 = request.form['ime2'].strip().lower()
        odgovor3 = request.form['ime3'].strip().lower()

        # Dobimo pravilne odgovore
        pravilno1 = request.form['pravilno1'].strip().lower()
        pravilno2 = request.form['pravilno2'].strip().lower()
        pravilno3 = request.form['pravilno3'].strip().lower()

        # Preveri pravilne odgovore
        i = 0
        if odgovor1 == pravilno1:
            i += 1
        if odgovor2 == pravilno2:
            i += 1
        if odgovor3 == pravilno3:
            i += 1

        # z cifro nastavmo rezultat za izpis
        if i == 0:
            rezultat = "Noben odgovor ni pravilen."
        elif i == 1:
            rezultat = "Pravilen je en odgovor."
        elif i == 2:
            rezultat = "Pravilna sta dva odgovora."
        elif i == 3:
            rezultat = "Vsi odgovori so pravilni!"

        # spet pošlje slike in imena iz POST
        slika1 = request.form['slika1']
        slika2 = request.form['slika2']
        slika3 = request.form['slika3']
        ime1 = request.form['pravilno1']
        ime2 = request.form['pravilno2']
        ime3 = request.form['pravilno3']

    else:
        st = random.randint(1, 30)
        url = f"{URL_igre}/games?key={API_kljuc_igre}&page={st}&page_size=30"
        podatki = requests.get(url)
        igre = podatki.json()['results']
        igra1 = random.choice(igre)
        igra2 = random.choice(igre)
        igra3 = random.choice(igre)

        slika1 = igra1["background_image"]
        ime1 = igra1["name"]
        slika2 = igra2["background_image"]
        ime2 = igra2["name"]
        slika3 = igra3["background_image"]
        ime3 = igra3["name"]

    return render_template('kviz.html', slika1=slika1, slika2=slika2, slika3=slika3, ime1=ime1, ime2=ime2, ime3=ime3, rezultat=rezultat, pravilno1=ime1, pravilno2=ime2, pravilno3=ime3)
if __name__ == "__main__":
    app.run(debug=True)
