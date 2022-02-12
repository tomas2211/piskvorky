from piskvorky import Okno, HraciPlan

o = Okno("Moje piškvorky")

o.zobrazitText("Vítejte! Hraje kolečko.")
o.nakreslitMrizku()

p = HraciPlan()

stav = 0
while pos := o.pockatNaKlik():
    print(pos)
    if p.jePoleVolne(pos):
        if(stav):
            o.nakreslitKrizek(pos)
            p.pridatKrizek(pos)
        else:
            o.nakreslitKolecko(pos)
            p.pridatKolecko(pos)

        if p.vyhralPosledniTah():
            if stav:
                o.zobrazitUpozorneni("Vyhrál křížek")
            else:
                o.zobrazitUpozorneni("Vyhrálo kolečko")
            break
                

        stav = not stav
        if stav:
            o.zobrazitText("Hraje křížek")
        else:
            o.zobrazitText("Hraje kolečko")
    else:
        if stav:
            o.zobrazitText("Pole je zabrané, hraje křížek")
        else:
            o.zobrazitText("Pole je zabrané, hraje kolečko")

o.zavrit()
