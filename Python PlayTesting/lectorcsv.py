import csv
import ftfy

with open('b.csv', newline='') as archivo_csv:
    array_build_A = []
    array_build_B = []
    lector_csv = csv.reader(archivo_csv)
    next(lector_csv)
    for columna in lector_csv:
        build = columna[3]
        fila = columna[5:23]
        fila_sin_tildes = list(map(ftfy.fix_text, fila))
        if build == "A":
            array_build_A.append(fila_sin_tildes)
        elif build == "B":
            array_build_B.append(fila_sin_tildes)

print(array_build_A)
print(array_build_B)






