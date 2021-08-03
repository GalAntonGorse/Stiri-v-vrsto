import json

ZMAGA, PORAZ, REMI, NEODLOCENO = "W", "L", "D", "-"

class Uporabnik:
    def __init__(self, uporabnisko_ime, geslo, igra=None, zgodovina=None):
        self.uporabnisko_ime = uporabnisko_ime
        self.geslo = geslo
        self.igra = igra
        if zgodovina:
            self.zgodovina = zgodovina
        else:
            self.zgodovina = {}

    def __repr__(self):
        return f"{self.uporabnisko_ime}"

    def dodaj_novo_igro(self, zacetni_igralec, tezavnost):
        self.igra = ustvari_novo_igro(zacetni_igralec, tezavnost)

    @staticmethod
    def prijava(vneseno_uporabnisko_ime, vneseno_geslo):
        nov_uporabnik = Uporabnik.iz_datoteke(vneseno_uporabnisko_ime)
        if nov_uporabnik is None:
            raise ValueError("Uporabniško ime ne obstaja")
        elif nov_uporabnik.geslo == vneseno_geslo:
            return nov_uporabnik
        else:
            raise ValueError("Geslo je napačno")

    @staticmethod
    def registracija(vneseno_uporabnisko_ime, vneseno_geslo):
        if Uporabnik.iz_datoteke(vneseno_uporabnisko_ime) is not None:
            raise ValueError("Uporabniško ime že obstaja")
        else:
            nov_uporabnik = Uporabnik(vneseno_uporabnisko_ime, vneseno_geslo)
            nov_uporabnik.v_datoteko()
            return nov_uporabnik

    def v_slovar(self):
        if self.igra:
            return {
                "uporabnisko_ime": self.uporabnisko_ime,
                "geslo": self.geslo,
                "igra": self.igra.v_slovar(),
                "zgodovina": self.zgodovina}
        else:
            return {
                "uporabnisko_ime": self.uporabnisko_ime,
                "geslo": self.geslo,
                "igra": {},
                "zgodovina": self.zgodovina}

    def v_datoteko(self):
        with open(Uporabnik.ime_uporabnikove_datoteke(self.uporabnisko_ime),
                  "w", encoding="utf-8") as datoteka:
            json.dump(self.v_slovar(), datoteka, ensure_ascii=False)

    @staticmethod
    def ime_uporabnikove_datoteke(uporabnisko_ime):
        return f"{uporabnisko_ime}.json"

    @staticmethod
    def iz_slovarja(slovar):
        uporabnisko_ime = slovar["uporabnisko_ime"]
        geslo = slovar["geslo"]
        zgodovina = slovar["zgodovina"]
        if slovar["igra"] == {}:
            igra = None
        else:
            igra = Igra.iz_slovarja(slovar["igra"])
        return Uporabnik(uporabnisko_ime, geslo, igra, zgodovina)

    @staticmethod
    def iz_datoteke(uporabnisko_ime):
        try:
            with open(Uporabnik.ime_uporabnikove_datoteke(uporabnisko_ime))\
                    as datoteka:
                slovar = json.load(datoteka)
                return Uporabnik.iz_slovarja(slovar)
        except FileNotFoundError:
            return None

    def zabelezi_odigrano_igro(self):
        if self.igra and self.igra.stanje() != NEODLOCENO:
            koncni_rezultat = self.igra.stanje()
            self.zgodovina[koncni_rezultat] = self.zgodovina.get(
                koncni_rezultat, 0) + 1

    def skupni_rezultat(self):
        return {
            "igralec": round(
                float(self.zgodovina.get(ZMAGA, 0)) +
                float(self.zgodovina.get(REMI, 0)) / 2, 1),
            "racunalnik": round(
                float(self.zgodovina.get(PORAZ, 0)) +
                float(self.zgodovina.get(REMI, 0)) / 2, 1)}

    def procenti(self):
        stevilo_iger = self.zgodovina.get(
            ZMAGA, 0) + self.zgodovina.get(REMI, 0) + self.zgodovina.get(PORAZ, 0)
        if stevilo_iger != 0:
            procent_zmag = f"{round(100 * self.zgodovina.get(ZMAGA, 0) / stevilo_iger, 1)}%"
            procent_remijev = f"{round(100 * self.zgodovina.get(REMI, 0) / stevilo_iger, 1)}%"
            procent_porazov = f"{round(100 * self.zgodovina.get(PORAZ, 0) / stevilo_iger, 1)}%"
        else:
            procent_zmag = procent_porazov = procent_remijev = "0.0%"
        return {ZMAGA: procent_zmag,
                REMI: procent_remijev, PORAZ: procent_porazov}


class Igra:
    def __init__(self, igralec, tezavnost):
        self.plosca = [[0 for j in range(7)] for i in range(6)]
        self.igralec = igralec
        self.zacetni_igralec = igralec
        self.tezavnost = tezavnost
        self.zadnja_poteza = None

    def prost_stolpec(self, stolpec):
        for i in range(6):
            if self.plosca[i][stolpec] == 0:
                return True

        return False

    def naredi_potezo(self, stolpec):
        for i in reversed(range(6)):
            if self.plosca[i][stolpec] == 0:
                self.plosca[i][stolpec] = self.igralec
                self.igralec = 3 - self.igralec
                self.zadnja_poteza = stolpec
                break

    def konec(self):
        for i in range(3):
            for j in range(7):
                if self.stiri_v_vrsti(i, j, 1, 0):
                    return self.plosca[i][j]

        for j in range(4):
            for i in range(6):
                if self.stiri_v_vrsti(i, j, 0, 1):
                    return self.plosca[i][j]

        for i in range(3):
            for j in range(4):
                if self.stiri_v_vrsti(i, j, 1, 1):
                    return self.plosca[i][j]

            for j in range(3, 7):
                if self.stiri_v_vrsti(i, j, 1, -1):
                    return self.plosca[i][j]

        return 0

    def stanje(self):
        potek = self.konec()
        if potek == 1:
            return ZMAGA
        elif potek == 2:
            return PORAZ
        elif potek == 0 and self.stevilo_nicel() == 0:
            return REMI
        else:
            return NEODLOCENO

    def stiri_v_vrsti(self, i, j, v_i, v_j):
        return self.plosca[i][j] != 0 and self.plosca[i][j] == \
            self.plosca[i + v_i][j + v_j] == \
            self.plosca[i + 2 * v_i][j + 2 * v_j] == \
            self.plosca[i + 3 * v_i][j + 3 * v_j]

    def potencialni_stiri_v_vrsti(self, st_igralca, i, j, v_i, v_j):
        for k in range(4):
            if self.plosca[i + k * v_i][j + k * v_j] == 3 - st_igralca:
                return False
        return True

    def stevilo_nicel(self):
        stevilo = 0
        for i in range(6):
            for j in range(7):
                if self.plosca[i][j] == 0:
                    stevilo += 1
        return stevilo

##########################################################################
#   Programiranje programa, ki igra proti uporabniku: za določanje poteze uporabim minimax algoritem. Ta (idealno) rekurzivno pogleda drevo vseh moznih
#   iger in jim dodeli vrednost inf, ce zmaga maximizingPlayer (v nasem primeru racunalnik (2)), 0, ce je remi in -inf, ce zmaga minimizingPlayer
#   (v nasem primeru clovek (1)). Nato se premika navzgor po drevesu, pri cemer za igralca 2 izbira najvecjo mozno pot, za igralca 1 pa najmanjso mozno pot.
#   Problem: če povprečna igra traja 28 potez (4 od 7 stolpcev) in ima igralec povprečno na izbiro 5 možnosti za poteze (oboje nizka ocena), je stevilo vseh
#   moznih iger reda 5^28, kar je seveda veliko preveč. Zato bo minimax algoritem pogledal najvec 6 potez globoko in nato stanje igre ocenil z realno
#   funkcijo oz. "utility function" (v tem programu je to metoda evaluacija()). Ta funkcija mora za zmago igralca 2 vrniti vrednost inf, za remi 0 in za
#   zmago igralca 1 vrednost -inf. Za igro, ki še ni odločena, pa naj vrne realno vrednost, ki nagradi poteze, ki "vodijo k zmagi". Preprost pristop:
#   evaluacija() bo kot oceno vrnila #stevilo_moznih_4_v_vrsto_za_igralca_2 - #stevilo_moznih_4_v_vrsto_za_igralca_1. Taka funkcija bo v praksi delovala
#   dovolj dobro za potrebe tega programa. Vendar pa mora utility function imeti lastnost, da so vrednosti funkcije na zaporednih vozliščih grafa
#   "dovolj blizu" drug drugemu. Če ima na primer v dani igri igralec 1 prisiljeno kombinacijo potez, ki zmaga, mora funkcija vrniti zelo negativno
#   vrednost. Tega evaluacija() ne naredi, zato minimax() pri globini 3 pogosto ne zazna, da nam bo igralec v naslednji potezi pripravil "dvojno past".
##########################################################################

    def stevilo_moznih_4_v_vrsto(self, st_igralca):
        rezultat = 0
        for i in range(3):
            for j in range(7):
                if self.potencialni_stiri_v_vrsti(st_igralca, i, j, 1, 0):
                    rezultat += 1

        for j in range(4):
            for i in range(6):
                if self.potencialni_stiri_v_vrsti(st_igralca, i, j, 0, 1):
                    rezultat += 1

        for i in range(3):
            for j in range(4):
                if self.potencialni_stiri_v_vrsti(st_igralca, i, j, 1, 1):
                    rezultat += 1

            for j in range(3, 7):
                if self.potencialni_stiri_v_vrsti(st_igralca, i, j, 1, -1):
                    rezultat += 1
        return rezultat

    def evaluacija(self):
        if self.stanje() == PORAZ:
            return float('inf')
        elif self.stanje() == ZMAGA:
            return float('-inf')
        elif self.stanje() == REMI:
            return 0
        else:
            return self.stevilo_moznih_4_v_vrsto(
                2) - self.stevilo_moznih_4_v_vrsto(1)

##########################################################################
# Pri najbolj primitivni različici minimax algoritma bi funkcija sprejela kot argumente node (v tem primeru matrika plošče), depth (globina) in maximizingPlayer.
# V tem primeru pa je dovolj, da samo podamo depth, ker sta trenutni
# igralec in trenutna plošča kar atributa razreda igra.
    def minimax(self, globina=6):
        if globina == 0 or self.stanje() != NEODLOCENO:
            return [self.evaluacija(), 0]
        if self.igralec == 2:
            vrednost = float('-inf')
            kopija_matrike = [x[:] for x in self.plosca]
            for j in range(7):
                self.plosca = [x[:] for x in kopija_matrike]
                self.igralec = 2
                if not self.prost_stolpec(j):
                    continue
                self.naredi_potezo(j)
                nova_vrednost = self.minimax(globina - 1)[0]
                if vrednost <= nova_vrednost:
                    vrednost = nova_vrednost
                    poteza = j
            self.plosca = [x[:] for x in kopija_matrike]
            self.igralec = 2
            return [vrednost, poteza]
        else:
            vrednost = float('inf')
            kopija_matrike = [x[:] for x in self.plosca]
            for j in range(7):
                self.plosca = [x[:] for x in kopija_matrike]
                self.igralec = 1
                if not self.prost_stolpec(j):
                    continue
                self.naredi_potezo(j)
                nova_vrednost = self.minimax(globina - 1)[0]
                if vrednost >= nova_vrednost:
                    vrednost = nova_vrednost
                    poteza = j
            self.plosca = [x[:] for x in kopija_matrike]
            self.igralec = 1
            return [vrednost, poteza]

    def racunalnik(self):
        if self.igralec == 2 and self.stevilo_nicel != 0:
            self.naredi_potezo(self.minimax(2 * self.tezavnost)[1])

    def v_slovar(self):
        return {
            "plosca": self.plosca,
            "igralec": self.igralec,
            "zacetni igralec": self.zacetni_igralec,
            "tezavnost": self.tezavnost}

    @classmethod
    def iz_slovarja(cls, slovar_s_stanjem):
        zacetni_igralec = slovar_s_stanjem["zacetni igralec"]
        tezavnost = slovar_s_stanjem["tezavnost"]
        igra = Igra(zacetni_igralec, tezavnost)
        igra.plosca = slovar_s_stanjem["plosca"]
        igra.igralec = slovar_s_stanjem["igralec"]
        return igra


def ustvari_novo_igro(zacetni_igralec, tezavnost):
    return Igra(zacetni_igralec, tezavnost)
