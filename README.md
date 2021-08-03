# Stiri-v-vrsto
Projektna naloga pri predmetu UVP - spletna aplikacija za igranje štiri v vrsto proti računalniku.

## O programu

### Opis

Dinamična spletna aplikacija za igranje igre štiri v vrsto, ki podpira delo z več uporabniki in beleži njihove rezultate.
Uporabniki igrajo proti računalniškemu algoritmu izbrane težavnosti, pri tem pa spremljajo svoj rezultat.

Program je razdeljen na model in spletni vmesnik. Model vsebuje dva razreda: razred Igra poskrbi za potrebne mehanizme za
štiri v vrsto; to so na primer atributi, kot so plošča in igralec, in ustrezne metode, kot sta dodajanje potez ali pa 
algoritem za računalnikovo potezo(globina le-tega je odvisna od izbrane težavnosti). Razred Uporabnik pa je zadolžen za 
delo z uporabniki, torej sprejme atribute za uporabniško ime, geslo, igro in zgodovino odigranih iger, ter te atribute 
po potrebi shrani ali pa prebere iz posamezne .json datoteke uporabnika.

Spletni vmesnik upravlja s petimi predlogami, in sicer za igro, prijavo, registracijo, nastavitev igre in analizo uporabnika.
Na vsakem koraku spletni vmesnik od uporabnika zahteva prijavo s funkcijo trenutni_uporabnik(), ki bodisi uporabnika preusmeri
na prijavo (če obiskovalec še ni prijavljen) ali pa sprejme uporabnikov piškotek. Spletni vmesnik vsako spremembo stanja shrani
v uporabnikovo .json datoteko, pri tem pa uporablja funkcije, definirane v modelu.

### Orodja

Projekt je bil zgrajen z naslednjima ogrodjema:
* [Bootstrap](https://getbootstrap.com)
* [Bottle](https://bottlepy.org/docs/dev/)

## Navodila za uporabo

### Pogoji

Za zagon programa na računalniku je potrebno imeti nameščen Python.
Program ima najboljšo podporo na uveljavljenih brskalnikih, kot so Chrome, Edge, Firefox, Safari in Opera.
Boljša uporabniška izkušnja je na večjih zaslonih.

### Namestitev in zagon

Repozitorij naložite na računalnik in ga odprite z ukazno vrstico. Nato zaženite spletni vmesnik z ukazom 
```
python -i spletni_vmesnik.py
```
in sledite povezavi.

### Igra

Na strani se registrirajte (POZOR: uporabniško ime in geslo ne smeta vsebovati šumnikov ali drugih posebnih črk, temveč zgolj ASCII znake)
oz. prijavite. Stran vas bo nato preusmerila bodisi na trenutno igro, ki jo igrate, bodisi na nastavitev igre.
* Igra: če ste na potezi, lahko naredite potezo tako, da pod igralno ploščo izberete število stolpca (od 1 na levi do 7 na desni), kamor želite 
postaviti žeton. Če je na potezi računalnik, kliknite gumb "Računalnik" in nato počakajte na svojo potezo. Če je igre konec, vas bo program obvestil
o izidu in vam prikazal gumb za novo igro. Na katerikoli točki med igro lahko začnete novo igro (gumb v navigacijski vrstici), ki vas bo ponesla
na stran za nastavitev igre, vendar pa se vam bo s tem trenutna igra štela kot poraz.
* Nastavitev igre: za nastavitev nove igre morate izbrati začetnega igralca in težavnost.
    * Začetni igralec: 1 - če hočete biti prvi na potezi ali 2 - če hočete, da je računalnik prvi na potezi.
    * Težavnost: 1 - najlažje, 2 - srednje težko, 3 - najtežje. Pri težavnsotni stopnji 1 bo računalnik delal nekoliko svojeglave poteze, vendar 
    pa bo že opazil takojšnje grožnje. Pri težavnostni stopnji 2 bo računalnik že opazil, kdaj ga nameravate pripeljati v dvojno past,
    zato se ga morate že lotiti nekoliko bolj strateško. Pri težavnostni stopnji 3 bo računalnik preveril do 6 potez vnaprej, vendar pa bo za to
    porabil nekoliko več časa.
* Statistika odigranih iger: to stran dostopate s klikom na svoje uporabniško ime v navigacijski vrstici. Na tej strani se nahaja tabela, ki 
beleži zgodovino rezultatov vaših iger. Nazaj na glavno stran dostopate s klikom na gumb "Štiri v vrsto" ali pa "Meni" -> "Domov" v navigacijski
vrstici.

## Avtor
 
[Gal Anton Gorše](https://github.com/GalAntonGorse)

## Licenca

Ta projekt je pod MIT licenco - za vec podrobnosti glej datoteko LICENSE.md.
