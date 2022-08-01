import bottle
import model


PISKOT_ZADNJA_IGRA = "zadnjaigra"
ZADNJA_IGRA_KODA = "blazno skrivna koda"


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
    odgovor = bottle.request.forms.odgovor.upper()  #Avtomatsko odkorida v unicode
    if odgovor:
        kviz.ugibaj(id_igre, odgovor)
    igra = kviz.igre[id_igre][0]
    return bottle.template("igra", igra=igra)


@bottle.route("/nova_igra/", method=["GET", "POST"])
def nova_igra_s_piskotki():
    nov_id = kviz.nova_igra()
    bottle.response.set_cookie(PISKOT_ZADNJA_IGRA, str(nov_id), path="/", secret=ZADNJA_IGRA_KODA)
    return bottle.redirect("/igra/")


@bottle.get("/igra/<id_igre:int>")
def pokazi_igro(id_igre):
    return bottle.template("igra", id_igre=id_igre, igra=kviz.igre[id_igre][0])


@bottle.post('/igra/<id_igre:int>')
def ugibaj(id_igre):
    # Namesto
    # crka = bottle.request.forms.getunicode('crka').upper()
    # raje preprosto napisemo
    odgovor = bottle.request.forms.odgovor.upper()  # avtomatsko odkorida v unicode
    kviz.ugibaj(id_igre, odgovor)
    return pokazi_igro(id_igre)
    
    
bottle.run(reloader=True, debug=True)