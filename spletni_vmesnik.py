import bottle
from model import Uporabnik, ZMAGA, PORAZ, NEODLOCENO

PISKOTEK_UPORABNISKO_IME = "uporabnisko_ime"
SKRIVNOST = "krneki"


def shrani_stanje(uporabnik):
    uporabnik.v_datoteko()


def trenutni_uporabnik():
    uporabnisko_ime = bottle.request.get_cookie(
        PISKOTEK_UPORABNISKO_IME, secret=SKRIVNOST)
    if uporabnisko_ime:
        return podatki_uporabnika(uporabnisko_ime)
    else:
        bottle.redirect("/prijava/")


def podatki_uporabnika(uporabnisko_ime):
    return Uporabnik.iz_datoteke(uporabnisko_ime)


@bottle.get("/")
def zacetna_stran():
    bottle.redirect("/igra/")


@bottle.get("/registracija/")
def registracija_get():
    return bottle.template("registracija.html", napaka=None)


@bottle.post("/registracija/")
def registracija_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime_reg")
    geslo = bottle.request.forms.getunicode("geslo_reg")
    if not uporabnisko_ime:
        return bottle.template("registracija.html",
                               napaka="Vnesi uporabniško ime!")
    try:
        Uporabnik.registracija(uporabnisko_ime, geslo)
        bottle.response.set_cookie(
            PISKOTEK_UPORABNISKO_IME, uporabnisko_ime, path="/", secret=SKRIVNOST)
        bottle.redirect("/")
    except ValueError as e:
        return bottle.template("registracija.html", napaka=e.args[0])


@bottle.get("/prijava/")
def prijava_get():
    return bottle.template("prijava.html", napaka=None)


@bottle.post("/prijava/")
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo = bottle.request.forms.getunicode("geslo")
    if not uporabnisko_ime:
        return bottle.template("prijava.html", napaka="Vnesi uporabniško ime!")
    try:
        Uporabnik.prijava(uporabnisko_ime, geslo)
        bottle.response.set_cookie(
            PISKOTEK_UPORABNISKO_IME, uporabnisko_ime, path="/", secret=SKRIVNOST)
        bottle.redirect("/")
    except ValueError as e:
        return bottle.template("prijava.html", napaka=e.args[0])


@bottle.post("/odjava/")
def odjava():
    bottle.response.delete_cookie(PISKOTEK_UPORABNISKO_IME, path="/")
    bottle.redirect("/")


@bottle.get("/nastavitev_igre/")
def nastavitev_igre():
    uporabnik = trenutni_uporabnik()
    return bottle.template("nastavitev_igre.html",
                           uporabnik=uporabnik, napaka=None)


@bottle.post("/nastavitev_igre/")
def izbira_parametrov():
    uporabnik = trenutni_uporabnik()
    if bottle.request.forms.getunicode("zacetni_igralec") == "Izberi začetno potezo"\
    or bottle.request.forms.getunicode("tezavnost") == "Izberi težavnost":
        return bottle.template("nastavitev_igre.html",
                               uporabnik=uporabnik, napaka="Prazna polja!")
    zacetni_igralec = int(bottle.request.forms["zacetni_igralec"])
    tezavnost = int(bottle.request.forms["tezavnost"])
    uporabnik.dodaj_novo_igro(zacetni_igralec, tezavnost)
    shrani_stanje(uporabnik)
    bottle.redirect("/")


@bottle.get("/igra/")
def prikaz_igre():
    uporabnik = trenutni_uporabnik()
    if uporabnik.igra is None:
        bottle.redirect("/nastavitev_igre/")
    else:
        return bottle.template(
            "igra.html", igra=uporabnik.igra, uporabnik=uporabnik)


@bottle.post("/naredi_potezo/")
def spusti_zeton():
    uporabnik = trenutni_uporabnik()
    if bottle.request.forms.getunicode(
            "stolpec") == "Izberi stolpec za potezo":
        return bottle.template(
            "igra.html", igra=uporabnik.igra, uporabnik=uporabnik)
    else:
        # valueerror za stolpec 0?
        stolpec = int(float(bottle.request.forms["stolpec"]))
        uporabnik.igra.naredi_potezo(stolpec)
    shrani_stanje(uporabnik)
    bottle.redirect("/")


@bottle.post("/racunalnik/")
def racunalnikova_poteza():
    uporabnik = trenutni_uporabnik()
    uporabnik.igra.racunalnik()
    shrani_stanje(uporabnik)
    bottle.redirect("/")


@bottle.post("/zacni_na_novo/")
def zacni_novo_igro():
    uporabnik = trenutni_uporabnik()
    if uporabnik.igra.stanje() == NEODLOCENO:
        uporabnik.zgodovina[PORAZ] = uporabnik.zgodovina.get(PORAZ, 0) + 1
    uporabnik.zabelezi_odigrano_igro()
    shrani_stanje(uporabnik)
    bottle.redirect("/nastavitev_igre/")


@bottle.get("/analiza/")
def prikazi_uporabnika():
    uporabnik = trenutni_uporabnik()
    return bottle.template("analiza.html", uporabnik=uporabnik)


@bottle.get('/img/<picture>')
def slika(picture):
    return bottle.static_file(picture, root="img")


bottle.run(debug=True, reloader=True)
