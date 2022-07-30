
import random
import uuid
import json
import os

def nakljucno_vprasanje():
    vrstice = open("vprasanja.txt").read().splitlines()
    trenutno_vprasanje = random.choice(vrstice)
    return trenutno_vprasanje

rezultat = int(0)
VPRASANJE = nakljucno_vprasanje()
ZACETEK = "Zacetek"
ZMAGA = "Čestitke, pravilno ste odgovorili na vseh 10 vprašanj"
PORAZ = "Na žalost ste izgubili. Poskusite ponovno."
PRAVILNO = "Vaš odgovor je pravilen"

class Vprasanje:
    def __init__(self, tuple):
        self.vprasanje = tuple[0]
        self.odgovori = tuple[1:3]
        self.resitev = tuple[-1]
    
    def pravilnost_odogovora(self, odgovor):
        if odgovor == self.resitev:
            rezultat += 1
            return True
        else:
            pass
    def rezultat(self):
        return rezultat

    def zmaga(self):
        return rezultat == 10
        
    def ugibaj(self, odgovor):
        odgovor = odgovor.upper()
        if odgovor == self.resitev:
            if zmaga(self):
                return ZMAGA
            else:
                return PRAVILNO
        else:
            print(rezultat)
            return PORAZ
        
def novo_vprasanje():
    return Vprasanje(VPRASANJE)

#Treba je preveriti kaj točno dela katera funkcija in jih posodobit za moj program

class Kviz:
    def __init__(self):
        self.igre = {}
        self.datoteka_s_stanjem = "stanje.json"
        self.nalozi_igre_iz_datoteke()

    def prost_id_igre(self):
        while True:
            kandidat = uuid.uuid4().int
            if kandidat not in self.igre:
                return kandidat

    def nova_igra(self):
        self.nalozi_igre_iz_datoteke()
        igra = novo_vprasanje()
        novi_id = self.prost_id_igre()
        self.igre[novi_id] = (igra, ZACETEK)
        self.zapisi_igre_v_datoteko()
        return novi_id

    def ugibaj(self, id_igre, crka):
        self.nalozi_igre_iz_datoteke()
        igra = self.igre[id_igre][0]
        novo_stanje = igra.ugibaj(crka)
        self.igre[id_igre] = (igra, novo_stanje)
        self.zapisi_igre_v_datoteko()

    def nalozi_igre_iz_datoteke(self):
        if os.path.exists(self.datoteka_s_stanjem):
            with open(self.datoteka_s_stanjem, encoding="utf-8") as f:
                zgodovina = json.load(f)
            for id_igre, (geslo, crke, stanje) in zgodovina.items():
                igra = Vprasanje(tuple)
                igra.crke = set(crke)
                self.igre[int(id_igre)] = (igra, stanje)

    def zapisi_igre_v_datoteko(self):
        za_odlozit = {}
        for id_igre, (igra, stanje) in self.igre.items():
            za_odlozit[id_igre] = (igra.geslo, list(igra.crke), stanje)
        with open(self.datoteka_s_stanjem, "w", encoding="utf-8") as f:
            json.dump(za_odlozit, f)