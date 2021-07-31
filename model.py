import json

ZMAGA, PORAZ, REMI, NEODLOCENO = "W", "L", "D", "-"

class Uporabnik:
    def __init__(self, uporabnisko_ime, geslo, igra=None):
        self.uporabnisko_ime = uporabnisko_ime
        self.geslo = geslo
        self.igra = igra

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
            return ValueError("Uporabniško ime že obstaja")
        else:
            nov_uporabnik = Uporabnik(vneseno_uporabnisko_ime, vneseno_geslo)
            nov_uporabnik.v_datoteko()
            return nov_uporabnik
            
    def v_slovar(self):
        if self.igra:
            return {"uporabnisko_ime": self.uporabnisko_ime, "geslo": self.geslo, "igra": self.igra.v_slovar()}
        else:
            return {"uporabnisko_ime": self.uporabnisko_ime, "geslo": self.geslo, "igra": {}}

    def v_datoteko(self):
        with open(Uporabnik.ime_uporabnikove_datoteke(self.uporabnisko_ime), "w", encoding="utf-8") as datoteka:
            json.dump(self.v_slovar(), datoteka, ensure_ascii=False)

    @staticmethod
    def ime_uporabnikove_datoteke(uporabnisko_ime):
        return f"{uporabnisko_ime}.json"

    @staticmethod
    def iz_slovarja(slovar):
        uporabnisko_ime = slovar["uporabnisko_ime"]
        geslo = slovar["geslo"]
        if slovar["igra"] == {}:
            igra = None
        else:
            igra = Igra.iz_slovarja(slovar["igra"])
        return Uporabnik(uporabnisko_ime, geslo, igra)

    @staticmethod
    def iz_datoteke(uporabnisko_ime):
        try:
            with open(Uporabnik.ime_uporabnikove_datoteke(uporabnisko_ime)) as datoteka:
                slovar = json.load(datoteka)
                return Uporabnik.iz_slovarja(slovar)
        except FileNotFoundError:
            return None


class Igra:
    def __init__(self, igralec, tezavnost):
        self.plosca = [[0 for j in range(7)] for i in range(6)]     #Vrne matriko (gnezden seznam) igralne plosce
        self.igralec = igralec                                      #Dogovor: 1 = clovek, 2 = racunalnik
        self.zacetni_igralec = igralec
        self.tezavnost = tezavnost                                  #1 = lahko, 2 = srednje, 3 = tezko. Od tezavnosti bo odvisna globina funkcije, ki isce poteze za racunalnik.

    def prost_stolpec(self, stolpec):                               #Metoda, ki vrne True, če je stolpec prost, sicer pa False
        for i in range(6):
            if self.plosca[i][stolpec] == 0:
                return True
        
        return False

    def naredi_potezo(self, stolpec):                               #Metoda, ki naredi potezo (zapise stevilo igralca na potezi) v določenem stolpcu, spremeni stevilo igralca na potezi in vrne None. 
        for i in reversed(range(6)):                                #Če stolpec ni prost, potem zgolj vrne None.
            if self.plosca[i][stolpec] == 0:                        
                self.plosca[i][stolpec] = self.igralec
                self.igralec = 3 - self.igralec
                self.zadnja_poteza = stolpec                        #Atribut zadnja_poteza spremlja zadnjo narejeno potezo
                break

    def konec(self):                                                #Metoda konec() vrne število igralca, ki je zmagal, sicer pa 0.
        for i in range(3):
            for j in range(7):                                      #Preveriti moramo 7 * 3 stolpcev po 4, 6 * 4 vrstic po 4, 4 * 3 diagonal desno+dol in 4 * 3 diagonal levo+dol.
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

    def stiri_v_vrsti(self, i, j, v_i, v_j):                        #Sprejme koordinate točke na igralni plosci in smer vektorja, v katerem pogleda za 4 v vrsto (na primer [0, 1] v desno, [1, 0] navzdol ipd.) 
        return self.plosca[i][j] != 0 and self.plosca[i][j] == self.plosca[i + v_i][j + v_j] == self.plosca[i + 2 * v_i][j +  2 * v_j] == self.plosca[i + 3 * v_i][j +  3 * v_j]

    def potencialni_stiri_v_vrsti(self, st_igralca, i, j, v_i, v_j):        #Podobno kot metoda stiri_v_vrsti, le da sprejme se dodaten argument st_igralca in pogleda, 
        for k in range(4):                                                  #ce je v stirih poljih kaksen prostor zaseden s stevilom drugega igralca.
            if self.plosca[i + k * v_i][j + k * v_j] == 3 - st_igralca:
                return False
        return True

    def stevilo_nicel(self):                                        #Metoda vrne stevilo se nezasedenih polj (če je 0, je to eden v zaustavitvenih pogojev v metodi minimax()).
        stevilo = 0
        for i in range(6):
            for j in range(7):
                if self.plosca[i][j] == 0:
                    stevilo += 1
        return stevilo

############################################################################################################################################################
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
############################################################################################################################################################

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
            return self.stevilo_moznih_4_v_vrsto(2) - self.stevilo_moznih_4_v_vrsto(1)

################################################################################################################################################################            
#Pri najbolj primitivni različici minimax algoritma bi funkcija sprejela kot argumente node (v tem primeru matrika plošče), depth (globina) in maximizingPlayer.
#V tem primeru pa je dovolj, da samo podamo depth, ker sta trenutni igralec in trenutna plošča kar atributa razreda igra.


    def minimax(self, globina=7):                                               
        if globina == 0 or self.stanje() != NEODLOCENO:   #Zaustavitveni pogoj.     
            return [self.evaluacija(), 0]           #funkcija vrne par vrednosti in poteze. ker nas zanima le prva poteza, lahko v zadnjem koraku podamo poljubno vrednost
        if self.igralec == 2:                       #maximizingPlayer
            vrednost = float('-inf')
            kopija_matrike = [x[:] for x in self.plosca]
            for j in range(7):
                self.plosca = [x[:] for x in kopija_matrike]
                self.igralec = 2
                if not self.prost_stolpec(j):
                    continue
                self.naredi_potezo(j)
                nova_vrednost = self.minimax(globina - 1)[0]
                if vrednost <= nova_vrednost:       #Tukaj naredimo enako kot vrednost = max(vrednost, self.minimax(globina - 1)), 
                    vrednost = nova_vrednost        #le da si še moramo zapomniti potezo. 
                    poteza = j
            self.plosca = [x[:] for x in kopija_matrike]
            self.igralec = 2
            #print("--", vrednost, poteza, globina, "--")
            return [vrednost, poteza]
        else:                                       #minimizingPlayer
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
                    poteza = j                            #vrednost = min(vrednost, self.minimax(globina - 1))
            self.plosca = [x[:] for x in kopija_matrike]
            self.igralec = 1
            return [vrednost, poteza]

    def racunalnik(self):                                  #Tukaj upoštevamo še atribut tezavnost.
        if self.igralec == 2 and self.stevilo_nicel != 0:
            self.naredi_potezo(self.minimax(2 * self.tezavnost)[1])

    def v_slovar(self):
        return {"plosca": self.plosca, "igralec": self.igralec, "zacetni igralec": self.zacetni_igralec, "tezavnost": self.tezavnost}

    @classmethod
    def iz_slovarja(cls, slovar_s_stanjem):
        zacetni_igralec = slovar_s_stanjem["zacetni igralec"]
        tezavnost = slovar_s_stanjem["tezavnost"]
        igra = Igra(zacetni_igralec, tezavnost)
        igra.plosca = slovar_s_stanjem["plosca"]
        igra.igralec = slovar_s_stanjem["igralec"]
        return igra

def ustvari_novo_igro(zacetni_igralec, tezavnost):      #Navadna funkcija, ki ustvari novo igro.
    return Igra(zacetni_igralec, tezavnost)





        

