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

# fce 'arguments' pro získání vstupu od uživatele: název webové stánky 'url' a název výstupu 'csv'
def arguments():
    print(sys.argv)
    if len(sys.argv) == 3:
        global url
        global vystup
        url = sys.argv[1]
        vystup = sys.argv[2]
        try:
            requests.get(url)
            if url[0:34] == "https://volby.cz/pls/ps2017nss/ps3" and vystup[-4:] == ".csv" and len(vystup) > 4:
                print(f"STAHUJI DATA Z VYBRANÉHO URL: {url}")                
        except:
            print("ŠPATNÝ VSTUP. NAPIŠ ZNOVU:")
            print('python projekt_3.py <odkaz-uzemniho-celku> <vysledny-soubor.csv>')
            exit()        
    else:
        print("ŠPATNÝ VSTUP. NAPIŠ ZNOVU:")
        print('python projekt_3.py <odkaz-uzemniho-celku> <vysledny-soubor.csv>')
        exit()

# fce 'link' pro najití všech webových odkazů na jednotlivé obce a uložení do listu 'link'
def f_link(soup: BeautifulSoup) -> list:
    link = []
    for one_link in soup.find_all("a"):
        if one_link.string != "X" and "vyber" in one_link["href"] or "okrsek" in one_link["href"]:
            link.append(one_link["href"])
    return link

# fce 'code' pro najití všech číselných kódů obcí a uložení do listu 'code'
def f_code(soup: BeautifulSoup) -> list:
    code = []
    for one_code in soup.find_all("a"):
        if str(one_code.string).isnumeric():
            code.append(one_code.string)
    return code

# fce 'location' pro najití všech názvů obcí a uložení do listu 'location'
def f_location(soup: BeautifulSoup) -> list:
    location = []
    for name in soup.find_all("td"):
        if not str(name.string).isnumeric() and len(name.string) >= 2 and \
            not "s1" in name["headers"] and not "s2" in name["headers"]:
            location.append(name.string)
    return location

# fce 'registered' pro zjištění počtu voličů v seznamu
def f_registered(soup_town: BeautifulSoup) -> str:
    for i in soup_town.find_all("td"):
        if "sa2" in i["headers"]:
            return int(i.string.encode('ascii','ignore'))

# fce 'envelopes' pro zjištění počtu vydaných obálek
def f_envelopes(soup_town: BeautifulSoup) -> str:
    for i in soup_town.find_all("td"):
        if "sa3" in i["headers"]:
            return int(i.string.encode('ascii','ignore'))

# fce 'valid' pro zjištění počtu platných hlasů
def f_valid(soup_town: BeautifulSoup) -> str:
    for i in soup_town.find_all("td"):
        if "sa6" in i["headers"]:
            return int(i.string.encode('ascii','ignore'))

# fce 'political_party' pro vytvoření listu 'pol_party_list' názvů politických stran
def f_political_party(soup_town: BeautifulSoup) -> list:
    pol_party_list = []
    for i in soup_town.find_all("td"):
        if "t1sb2" in i["headers"] or "t2sb2" in i["headers"]:
            pol_party_list.append(i.string)
    return pol_party_list

# fce 'poll' pro vytvoření listu 'poll' počtu hlasů politických stran
def f_poll(soup_town: BeautifulSoup) -> list:
    poll_list = []
    for i in soup_town.find_all("td"):
        if "t1sb3" in i["headers"] or "t2sb3" in i["headers"]:
            poll_list.append(int(i.string.encode('ascii','ignore')))
    return poll_list

# fce pro vytvoření následujících listů
def f_lists(html_start, link) -> list:
    registered_list = [] # list voliči počet v seznamu
    envelopes_list = [] # list počet vydaných obálek
    valid_list = [] # list počet platných hlasů
    poll_list = [] # list počet hlasů jednotlivýchy stran - seznam seznamů

    for link_town in link:
        html_town = requests.get(html_start+link_town)
        soup_town = BeautifulSoup(html_town.text, "html.parser")
        
        reg = f_registered(soup_town)
        registered_list.append(reg)
        
        env = f_envelopes(soup_town)
        envelopes_list.append(env)
        
        val = f_valid(soup_town)
        valid_list.append(val)
        
        pol = f_poll(soup_town)
        poll_list.append(pol)
    return registered_list, envelopes_list, valid_list, poll_list

# fce pro vytvoření konečných dat pro převedení do csv ve formě listu slovníků - proměnná 'list_dict'
def f_data_csv():
    html_code = requests.get(url) # 'html_code' - proměnná pro získání url pomocí metody get
    global soup
    soup = BeautifulSoup(html_code.text, "html.parser") # převedení url do typu bs4.BeautifulSoup - proměnná 'soup'
    link = f_link(soup)
    code = f_code(soup)
    location = f_location(soup)

    html_start = "https://volby.cz/pls/ps2017nss/"
    html_first = requests.get(html_start+f_link(soup)[0])
    soup_first = BeautifulSoup(html_first.text, "html.parser") # soup prvního url
    pol_party_list = f_political_party(soup_first) # názvy politických stran
    list_first = ["Code", "Location", "Registered", "Envelopes", "Valid"]
    for i in pol_party_list:
        list_first.append(i)
    
    list_data = [] # číselné hodnoty pro csv
    registered_list, envelopes_list, valid_list, poll_list = f_lists(html_start, link)
    for i in range(0, len(link)):
        list_data.append([code[i], location[i], registered_list[i], envelopes_list[i], valid_list[i]])
        for j in poll_list[i]:
            list_data[i].append(j)

    list_dict = []
    for i in range(0, len(link)):
        dictionary = {}
        for j in range(0, len(list_first)):
            dictionary[list_first[j]] = list_data[i][j]
        list_dict.append(dictionary)
    return list_dict

# vložení dat do csv
def print_csv():
    list_dict = f_data_csv()
    link = f_link(soup)
    print(f"UKLÁDÁM DATA DO SOUBORU: {vystup}")
    with open(vystup, mode="w", newline="") as new_csv:
        title = list_dict[0].keys()
        writer = csv.DictWriter(new_csv, delimiter=";", fieldnames=title)
        writer.writeheader()
        for i in range(0, len(link)):
            writer.writerow(list_dict[i])
    print("UKONČUJI Election Scraper.")

if __name__ == "__main__":
    arguments()
    print_csv()

# možnost vypsání csv souboru do terminálu:
# with open(vystup) as read_csv:
#     reading = csv.reader(read_csv, delimiter=" ")
#     for i in reading:
#         print(" ".join(i).replace(";", ", "))