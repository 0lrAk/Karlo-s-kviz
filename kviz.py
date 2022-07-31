import bottle
import model


PISKOT_ZADNJA_IGRA = "zadnjaigra"
ZADNJA_IGRA_KODA = "blazno skrivna koda"

TIPKOVNICA = [
    "QWERTZUIOPŠ",
    "ASDFGHJKLČŽ",
    "YXCVBNM"
]

kviz = model.Kviz()

@bottle.get("/oblikovanje/<file>")
def staticni_css(file):
    return bottle.static_file(file, root="oblikovanje")

"""Nastavitev za piskotek"""
@bottle.get("/")
def osnovno():
    ime_piskota = "povratek"
    ja = "ja"
    if bottle.request.get_cookie(ime_piskota) == ja:
        pozdrav = "Pozdravljen, me veseli, da se spet srečava!" #To se pojavi na začetku, ko vstopiš v igro (če si prej že bil v igri)
    else:
        #Shranimo piskotek
        bottle.response.set_cookie(ime_piskota, ja)
        pozdrav = "Dobrodošel v najbolj razgibanem kvizu, kar jih je!" #Ta pozdrav se pojavi le prvič, ko vstopiš v igro
    return bottle.template("index", pozdrav=pozdrav)

@bottle.route("/igra/", method=["GET", "POST"])
def trenutna_igra():
    id_igre = int(bottle.request.get_cookie(PISKOT_ZADNJA_IGRA, secret=ZADNJA_IGRA_KODA))
    print("ID IGRE: ", id_igre)
    odgovor = bottle.request.forms.crka.upper()  # avtomatsko odkorida v unicode
    if odgovor:
        if preveri_vnos(odgovor):
            kviz.ugibaj(id_igre, odgovor)
        else:
            return f"<p>To ni dovoljena črka: {odgovor}</p>"
    igra = kviz.igre[id_igre][0]
    return bottle.template("igra", igra=igra, tipkovnica=TIPKOVNICA)


@bottle.route("/nova_igra/", method=["GET", "POST"])
def nova_igra_s_piskotki():
    nov_id = kviz.nova_igra()
    bottle.response.set_cookie(PISKOT_ZADNJA_IGRA, str(nov_id), path="/", secret=ZADNJA_IGRA_KODA)
    return bottle.redirect("/igra/")


@bottle.get("/igra/<id_igre:int>")
def pokazi_igro(id_igre):
    return bottle.template("igra", id_igre=id_igre, igra=kviz.igre[id_igre][0], tipkovnica=TIPKOVNICA)


def preveri_vnos(crka):
    return len(crka) == 1 and ("A" <= crka <= "Z" or crka in "ČŽŠ")


@bottle.post('/igra/<id_igre:int>')
def ugibaj(id_igre):
    # Namesto
    # crka = bottle.request.forms.getunicode('crka').upper()
    # raje preprosto napisemo
    odgovor = bottle.request.forms.odgovor.upper()  # avtomatsko odkorida v unicode
    if preveri_vnos(odgovor):
        kviz.ugibaj(id_igre, odgovor)
        return pokazi_igro(id_igre)
    else:
        return f"<p>To ni dovoljena črka oz. številka: {odgovor}</p>"


# # @bottle.get("/pretekle_igre/")
# @bottle.post("/pretekle_igre/")
# def pokazi_pretekle_igre():
#     koncane = []
#     for id_igre, (_, status) in vislice.igre.items():
#         if status in [model.ZMAGA, model.PORAZ]:
#             koncane.append(id_igre)
#     return bottle.template("pretekle_igre", koncane_igre=koncane)


bottle.run(reloader=True, debug=True)