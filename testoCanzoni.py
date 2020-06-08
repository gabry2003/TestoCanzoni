#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__project__ = "Testo canzoni"
__file__ = "testoCanzoni.py"
__author__ = "Gabriele Princiotta"
__version__ = "1.0"
__email__ = "gabriprinciott@gmail.com"
__date__ = "2020-05-21"

import subprocess, os, platform
import requests
from bs4 import BeautifulSoup

def pulisci():
    """ Pulisce la console e stampa a schermo il nome del programma """
    os.system("clear")
    print("-------------------------------")
    print("----- Gabriele Princiotta -----")
    print("----- Testo canzoni       -----")
    print("----- v. 1.0              -----")
    print("-------------------------------")
    print("\nPuoi cercare il testo di una canzone e, se e' disponibile, ti verra' restituita anche la traduzione\n")

def cerca(nome,artista):
    """ Cerca la canzone sul sito mtv.it """
    URL_SITO = "http://testicanzoni.mtv.it"  # URL sito per prendere i testi delle canzoni
    r = requests.post(URL_SITO, params ={
        "query": artista + " - " + nome
    })

    if r.status_code == 200:
        result = r.text
        soup = BeautifulSoup(result, 'html.parser')

        canzoni = []

        for li in soup.select("ul.research_result a"):
            canzoni.append([
                li.get_text(),
                URL_SITO + li.get("href").replace("testo-","traduzione-")
            ])

        return canzoni
    else:
        print("Impossibile controllare le canzoni!")
        exit()

def leggiTesto(urlCanzone):
    """ Ritorna il testo e la traduzione della canzone """
    r = requests.post(urlCanzone)

    if r.status_code == 200:
        result = r.text
        soup = BeautifulSoup(result, 'html.parser')

        return str(soup.select("div.testo")[0])
    else:
        print("Impossibile leggere il testo della canzone!")
        exit()

def apriFile(nomeFile):
    """ Apre un file con l'applicazione di default dell'OS """
    if platform.system() == 'Darwin':  # macOS
        subprocess.call(('open', nomeFile))
    elif platform.system() == 'Windows':  # Winzozz
        os.startfile(nomeFile)
    else:  # Linux
        subprocess.call(('xdg-open', nomeFile))

def salvaSuFile(nomeBrano,testo):
    """ Salva su un file il testo originale e la traduzione """
    nomeFile = "/tmp/" + nomeBrano + ".html"

    testo = testo.replace('<p class="traduction"></p>','')  # Elimino i p vuoti in caso non esiste la traduzione

    headerHtml = "<!doctype html>" \
                 "<html>" \
                 "  <head>" \
                 "      <title>" + nomeBrano + "</title>" \
                 "      <link rel='stylesheet' href='http://testicanzoni.mtv.it/static/mtvit15/mtvit18/css/mtvit18.css'>" \
                 "      <link rel='stylesheet' href='http://testicanzoni.mtv.it/static/mtvit15/mtvit18/css/style.css'>" \
                 "      <link rel='stylesheet' href='http://testicanzoni.mtv.it/static/mtvit15/bootstrap.min.css'>" \
                 "      <link rel='stylesheet' href='https://fonts.googleapis.com/css2?family=Raleway&display=swap'>" \
                 "      <style>" \
                 "          .traduction {" \
                 "              font-weight:bold;" \
                 "              font-family: 'Raleway', sans-serif;" \
                 "          }" \
                 "          body * {" \
                 "              font-family: 'Raleway', sans-serif;" \
                 "          }" \
                 "          body {" \
                 "              background: rgb(34,193,195);" \
                 "              background: linear-gradient(0deg, rgba(34,193,195,1) 0%, rgba(253,187,45,1) 100%);" \
                 "          }" \
                 "          .testo-info {" \
                 "              background: #fff;" \
             "              }" \
                 "      </style>" \
                 "  </head>" \
                 "  <body>" \
                "   <!-- Viva la vespa -->"
    footerHtml = "  </body>" \
                 "  </html>"

    f = open(nomeFile,"w")
    f.write(headerHtml + testo + footerHtml)
    f.close()

    apriFile(nomeFile)

def main():
    """ Programma che prende in input il nome di una canzone, cerca su internet il testo e la traduzione di quella canzone e se la trova la stampa a schermo """

    continuare = True
    while continuare:   # Fino a quando devo l'utente vuole continuare a cercare testi di canzoni
        pulisci()
        nomeCanzone = input("Inserisci il nome della canzone (lascia vuoto per cercare tutte le canzoni dell'artista): ")
        nomeArtista = input("Inserisci il nome dell'artista (lascia vuoto per cercare in tutti gli artisti): ")

        if not nomeArtista == "" or not nomeCanzone == "":
            canzoni = cerca(nome = nomeCanzone, artista = nomeArtista)

            if len(canzoni) > 0:  # Se ho trovato la canzone
                print("\nHo trovato {} canzoni:".format(len(canzoni)))
                for i in range(len(canzoni)):
                    print("{} - {}".format(i,canzoni[i][0]))

                scelta = int(input("\nQuale canzone scegli (inserisci il numero)? "))
                if scelta < 0 or scelta >= len(canzoni):
                    print("Canzone non presente nella lista!")
                else:
                    salvaSuFile(nomeBrano = canzoni[scelta][0],testo = leggiTesto(canzoni[scelta][1]))
            else:
                print("Canzone non trovata!")
        else:
            print("Inserisci almeno un artista o una canzone")
        continuare = input("Vuoi cercare il testo di altre canzoni? (s|n) ").lower() == 's'

if __name__ == "__main__":
    main()
