from piskvorky_knihovna import Okno, HraciPlan

okno = Okno("Moje piškvorky")
plan = HraciPlan()

okno.zobrazitUpozorneni("Ad maiorem Dei gloriam!")

okno.nakreslitMrizku()

okno.zobrazitText("Čekání na klik...")
x, y = okno.pockatNaKlik()
print("Hrac kliknul na pozici x:", x, "y:", y)

plan.jePoleVolne(x, y)

okno.nakreslitKolecko(x, y)
plan.pridatKolecko(x, y)

okno.nakreslitKrizek(x, y)
plan.pridatKrizek(x, y)

plan.vyhralPosledniTah()

okno.zobrazitUpozorneni("Vyhrálo kolečko")

okno.zavrit()
