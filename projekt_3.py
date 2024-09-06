"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Pavla Koštuříková
email: kosturikovap@gmail.com
discord: Pavla K
"""

import sys
import requests
from bs4 import BeautifulSoup
import csv


# spuštění projektu pro územní celek Třebíč:
# python projekt_3.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=10&xnumnuts=6104" "vysledky_trebic.csv"

# fce 'arguments' pro získání vstupu do uživatele: název webové stánky 'url' a název výstupu 'csv'
def arguments():
    print(sys.argv)
    if len(sys.argv) == 3:
        url = sys.argv[1]
        vystup = sys.argv[2]
        try:
            requests.get(url)
            if url[0:34] == "https://volby.cz/pls/ps2017nss/ps3" and vystup[-4:] == ".csv" and len(vystup) > 4:
                print(f"STAHUJI DATA Z VYBRANÉHO URL: {url}")
                return url, vystup
        except:
            print("ŠPATNÝ VSTUP. NAPIŠ ZNOVU:")
            print('python projekt_3.py <odkaz-uzemniho-celku> <vysledny-soubor.csv>')
            exit()        
    else:
        print("ŠPATNÝ VSTUP. NAPIŠ ZNOVU:")
        print('python projekt_3.py <odkaz-uzemniho-celku> <vysledny-soubor.csv>')
        exit()

# fce 'link' pro najití všech webových odkazů na jednotlivé obce a uložení do listu 'link'
def link(soup: BeautifulSoup):
    link = []
    for one_link in soup.find_all("a"):
        if one_link.string != "X" and "vyber" in one_link["href"] or "okrsek" in one_link["href"]:
            link.append(one_link["href"])
    return link

# fce 'code' pro najití všech číselných kódů obcí a uložení do listu 'code'
def code(soup: BeautifulSoup):
    code = []
    for one_code in soup.find_all("a"):
        if str(one_code.string).isnumeric():
            code.append(one_code.string)
    return code

# fce 'location' pro najití všech názvů obcí a uložení do listu 'location'
def location(soup: BeautifulSoup):
    location = []
    for name in soup.find_all("td"):
        if not str(name.string).isnumeric() and len(name.string) >= 2 and \
            not "s1" in name["headers"] and not "s2" in name["headers"]:
            location.append(name.string)
    return location

# fce 'registered' pro zjištění počtu voličů v seznamu
def registered(soup_town: BeautifulSoup) -> str:
    for i in soup_town.find_all("td"):
        if "sa2" in i["headers"]:
            return int(i.string.encode('ascii','ignore'))

# fce 'envelopes' pro zjištění počtu vydaných obálek
def envelopes(soup_town: BeautifulSoup) -> str:
    for i in soup_town.find_all("td"):
        if "sa3" in i["headers"]:
            return int(i.string.encode('ascii','ignore'))

# fce 'valid' pro zjištění počtu platných hlasů
def valid(soup_town: BeautifulSoup) -> str:
    for i in soup_town.find_all("td"):
        if "sa6" in i["headers"]:
            return int(i.string.encode('ascii','ignore'))

# fce 'political_party' pro vytvoření listu 'pol_party_list' názvů politických stran
def political_party(soup_town: BeautifulSoup):
    pol_party_list = []
    for i in soup_town.find_all("td"):
        if "t1sb2" in i["headers"] or "t2sb2" in i["headers"]:
            pol_party_list.append(i.string)
    return pol_party_list

# fce 'poll' pro vytvoření listu 'poll' počtu hlasů politických stran
def poll(soup_town: BeautifulSoup):
    poll_list = []
    for i in soup_town.find_all("td"):
        if "t1sb3" in i["headers"] or "t2sb3" in i["headers"]:
            poll_list.append(int(i.string.encode('ascii','ignore')))
    return poll_list

# fce pro vytvoření následujících listů
def lists(html_start, link):
    registered_list = [] # list voliči počet v seznamu
    envelopes_list = [] # list počet vydaných obálek
    valid_list = [] # list počet platných hlasů
    poll_list = [] # list počet hlasů jednotlivýchy stran - seznam seznamů

    for link_town in link:
        html_town = requests.get(html_start+link_town)
        soup_town = BeautifulSoup(html_town.text, "html.parser")
        
        reg = registered(soup_town)
        registered_list.append(reg)
        
        env = envelopes(soup_town)
        envelopes_list.append(env)
        
        val = valid(soup_town)
        valid_list.append(val)
        
        pol = poll(soup_town)
        poll_list.append(pol)
    return registered_list, envelopes_list, valid_list, poll_list


url, vystup = arguments() # načtení vstupů do proměnných
html_code = requests.get(url) # 'html_code' - proměnná pro získání url pomocí metody get 
soup = BeautifulSoup(html_code.text, "html.parser") # převedení url do typu bs4.BeautifulSoup - proměnná 'soup'
# print(soup) # vypsání celého html kódu (z původní 'url') do terminálu

link = link(soup) # proměnná 'link' - seznam všech url na jednotlivé obce
code = code(soup) # proměnná 'code' - seznam všech kódů jednotlivých obcí
location = location(soup) # proměnná 'location' - seznam názvů obcí

# pro kontrolu:
# print(link)                           # zobrazení listu 'link' do terminálu
# print(code)                           # zobrazení listu 'code' do terminálu
# print(location)                       # zobrazení listu 'location' do terminálu
# print(f"link {len(link)}")            # zobrazení délky listu 'link'
# print(f"code {len(code)}")            # zobrazení délky listu 'code'
# print(f"name_obec {len(location)}")   # zobrazení délky listu 'location'


html_start = "https://volby.cz/pls/ps2017nss/" # začátek url odkazu
html_first = requests.get(html_start+link[0]) # odkaz na první url
soup_first = BeautifulSoup(html_first.text, "html.parser") # soup prvního url
pol_party_list = political_party(soup_first) # názvy politických stran

# vytvoření záhlaví pro csv - list 'list_first'
list_first = ["Code", "Location", "Registered", "Envelopes", "Valid"]
for i in pol_party_list:
    list_first.append(i)

# vytvoření listu 'list_data' - číselné hodnoty pro csv
list_data = []
registered_list, envelopes_list, valid_list, poll_list = lists(html_start, link)
for i in range(0, len(link)):
    list_data.append([code[i], location[i], registered_list[i], envelopes_list[i], valid_list[i]])
    for j in poll_list[i]:
        list_data[i].append(j)

# vytvoření listu slovníků 'list_dict' - konečná data pro převedení do csv 
list_dict = []
for i in range(0, len(link)):
    dictionary = {}
    for j in range(0, len(list_first)):
        dictionary[list_first[j]] = list_data[i][j]
    list_dict.append(dictionary)

# vložení dat do csv
print(f"UKLÁDÁM DATA DO SOUBORU: {vystup}")
with open(vystup, mode="w", newline="") as new_csv:
    title = list_dict[0].keys()
    writer = csv.DictWriter(new_csv, delimiter=";", fieldnames=title)
    writer.writeheader()
    for i in range(0, len(link)):
        writer.writerow(list_dict[i])

print("UKONČUJI Election Scraper.")


# možnost vypsání csv souboru do terminálu:
# with open(vystup) as read_csv:
#     reading = csv.reader(read_csv, delimiter=" ")
#     for i in reading:
#         print(" ".join(i).replace(";", ", "))
        
