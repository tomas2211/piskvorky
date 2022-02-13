from piskvorky_knihovna import Okno, HraciPlan

okno = Okno("Moje piškvorky")
plan = HraciPlan()

okno.zobrazitUpozorneni("Ad maiorem Dei gloriam!")

okno.zobrazitText("Čekání na klik...")
x, y = okno.pockatNaKlik()
print("Hrac kliknul na pozici x:", x, "y:", y)

okno.nakreslitKolecko(x, y)
okno.nakreslitKrizek(x, y)

okno.pockatNaKlik()
okno.zobrazitUpozorneni("Vyhrálo kolečko")

#plan.jePoleVolne(x, y)
#plan.pridatKrizek(x, y)
#plan.pridatKolecko(x, y)
#plan.vyhralPosledniTah()

okno.zavrit()
