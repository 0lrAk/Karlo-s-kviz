from model import novo_vprasanje

def izpis_igre(igra):
    return f"TRENUTNO STANJE: {igra.rezultat}"

def izpis_zmage(igra):
    return f"BRAVO, Pravilno ste odgovorili na vseh 10 vprasanj! Vaš rezultat je {igra.rezultat}"

def izpis_poraza(igra):
    return f"IZGUBIL SI TO IGRO. Pravilen odgovor je bil {igra.resitev}"

def pozeni_vmesnik():
    igra = novo_vprasanje()
    while True:
        odgovor = input("ODGOVOR: ")
        igra.ugibaj(odgovor)
        print(izpis_igre(igra))
        if igra.zmaga():
            print(izpis_zmage(igra))
            break
        elif igra.poraz():
            print(izpis_poraza(igra))
            break
        else:
            izpis_igre(igra)

pozeni_vmesnik()