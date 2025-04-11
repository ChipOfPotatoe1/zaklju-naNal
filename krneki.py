import requests

API_kljuc_igre = "7482e2d4fb924a119eedc34862b5ce39"
URL_igre = "https://api.rawg.io/api"

#iskanje iger
def iskanje_iger(ime_igre):
    url = f"{URL_igre}/games?key={API_kljuc_igre}&search={ime_igre}" #link z formatiranimi podatki
    podatki = requests.get(url) #pridobivanje podatkov
    vrnjeno = podatki.json() #spreminjanje za lepsi pogled
    return vrnjeno #vračanje json datoteke

#pridobivanje podatkov
ime_igre = input("vnesi ime: ")
podatki = iskanje_iger(ime_igre)

#podatki
ime = podatki['results'][0]['name']
datum = podatki['results'][0]['released']
ocena = podatki['results'][0]['rating']
slika = podatki['results'][0]['background_image']

print(podatki['results'][0]['background_image'])