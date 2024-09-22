# Engeto projekt_3

Třetí projekt do Engeto Online Python Akademie

## Popis projektu

Tento projekt slouží k extrahování výsledků z parlamentních voleb v roce 2017 z následujícího odkazu [zde](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ). Program umí získat výsledky z jakéhokoliv uzemního celku včetně zahraničí a následně je uloží do csv souboru.
URL územního celku vybereme ze sloupce `Výběr obce` podle obrázku:

![Vyber_obce](https://github.com/user-attachments/assets/910567ff-0ada-4f8f-9b57-e233cab04fb5)

## Virtuální prostředí

Před spuštěním programu je třeba aktivovat virtuální prostředí pomocí příkazového řádku / powershellu.

Soubory `projekt_3.py` a `requirements.txt` je potřeba vložit do složky aktivního virtuálního prostředí.

## Instalace knihoven

Použité knihovny třetích stran a jejich verze jsou uloženy v souboru: <pre>requirements.txt</pre> Do nově vytvořeného virtuálního prostředí se pomocí následujícího příkazu nainstalují potřebné knihovny:
<pre>pip3 install -r requirements.txt</pre>

## Spuštění projektu

Ke spuštění souboru projekt_3.py je potřeba dvou argumentů:

<pre>
1. argument: url_uzemniho_celku 
2. argument: csv_soubor
</pre>

Do příkazového řádku se následně napíše:

<pre>python projekt_3.py "url_uzemniho_celku" "csv_soubor"</pre>

## Ukázka projektu pro územní celek Třebíč

Spuštění programu:

<pre>python projekt_3.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=10&xnumnuts=6104" "vysledky_trebic.csv"</pre>

Spuštění stahování:

<pre>
STAHUJI DATA Z VYBRANÉHO URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=10&xnumnuts=6104
UKLÁDÁM DATA DO SOUBORU: vysledky_trebic.csv
UKONČUJI Election Scraper.
</pre>

Částečný výstup

- z terminálu:
<pre>
Code, Location, Registered, Envelopes, Valid, Občanská demokratická strana, Řád národa - Vlastenecká unie, CESTA ODPOVĚDNÉ SPOLEČNOSTI, Česká str.sociálně demokrat., Radostné Česko, ... 
590274, Babice, 167, 126, 126, 9, 0, 0, 11, 0, 8, 9, 0, 0, 3, 0, 0, 16, 0, 1, 40, 0, 19, 0, 1, 0, 0, 7, 2 
590282, Bačice, 165, 104, 104, 1, 1, 0, 5, 0, 6, 23, 0, 1, 0, 0, 0, 5, 1, 2, 33, 1, 7, 0, 0, 0, 0, 14, 4 
544833, Bačkovice, 88, 53, 52, 1, 0, 0, 9, 0, 1, 7, 0, 1, 0, 0, 0, 3, 0, 3, 18, 0, 5, 0, 0, 0, 0, 4, 0 
590304, Benetice, 150, 117, 117, 3, 0, 0, 15, 0, 4, 6, 0, 1, 0, 0, 0, 11, 0, 2, 41, 0, 23, 0, 0, 0, 0, 10, 1 
590312, Biskupice-Pulkov, 222, 118, 118, 7, 0, 0, 7, 1, 8, 13, 2, 1, 1, 0, 0, 6, 2, 2, 48, 0, 14, 0, 0, 0, 0, 6, 0 
590321, Blatnice, 303, 177, 177, 7, 0, 0, 16, 0, 2, 25, 1, 1, 1, 0, 0, 9, 0, 1, 66, 0, 26, 0, 0, 2, 0, 20, 0 
550400, Bohušice, 124, 76, 76, 6, 0, 0, 4, 0, 4, 9, 0, 1, 0, 0, 0, 2, 0, 9, 20, 0, 10, 0, 0, 0, 0, 11, 0 
590347, Bochovice, 137, 104, 102, 2, 1, 0, 8, 0, 4, 2, 1, 0, 3, 0, 0, 9, 0, 8, 42, 0, 10, 0, 0, 1, 0, 10, 1 
590363, Bransouze, 200, 149, 148, 10, 3, 0, 23, 0, 7, 16, 1, 1, 1, 0, 0, 12, 0, 5, 48, 0, 15, 0, 3, 0, 0, 3, 0
</pre>

- z csv souboru:

![csv_vystup](https://github.com/user-attachments/assets/3daf6a8d-744c-42d2-b352-c4e5eb6ad012)
