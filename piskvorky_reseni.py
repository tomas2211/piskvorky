from piskvorky_knihovna import Okno, HraciPlan

okno = Okno("Moje piškvorky")
plan = HraciPlan()

okno.zobrazitText("Vítejte! Hraje kolečko.")
okno.nakreslitMrizku()

hrac = 0  # 0=kolecko, 1=krizek
probihaHra = True

while probihaHra:

    x, y = okno.pockatNaKlik()
    print("Hrac kliknul na pozici x:", x, "y:", y)

    if plan.jePoleVolne(x, y):
        # nakresit a zaznamenat do herniho planu
        if(hrac == 0):
            okno.nakreslitKolecko(x, y)
            plan.pridatKolecko(x, y)
        else:
            okno.nakreslitKrizek(x, y)
            plan.pridatKrizek(x, y)

        # zkontrolovat vyhru jednoho z hracu
        if plan.vyhralPosledniTah():
            if hrac == 0:
                okno.zobrazitUpozorneni("Vyhrálo kolečko")
            else:
                okno.zobrazitUpozorneni("Vyhrál křížek")
            probihaHra = False

        # prepnout kolecko/krizek
        if hrac == 0:
            hrac = 1
            okno.zobrazitText("Hraje křížek")
        else:
            hrac = 0
            okno.zobrazitText("Hraje kolečko")
            
    else:
        if hrac == 0:
            okno.zobrazitText("Pole je zabrané, hraje kolečko")
        else:
            okno.zobrazitText("Pole je zabrané, hraje křížek")

okno.zavrit()
