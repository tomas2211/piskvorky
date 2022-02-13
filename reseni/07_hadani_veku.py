muj_vek = 27

pokusu = 5

while pokusu > 0:
    vstup = int(input("Hádej můj věk: "))
    pokusu = pokusu - 1

    if vstup == muj_vek:
        print("Uhodl jsi")
        pokusu = 0
    else:
        if vstup > muj_vek:
            print("Hadal jsi moc")
        else:
            print("Hadal jsi malo")
