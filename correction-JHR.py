### MES COMMENTAIRES ET CORRECTIONS SONT MARQUÉS PAR TROIS DIÈSES

### Ton script fonctionne, super!
### Par contre, il n'était pas nécessaire de le diviser en deux parties
### D'autant plus que du réunis, en quelque sorte, deux scripts en un seul.
### Ici, il fallait faire 2 scripts: le premier qui produit le fichier txt; le second qui produit le CSV
### Ou bien tu pouvais conserver un seul script et tout faire d'un coup comme je te le propose ci-dessous:

# Mon script se divise en plusieurs parties.
# Premièrement, déterminer les url qui fonctionnent puisqu'elles changent selon le numéro associé à la réserve consultée.

# coding: utf-8

import csv
import re ### J'ajoute ce module que tu déclarais à la ligne 42
import requests
from bs4 import BeautifulSoup

reserves = list (range(0,1000))

entetes = {
	"User-Agent":"Jean-Philippe Guilbault - Requête envoyée dans le cadre d'un cours de journalisme informatique à l'UQAM (EDM5240)",
	"From":"jp.guilbault@protonmail.com"
}

### À mon sens, l'étape ci-dessous n'était pas nécessaire
# fonctionne = "url-aandc.txt"
# url = open(fonctionne,"w")

fichier = "populations-autochtones-JHR.csv" ### Je remonte plus haut cette déclaration de la variable «fichier» et lui ajoute «-JHR»

for reserve in reserves:
    ### Pourquoi la version anglaise des pages?
    ### Je vais essayer la version française
    # url1 = "http://fnp-ppn.aandc-aadnc.gc.ca/fnp/Main/Search/FNMain.aspx?BAND_NUMBER={}&lang=eng".format(reserve)
    url1 = "http://fnp-ppn.aandc-aadnc.gc.ca/fnp/Main/Search/FNMain.aspx?BAND_NUMBER={}&lang=fra".format(reserve)
    reponses = requests.get(url1, headers=entetes)
    if reponses.status_code == 200:

        ### Donc, pas nécessaire de créer un fichier txt, ici.
        ### On peut directement moissonner l'URL qui t'intéresse
        # url.write(url1)
        # url.write("\n")

# Deuxièmement utiliser les bonnes url à partir du fichier .txt pour faire mon moissonnage.

# coding: utf-8

# import csv
# import re
# import requests
# from bs4 import BeautifulSoup

# entetes = {
#     "User-Agent":"Jean-Philippe Guilbault - Requête pour un cours",
#     "From":"jp.guilbault@protonmail.com"
# }

# fich = "url-aandc.txt"
# f = open(fich)

# lignes = f.readlines()

# url2 = []

# for ligne in lignes:
#     numeros = re.findall('\d+', ligne)
#     numero = numeros[0]
#     url2.append("http://fnp-ppn.aandc-aadnc.gc.ca/fnp/Main/Search/FNRegPopulation.aspx?BAND_NUMBER={}&lang=fra".format(numero))

### Tout de suite, on créé l'URL où se trouvent les données de population qui t'intéressent avec la variable «réserve» créé plus tôt

        url2 = "http://fnp-ppn.aandc-aadnc.gc.ca/fnp/Main/Search/FNRegPopulation.aspx?BAND_NUMBER={}&lang=fra".format(reserve)

# for url in url2:
        stats = []

        demandes = requests.get(url2,headers=entetes) ### Je corrige ici «url» par »«url2»
        pages = BeautifulSoup(demandes.text,"html.parser")
        stats.append(pages.find("span", id="plcMain_txtBandName").text)
        print("On moissonne {}".format(pages.find("span", id="plcMain_txtBandName").text)) ### J'ajoute ce «print» pour suivre l'exécution du script

        ### Je crois qu'il peut être utile d'ajouter deux infos à ton fichier
        ### Le numéro identifié plus haut, pour référence future:
        stats.append(reserve)

        ### La province ou le territoire où se trouve la réserve, afin d'effectuer certains regroupements
        urlpop = "http://fnp-ppn.aandc-aadnc.gc.ca/fnp/Main/Search/FNPopulation.aspx?BAND_NUMBER={}&lang=fra".format(reserve)
        contenupop = requests.get(urlpop,headers=entetes)
        if contenupop.status_code == 200:
            pagepop = BeautifulSoup(contenupop.text,"html.parser")
            stats.append(pagepop.find("span", id="plcMain_txtProvince2").text.capitalize())
        else:
            stats.append("")
            
        for item in pages.find("div", class_="table-responsive").find_all("tr")[1:]:
            ### Comme tu moissonnes des nombres, il serait utile de les transformer en nombres
            ### D'abord, je place ce que tu extrais dans une variable que je vais appeler «nombre»
            nombre = item.find_all("span")[1].text
            ### Ensuite, j'en retire les espaces insécables, s'il y a lieu
            nombre = nombre.replace("\xa0","")
            ### Enfin, je le transforme en nombre et l'ajoute à la liste «stats»
            nombre = int(nombre)
            stats.append(nombre)
    
        ecrire = open(fichier,"a")
        pouet = csv.writer(ecrire)
        pouet.writerow(stats)
