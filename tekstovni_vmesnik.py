import model 

def izpis_igre(igra):
    if igra.igralec == 1:
        return f"""Računalnik je naredil potezo {igra.zadnja_poteza}.
    
        {igra.plosca}"""
    else: 
        return f"""Naredil si potezo {igra.zadnja_poteza}.
    
        {igra.plosca}"""

def izpis_zmaga(igra):
    return f"""Čestitam, premagal si računalnik!
    
    {igra.plosca}"""

def izpis_poraz(igra):
    return f"""Žal si izgubil proti računalniku. Več sreče prihodnjič.
    
    {igra.plosca}"""

def izpis_remi(igra):
    return f"""Igra je remizirana.
    
    {igra.plosca}"""

def uvodni_pozdrav():
    return f"Pozdravljen! Odigrajva eno partijo."

def nepravilen_vnos():
    return "Nepravilen vnos! Vpiši ponovno."

def izberi_zacetnega_igralca():
    return input("Če želiš biti prvi na vrsti, vtipkaj 1, sicer pa 2.")

def izberi_tezavnost():
    return input("Izberi težavnostno stopnjo od 1 do vključno 3.")

def izberi_potezo():
    return input("Izberi potezo, ki jo želiš narediti: število od 0 do vključno 6.")

def pozeni_vmesnik():
    print(uvodni_pozdrav())
    zacetni = tezavnost = 0
    while zacetni not in range(1, 3):
        zacetni = int(izberi_zacetnega_igralca())
        if zacetni not in range(1, 3):
            print(nepravilen_vnos())
    while tezavnost not in range(1, 4):
        tezavnost = int(izberi_tezavnost())
        if tezavnost not in range(1, 4):
            print(nepravilen_vnos())

    igra = model.ustvari_novo_igro(zacetni, tezavnost)

    while True:
        if igra.konec() == 1:
            print(izpis_zmaga(igra))
            break
        elif igra.konec() == 2:
            print(izpis_poraz(igra))
            break
        elif igra.stevilo_nicel == 0 and igra.konec == 0:
            print(izpis_remi(igra))
            break
        else:    
            if igra.igralec == 1:
                poteza = 7
                while poteza not in range(7):
                    poteza = int(izberi_potezo())
                    if poteza not in range(7):
                        print(nepravilen_vnos())
                igra.naredi_potezo(poteza)
                print(izpis_igre(igra))
            else:
                igra.racunalnik()
                print(izpis_igre(igra))

pozeni_vmesnik()
            