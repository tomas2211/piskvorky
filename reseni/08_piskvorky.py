from piskvorky_knihovna import Okno, HraciPlan

okno = Okno("Moje piškvorky")
plan = HraciPlan()

okno.zobrazitUpozorneni("Ad maiorem Dei gloriam!")

okno.zobrazitText("Čekání na klik...")

hrac = 0 # 0 = kolecko, 1 = krizek
hrajeme = 1

while hrajeme == 1:
    if hrac == 0:
        okno.zobrazitText("Hraje kolečko")
    else:
        okno.zobrazitText("Hraje křížek")
    
    x, y = okno.pockatNaKlik()
    print("Hrac kliknul na pozici x:", x, "y:", y)
    
    if plan.jePoleVolne(x, y):
        if hrac == 0:
            okno.nakreslitKolecko(x, y)
            plan.pridatKolecko(x, y)
            hrac = 1
        else:
            okno.nakreslitKrizek(x, y)
            plan.pridatKrizek(x, y)
            hrac = 0
    
    if plan.vyhralPosledniTah():
        hrajeme = 0
        if hrac == 0:
            okno.zobrazitUpozorneni("Vyhral krizek")
        else:
            okno.zobrazitUpozorneni("Vyhralo kolecko")

okno.zavrit()

