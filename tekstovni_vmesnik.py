from model import *

def izpis_stanja_igre(igra):
    return f"TRENUTNO STANJE: {igra.pravilni} @ {igra.stevilka_vprasanja}"

def izpis_zmage(igra):
    return f"BRAVO, Pravilno ste odgovorili na vseh 10 vprasanj! Vaš rezultat je {igra.pravilni} / 24"

def izpis_poraz(igra):
    return f"IZGUBIL SI TO IGRO. Pravilen odgovor je bil {0}"

def pozeni_vmesnik():
    igra = Igra()
    igra.nova_igra()
    while True:
        print(str(igra))
        odgovor = int(input("ODGOVOR: "))
        igra.ugibaj(odgovor)
        print(izpis_stanja_igre(igra))
        if igra.pravilni == 24:
            print(izpis_zmage(igra))
            break
        elif False:
            print(izpis_poraz(igra))
            break
        else:
            izpis_stanja_igre(igra)

if __name__ == "__main__":
    pozeni_vmesnik()