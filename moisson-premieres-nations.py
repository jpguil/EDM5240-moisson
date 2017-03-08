# Mon script se divise en plusieurs parties.
# Premièrement, déterminer les url qui fonctionnent puisqu'elles changent selon le numéro associé à la réserve consultée.

# coding: utf-8

import csv
import requests
from bs4 import BeautifulSoup

reserves = list (range(0,1000))

entetes = {
	"User-Agent":"Jean-Philippe Guilbault - Requête envoyée dans le cadre d'un cours de journalisme informatique à l'UQAM (EDM5240)",
	"From":"jp.guilbault@protonmail.com"
}

fonctionne = "url-aandc.txt"
url = open(fonctionne,"w")

for reserve in reserves:
    url1 = "http://fnp-ppn.aandc-aadnc.gc.ca/fnp/Main/Search/FNMain.aspx?BAND_NUMBER={}&lang=eng".format(reserve)
    reponses = requests.get(url1, headers=entetes)
    if reponses.status_code == 200:
        url.write(url1)
        url.write("\n")

# Deuxièmement utiliser les bonnes url à partir du fichier .txt pour faire mon moissonnage.

# coding: utf-8

import csv
import re
import requests
from bs4 import BeautifulSoup

fichier = "populations-autochtones.csv"
entetes = {
    "User-Agent":"Jean-Philippe Guilbault - Requête pour un cours",
    "From":"jp.guilbault@protonmail.com"
}

fich = "url-aandc.txt"
f = open(fich)

lignes = f.readlines()

for ligne in lignes:
    numeros = re.findall('\d+', ligne)
    numero = numeros[0]
    url2 = "http://fnp-ppn.aandc-aadnc.gc.ca/fnp/Main/Search/FNRegPopulation.aspx?BAND_NUMBER={}&lang=eng".format(numero)
    demandes = requests.get(url2,headers=entetes)
    # print(demandes)
    page = BeautifulSoup(demandes.text,"html.parser")
    
    reserves = page.find("span", id="plcMain_txtBandName").text
    for item in page.find("div", class_="table-responsive").find_all("tr")[1:]:
        categorie = item.find_all("span")[0]
        valeur = item.find_all("span")[1]
        total = (reserves, categorie.text, valeur.text)
