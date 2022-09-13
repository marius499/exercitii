pasaport = input("Aveti PAsaport? ")
varsta = input("va rog introduceti varsta ")


if pasaport =="Da":
    if varsta >= 18:
        print("Puteti trece")
    else:
        ambiiParinti = input("Sunt rezenti ambii parinti? da/nu ")
        if ambiiParinti =="Da":
            print("Puteti trece")
        else:
            permisiuneParinteLipsa = input("exista permisiune parinte lipsa? Da/Nu")
            if permisiuneParinteLipsa == "Da" :
                print("Puteti Trece")
            else:
                print("NU puteti trece")