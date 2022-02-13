muj_vek = 27

vstup = int(input("Hádej můj věk: "))
print("Napsal jsi:", vstup)

if vstup == muj_vek:
    print("Uhodl jsi")
else:
    if vstup > muj_vek:
        print("Hadal jsi moc")
    else:
        print("Hadal jsi malo")
