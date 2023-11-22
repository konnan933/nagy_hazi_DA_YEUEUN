import re
import pyconio  
import glob
from esemenyek import Esemenyek 

def sendErrorMessage(text):
    pyconio.textcolor(pyconio.BLACK)
    pyconio.textbackground(pyconio.RED)
    print(text, end="")
    setOutputColor()
    print("")

def sendImportantMessage(text):
    pyconio.textcolor(pyconio.BLACK)
    pyconio.textbackground(pyconio.YELLOW)
    print(text, end="")
    setOutputColor()
    print("")

def line_separator():
    pyconio.textcolor(pyconio.BLACK)
    pyconio.textbackground(pyconio.LIGHTGRAY)
    print("----------------------------------------------", end="")  #átláthatóság a konzolon miatt
    setOutputColor()
    print("")

def setOutputColor():
    pyconio.textcolor(pyconio.BLACK)
    pyconio.textbackground(pyconio.BLUE)

def sendConfirmMessage(text):
    pyconio.textcolor(pyconio.BLACK)
    pyconio.textbackground(pyconio.GREEN)
    print(text, end="")
    setOutputColor()
    print("")

def ciklus_kiiratas(esemenyek):
    for esemeny in esemenyek:
        print(str(esemeny))

def bejelntkezes_folyamat(fiokok):
    line_separator()
    nevek = fiokok.log_in_nev_input()
    succesful_log_in = fiokok.log_in(nevek)
    while succesful_log_in == None: 
        succesful_log_in = fiokok.log_in(nevek)
    return succesful_log_in

def bejenkezes_or_add_felhasznalo(fiokok):
    line_separator()
    valasz = input(f"Bejelentkezéshez  (adja meg az 1-est)\nÚj fiók lértehozásához (adja meg az 2-est)\nKilépés (adja meg az 9-est) ")

    while valasz != "1" and valasz != "2" and valasz != "9":
        sendErrorMessage("Rossz számot adott meg")
        valasz = input(f"Bejelentkezéshez  (adja meg az 1-est)\nÚj fiók lértehozásához (adja meg az 2-est)\nKilépés (adja meg az 9-est) ")

    if(valasz == "1"):
        return bejelntkezes_folyamat(fiokok)
    elif(valasz == "2"):
        fiokok.addFelhasznalo()
        return bejelntkezes_folyamat(fiokok)
    elif(valasz == "9"):
        line_separator()
        sendConfirmMessage("Sikeresen kilépett!")
        return None
    


def fiok_esmenyei(fiok_id):
    esemenyek = Esemenyek(fiok_id)
    if(len(esemenyek.esemeny_tomb) == 0):
        sendImportantMessage("Még nincsen eseményed csinálj újjat!")
        esemenyek.addEsemeny(fiok_id)
    return esemenyek    

def esemeny_konzol_valasztasok():
    line_separator()
    input_lista = ["1", "2", "3", "4", "5", "6", "9"]
    valasz = input("Eseményeim megnézése (adja meg az 1-est)\n"+
                   "Új esemény hozzá adása (adja meg az 2-est)\n"+
                   "Esemény szerkeztése (adja meg az 3-ast)\n"+
                   "Esemény törlése (adja meg az 4-est)\n"+
                   "Saját adataim exportálása (adja meg az 5-öst)\n"+
                   "Kijelentkezés (adja meg az 6-ost)\n"+
                   "Kilépés (adja meg az 9-est) ")
    while valasz not in input_lista:
        sendErrorMessage("Rossz számot adott meg")
        valasz = input("Eseményeim megnézése (adja meg az 1-est)\n"+
                   "Új esemény hozzá adása (adja meg az 2-est)\n"+
                   "Esemény szerkeztése (adja meg az 3-ast)\n"+
                   "Esemény törlése (adja meg az 4-est)\n"+
                   "Saját adataim exportálása (adja meg az 5-öst)\n"+
                   "Kijelentkezés (adja meg az 6-ost)\n"+
                   "Kilépés (adja meg az 9-est) ")
    return valasz

def esemeny_konzol_eldontes(valasz, esemenyek, fiok_id):
    line_separator()
    if(valasz == "1"):
        esemeny_megjelenites_valasztasok(esemenyek)
    elif(valasz == "2"):
        esemenyek.addEsemeny(fiok_id)
    elif(valasz == "3"):
        esemeny_szerkeztes_valsztasok(esemenyek,esemenyek.show_by_index_fiok())
    elif(valasz == "4"):
        esemenyek.deleteEsemeny(esemenyek.show_by_index_fiok())
    elif(valasz == "5"):
        foik_export_valasztas(esemenyek)
    elif(valasz == "6"):
        sendConfirmMessage("Sikeres kijelenkezés!")
    elif(valasz == "9"): 
        sendConfirmMessage("Sikeresen kilépett!")

def foik_export_valasztas(esemenyek):
    fajl_nev = input("Kérem adja meg a fájl nevet! (kiterjesztést nem kell megadni) ")
    
    while None == re.fullmatch(r'^[a-zA-Z0-9_-]+$', fajl_nev):
        sendErrorMessage("Hibás fájl név adjon újjat!:")
        fajl_nev = input("Kérem adja meg a fájl nevet! (kiterjesztést nem kell megadni) ")
    if(2 in [file.find(fajl_nev+".txt") for file in glob.glob("./*")]): # glob vissza adja ebben a fáljban az összes  file-t és find-al megnézzézük hogy léztezik e már ilyen kiterjesztésű txt
        sendErrorMessage("Adjon új nevet ez már foglalt: ")
        foik_export_valasztas(esemenyek)
    else:
        sendConfirmMessage(f"Sikeres volt az adatok exportja, {fajl_nev}.txt néven fogja találni a fő mappában.")
        esemenyek.fiok_esemenyek_export(fajl_nev)

def esemeny_szerkeztes_valsztasok(esemenyek, valasztott_index):
    input_lista = ["1", "2", "3", "4"]
    line_separator()
    valasz = input("Esemény  név szerkeztése (adja meg az 1-est)\n"+
            "Esemény  dátum szerkeztése (adja meg az 2-est)\n"+
            "Esemény  hely szerkeztése (adja meg az 3-ast)\n"+
            "Esemény  megjegyzés szerkeztése (adja meg az 4-est) ")
    
    while valasz not in input_lista:
        sendErrorMessage("Rossz számot adott meg")
        valasz = input("Esemény  név szerkeztése (adja meg az 1-est)\n"+
                    "Esemény  dátum szerkeztése (adja meg az 2-est)\n"+
                    "Esemény  hely szerkeztése (adja meg az 3-ast)\n"+
                    "Esemény  megjegyzés szerkeztése (adja meg az 4-est) ")
    
    
    if(valasz == "1"):
        esemenyek.fiok_esemenyei[valasztott_index].setNev(esemenyek.inputNev())
        sendConfirmMessage("Sikeresen megváltoztatta!")
    elif(valasz == "2"):
        esemenyek.fiok_esemenyei[valasztott_index].setDatum(esemenyek.inputDatum())
        sendConfirmMessage("Sikeresen megváltoztatta!")
    elif(valasz == "3"):
        esemeny_szerkeztes_valsztasok_hely(esemenyek, valasztott_index)
    elif(valasz == "4"):
        esemenyek.fiok_esemenyei[valasztott_index].setMegjegyzes(esemenyek.inputMegjegyzes())
        sendConfirmMessage("Sikeresen megváltoztatta!")

def esemeny_szerkeztes_valsztasok_hely(esemenyek, valasztott_index):
    line_separator()
    input_lista = ["1", "2", "3", "4"]

    valasz = input("Hely iranyitó szám szerkeztése (adja meg az 1-est)\n"+
                    "Város szerkeztése (adja meg az 2-est)\n"+
                    "Utca  szerkeztése (adja meg az 3-ast)\n"+
                    "Ház szám   szerkeztése (adja meg az 4-est) ")
    
    while valasz not in input_lista:
        sendErrorMessage("Rossz számot adott meg")
        valasz = input("Hely iranyitó szám szerkeztése (adja meg az 1-est)\n"+
                        "Város szerkeztése (adja meg az 2-est)\n"+
                        "Utca szerkeztése (adja meg az 3-ast)\n"+
                        "Ház szám szerkeztése (adja meg az 4-est) ")
        
    if(valasz == "1"):
        esemenyek.fiok_esemenyei[valasztott_index].getHely().setIranyitoSzam(esemenyek.inputHelyISzam())
    elif(valasz == "2"):
        esemenyek.fiok_esemenyei[valasztott_index].getHely().setVaros(esemenyek.inputHelyVaros())
    elif(valasz == "3"):
        esemenyek.fiok_esemenyei[valasztott_index].getHely().setUtca(esemenyek.inputHelyUtca())
    elif(valasz == "4"):
        esemenyek.fiok_esemenyei[valasztott_index].getHely().setHazSzam(esemenyek.inputHelyHazSzam())
    sendConfirmMessage("Sikeresen megváltoztatta!")

def esemeny_megjelenites_valasztasok(esemenyek):
    valasz = input(f"Idő szerinti sorrendben megnézni (adja meg az 1-est)\nFelvett sorrendben megnézni (adja meg az 2-est)\nNév alapján keresés (adja meg az 3-ast)")

    while valasz != "1" and valasz != "2" and valasz != "3":
        sendErrorMessage("Rossz számot adott meg")
        valasz = input(f"Bejelentkezéshez  (adja meg az 1-est)\nÚj fiók lértehozásához (adja meg az 2-est)")
    line_separator()
    if(valasz == "1"):
        ciklus_kiiratas(esemenyek.sort_by_datum())
    elif(valasz == "2"):
        ciklus_kiiratas(esemenyek.fiok_esemenyei)
    elif(valasz == "3"):
        print(esemenyek.search_by_nev_fiok())

def input_ev():
    while True:
            try:
                ev = int(input("Kérem adja meg a év számát:"))
                while ev < 0:                    
                    sendErrorMessage("Év nem lehet negatív!")
                    ev = int(input("Kérem adja meg a év számát:"))
                return ev
            except ValueError:
                sendErrorMessage("Nem lehet karakter a év számában.")
                continue

def search_by_week_input():

    while True:
            try:
                het = int(input("Kérem adja meg a hét számát:"))
                while het in range(1, 53):                    
                    sendErrorMessage("Egy évben 52 hét van, és nem lehet 0-nál kissebb!")
                    het = int(input("Kérem adja meg a hét számát:"))
                return het
            except ValueError:
                sendErrorMessage("Nem lehet karakter a hét számában.")
                continue

def search_by_month_input():

    while True:
            try:
                honap = int(input("Kérem adja meg a hónap számát:"))
                while honap in range(1, 13):                    
                    sendErrorMessage("Egy évben 52 hónap van, és nem lehet 0-nál kissebb!")
                    honap = int(input("Kérem adja meg a hónap számát:"))
                return honap
            except ValueError:
                sendErrorMessage("Nem lehet karakter a hónap számában.")
                continue

def search_by_day_input(ev ,honap):
    max_nap_of_month = check_if_day_valid(ev ,honap)+1
    while True:
            try:
                nap = int(input("Kérem adja meg a nap számát:"))
                while nap in range(1, max_nap_of_month+1):                    
                    sendErrorMessage(f"1 és {max_nap_of_month} között lehet a nap!")
                    nap = int(input("Kérem adja meg a nap számát:"))
                return nap
            except ValueError:
                sendErrorMessage("Nem lehet karakter a nap számában.")
                continue   

def check_if_day_valid(ev ,honap):
    if honap == 1 or honap == 3 or honap == 5 or honap == 7 or honap == 8 or honap == 10 or honap == 12:
        return 31
    elif honap == 4 or honap == 6 or honap == 9 or honap == 11:
        return 30
    elif ev % 4 == 0 and ev % 100 != 0 or ev % 400 == 0:
        return 29
    else:
        return 28