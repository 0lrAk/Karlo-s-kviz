#Model.py 

from distutils.log import set_verbosity
import random
import uuid #Paket za ustvarjanje ID-ijev
import json
import os #Omogoča funkcije za "komuniciranje" z operacijskim sistemom
import random


class Vprasanje:

    VPRASANJA = [] # seznam vseh vprasanj

    def __init__(self):
        self.id_vprasanja = -1
        self.tekst = ""
        self.odgovori = []
    
    def nalozi(self, podatki):
        self.id_vprasanja = podatki["id"]
        self.tekst = podatki["tekst"]
        for i, odgovor in enumerate(podatki["odgovori"]):
            if i == 0:
                self.odgovori.append((odgovor, True))
            else:
                self.odgovori.append((odgovor, False))

        Vprasanje.VPRASANJA.append(self)
    
    def premesaj_odgovore(self):
        random.shuffle(self.odgovori)
    
    def __str__(self):
        return f"{self.tekst}\n{self.odgovori[0]}\n{self.odgovori[1]}\n{self.odgovori[2]}\n{self.odgovori[3]}"
    


def pripravi_vprasanja():
    with open("vprasanja.json", "r", encoding="utf-8") as f:
        seznam_vprasanj = json.load(f)
    for vprasanje in seznam_vprasanj:
        v = Vprasanje()
        v.nalozi(vprasanje)

def najdi_vprasajne(id_vprasanja):
    for vprasanje in Vprasanje.VPRASANJA:
        if vprasanje.id_vprasanja == id_vprasanja:
            return vprasanje
    

class Igra:

    IGRE = {} # seznam iger

    def __init__(self):
        self.id_igre = None
        self.vprasanja = []
        self.stevilka_vprasanja = 0
        self.pravilni = 0

    def nova_igra(self):
        self.id_igre = self._prost_id_igre()
        self.vprasanja = random.sample(Vprasanje.VPRASANJA, 25)
        Igra.IGRE[self.id_igre] = self
    
    def _prost_id_igre(self):
        while True:
            kandidat = uuid.uuid4().int    # uuid4 nam vrne "kodo" oz. id iz samih številk
            if kandidat not in Igra.IGRE:  # Če se ta ID še ne pojavi, 
                return kandidat            # Nam ga vrne  
        
    def ugibaj(self, odgovor):
        vprasanje = self.vprasanja[self.stevilka_vprasanja]
        if vprasanje.odgovori[odgovor][1] == True:
            self.pravilni += 1
        self.stevilka_vprasanja += 1
    
    def get_vprasanje(self, stevilka):
        return self.vprasanja[stevilka]
    
    def __str__(self):
        return str(self.get_vprasanje(self.stevilka_vprasanja))
    
    def stajne(self):
        stanje = {}
        stanje["id"] = self.id_igre
        stanje["vprasanja"] = []
        stanje["stevilka_vprasanja"] = self.stevilka_vprasanja
        stanje["pravilni"] = self.pravilni
        for vprasanje in self.vprasanja:
            stanje["vprasanja"].append(vprasanje.id_vprasanja)
        return stanje
    
    def shrani_stanje(self):
        if os.path.exists("stanje.json"):
            with open("stanje.json", "r", encoding="utf-8") as f:
                stanja = json.load(f)
        else:
            stanja = []

        for stanje in stanja:
            if int(stanje["id"]) == self.id_igre:
                stanja.remove(stanje)
                break

        stanja.append(self.stajne())
        with open("stanje.json", "w", encoding="utf-8") as f:
            json.dump(stanja, f)
        
    def nalozi_stanje(self, id_igre):
        if id_igre in Igra.IGRE:
            print("Igra je ze nalozena")
            return

        if os.path.exists("stanje.json"):
            with open("stanje.json", "r", encoding="utf-8") as f:
                stanja = json.load(f)
        else:
            print("Nobena igra ni shranjena.")
            self.nova_igra()
            return
        
        for stanje in stanja:
            if int(stanje["id"]) == id_igre:
                break
        else:
            print("Igra ne obstaja.")
            self.nova_igra()
            return

        self.id_igre = id_igre
        self.stevilka_vprasanja = stanje["stevilka_vprasanja"]
        self.pravilni = stanje["pravilni"]
        for nr in stanje["vprasanja"]:
            self.vprasanja.append(najdi_vprasajne(nr))



VPRASANJA = pripravi_vprasanja()
MAKSIMUM = 24 #Maksimalno stevilo pravilno odgovorjeni vprasanj == Zmaga
ZMAGA = "ČESTITKE, pravilno ste odgovorili na vseh 24 vprašanj!"
ZACETEK = "Zacetek"
PRAVILNO = "p"
NAPACNO = "n"
rezultat = 0



class Kviz:
    def __init__(self):
        self.igre = {}
        self.datoteka_s_stanjem = "stanje.json"

    def nova_igra(self):
        igra = Igra()
        igra.nova_igra()
        return igra
    
    def nalozi_igro(self, id_igre):
        igra = Igra()
        igra.nalozi_stanje(id_igre)
        return igra
    
    def nalozi_vse_igre(self):
        if os.path.exists("stanje.json"):
            with open("stanje.json", "r", encoding="utf-8") as f:
                stanja = json.load(f)
        else:
            print("Nobena igra ni shranjena.")
            stanja = []
            return
        
        for stanje in stanja:
            igra = Igra()
            igra.id_igre = stanje["id"]
            igra.stevilka_vprasanja = stanje["stevilka_vprasanja"]
            igra.pravilni = stanje["pravilni"]
            for nr in stanje["vprasanja"]:
                igra.vprasanja.append(najdi_vprasajne(nr))

    def ugibaj(self, id_igre, odgovor):
        igra = Igra.IGRE[id_igre]
        igra.ugibaj(odgovor)
    
    def shrani_stanje_igre(self, id_igre):
        Igra.IGRE[id_igre].shrani_stanje()
    
    def shrani_vse_igre(self):
        if os.path.exists("stanje.json"):
            with open("stanje.json", "r", encoding="utf-8") as f:
                stanja = json.load(f)
        else:
            stanja = []

        for stanje in stanja:
            for id_igre in Igra.IGRE:
                if int(stanje["id"]) == id_igre:
                    stanja.remove(stanje)
                    break
        
        for id_igre in Igra.IGRE:
            stanja.append(Igra.IGRE[id_igre].stajne())
        with open("stanje.json", "w", encoding="utf-8") as f:
            json.dump(stanja, f)
        print("Igre so shranjene.")