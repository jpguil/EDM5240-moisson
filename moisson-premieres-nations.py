# Mon script se divise en plusieurs parties.
# Premièrement, déterminer les url qui fonctionnent puisqu'elles changent selon le numéro associé à la réserve consultée.

# coding: utf-8

import csv
import requests
from bs4 import BeautifulSoup

#Toutes les possibilités de numéros de réserve (je doute qu'il y en ait plus de 1000).
reserves = list (range(0,1000))

entetes = {
	"User-Agent":"Jean-Philippe Guilbault - Requête envoyée dans le cadre d'un cours de journalisme informatique à l'UQAM (EDM5240)",
	"From":"jp.guilbault@protonmail.com"
}

#Je teste toutes les combinaisons d'url possibles pour les pages «Main» des réserves autochtones pour déterminer celles qui fonctionnent.
fonctionne = "url-aandc.txt"
url = open(fonctionne,"w")

for reserve in reserves:
    url1 = "http://fnp-ppn.aandc-aadnc.gc.ca/fnp/Main/Search/FNMain.aspx?BAND_NUMBER={}&lang=eng".format(reserve)
    reponses = requests.get(url1, headers=entetes)
#Si elles fonctionnent, je les entrepose dans un fichier .txt à réutiliser pour plus tard.
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

url2 = []

#Je reprends mes urls qui fonctionnent pour en extraire le numéro de réserve (je dois faire cette étape car les pages /FNRegPopulation.aspx?BAND_NUMBER=... me renvoient une page fonctionnelle même si le numéro de réserve n'est associé à aucune réserve réelle.
for ligne in lignes:
    numeros = re.findall('\d+', ligne)
    numero = numeros[0]
    url2.append("http://fnp-ppn.aandc-aadnc.gc.ca/fnp/Main/Search/FNRegPopulation.aspx?BAND_NUMBER={}&lang=fra".format(numero))

#Dans ces nouvelles urls fonctionnelles je vais faire mon moissonnage de statistiques de population (merci pour le coup de pouce lors du dernier cours!)
for url in url2:
    stats = []
    demandes = requests.get(url,headers=entetes)
    pages = BeautifulSoup(demandes.text,"html.parser")
    stats.append(pages.find("span", id="plcMain_txtBandName").text)
    for item in pages.find("div", class_="table-responsive").find_all("tr")[1:]:
        stats.append(item.find_all("span")[1].text)

#Je transcris mes résultats dans un fichier .csv
    ecrire = open(fichier,"a")
    pouet = csv.writer(ecrire)
    pouet.writerow(stats)
