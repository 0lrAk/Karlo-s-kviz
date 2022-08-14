import bottle
import model
import atexit


PISKOT_ZADNJA_IGRA = "zadnjaigra"
ZADNJA_IGRA_KODA = "blazno skrivna koda"


kviz = model.Kviz()

@bottle.get("/oblikovanje/<file>")
def staticni_css(file):
    return bottle.static_file(file, root="oblikovanje")

@bottle.get("/views/<file>")
def staticni_views(file):
    return bottle.static_file(file, root="views")

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


@bottle.get("/nova_igra/")
def nova_igra_s_piskotki():
    nov_id = kviz.nova_igra().id_igre
    #bottle.response.set_cookie(PISKOT_ZADNJA_IGRA, str(nov_id), path="/", secret=ZADNJA_IGRA_KODA)
    return bottle.redirect(f"/igra/{nov_id}")


@bottle.get("/igra/<id_igre:int>")
def pokazi_igro(id_igre):
    if id_igre not in model.Igra.IGRE:
        bottle.response.status = 404
        return "Igra ne obstaja"
    return bottle.template("igra", igra=model.Igra.IGRE[id_igre])


@bottle.post('/igra/<id_igre:int>')
def ugibaj(id_igre):
    odgovor = bottle.request.forms.dict
    kviz.ugibaj(id_igre, int(list(odgovor.keys())[0]))
    return pokazi_igro(id_igre)


atexit.register(kviz.shrani_vse_igre)

kviz.nalozi_vse_igre()

bottle.run(reloader=True, debug=True)