#Model.py 

from distutils.log import set_verbosity
import random
import uuid #Paket za ustvarjanje ID-ijev
import json
import os #Omogoča funkcije za "komuniciranje" z operacijskim sistemom


def pripravi_vprasanja():
    """Funkcija odpre dokument z vprašanji in prebere vsako vrstico posebje"""
    with open("vprasanja.txt", encoding="utf-8") as f:
        return [vrsta.strip() for vrsta in f.readlines()] #vrsta.strip, da se znebimo \n na koncu vrstice


MAKSIMUM = 24 #Maksimalno stevilo pravilno odgovorjeni vprasanj == Zmaga
ZMAGA = "ČESTITKE, pravilno ste odgovorili na vseh 24 vprašanj!"
ZACETEK = "Zacetek"
PRAVILNO = "p"
NAPACNO = "n"
rezultat = 0


class Vprasanje:

    VPRASANJA = [] #V ta seznam bomo dodajali vprašanja

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
    with open("vprasanja.json") as f:
        seznam_vprasanj = json.load(f)
    for vprasanje in seznam_vprasanj:
        vpr = Vprasanje()
        vpr.nalozi(vprasanje)

def najdi_vprasajne(id_vprasanja):
    for vprasanje in Vprasanje.VPRASANJA:
        if vprasanje.id_vprasanja == id_vprasanja:
            return vprasanje


class Kviz:
    def __init__(self):
        self.igre = {}
        self.datoteka_s_stanjem = "stanje.json"

    def prost_id_igre(self):
        while True:
            kandidat = uuid.uuid4().int #uuid4 nam vrne "kodo" oz. id iz samih številk
            if kandidat not in self.igre: #Če se ta ID še ne pojavi, 
                return kandidat           #Nam ga vrne  

    def nalozi_igre_iz_datoteke(self):
        if os.path.exists(self.datoteka_s_stanjem):
            with open(self.datoteka_s_stanjem, encoding="utf-8") as f:
                zgodovina = json.load(f)
            for id_igre, (tuple, odgovor, stanje) in zgodovina.items():
                igra = Vprasanje(tuple)
                igra.odgovor = set(odgovor)
                self.igre[int(id_igre)] = (igra, stanje)

    def nova_igra(self):
        self.nalozi_igre_iz_datoteke()
        igra = nova_igra()
        novi_id = self.prost_id_igre() #Izberemo nek nov ID
        self.igre[novi_id] = (igra, ZACETEK)
        self.zapisi_igre_v_datoteko() #Igro zabeležimo v datoteko
        return novi_id                #Funkcija pa nam vrne samo nov ID

    def ugibaj(self, id_igre, odgovor):
        self.nalozi_igre_iz_datoteke()
        igra = self.igre[id_igre][0]
        novo_stanje = igra.ugibaj(odgovor)
        self.igre[id_igre] = (igra, novo_stanje)
        self.zapisi_igre_v_datoteko()

    # def nalozi_igre_iz_datoteke(self):
    #     if os.path.exists(self.datoteka_s_stanjem):
    #         with open(self.datoteka_s_stanjem, encoding="utf-8") as f:
    #             zgodovina = json.load(f)
    #         for id_igre, (vprasanje, odgovor, stanje) in zgodovina.items():
    #             igra = Vprasanje(vprasanje)
    #             igra.odgovori = set(odgovor)
    #             self.igre[int(id_igre)] = (igra, stanje)

    def zapisi_igre_v_datoteko(self):
        """Kako se bo zadeva izpisevala v .json datoteko"""
        za_odlozit = {}
        for id_igre, (igra, stanje) in self.igre.items():
            za_odlozit[id_igre] = (igra.vprasanje, igra.odgovor, stanje)
        with open(self.datoteka_s_stanjem, "w", encoding="utf-8") as f:
            json.dump(za_odlozit, f)