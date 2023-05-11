import csv
import ftfy
import matplotlib.pyplot as plt
from collections import Counter


with open('b.csv', newline='') as archivo_csv:
    array_build_A = []
    array_build_B = []
    #Variable para la abundancia de munición en el mapa
    AbundanciaMunicion=[]
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
    #Guardamos en la lista las respuestas
    for index in array_build_A:
        AbundanciaMunicion.append(int(index[0]))  # Agregar el primer elemento convertido a entero a la lista "data"
    for index in array_build_B:
        AbundanciaMunicion.append(int(index[0]))  # Agregar el primer elemento convertido a entero a la lista "data"
    # Crear la figura y los ejes
frecuencias=dict(Counter(AbundanciaMunicion))
etiquetas = []
for valor in frecuencias.keys():
    if valor == 0:
        etiquetas.append("0 muy escasa")
    elif valor == 1:
        etiquetas.append("1 bastante escasa")
    elif valor == 2:
        etiquetas.append("2 escasa")
    elif valor == 3:
        etiquetas.append("3 abundante")
    elif valor == 4:
        etiquetas.append("4 bastante abundante")
    else:
        etiquetas.append("5 muy abundante")
print (len(etiquetas))
fig, ax = plt.subplots()
# Crear el gráfico de pastel
ax.set_title('Cantidad de munición a lo largo de los niveles')
ax.pie(frecuencias.values(), labels=etiquetas,autopct='%1.1f%%', startangle=90)
plt.show()
# Crear el gráfico de barras
ax.bar(frecuencias.keys(),  height=frecuencias.values())
ax.set_xlabel('Abundancia')
ax.set_ylabel('Número de personas')
plt.show()


print(array_build_A)
print(array_build_B)






