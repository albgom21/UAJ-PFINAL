import csv
import ftfy
import matplotlib.pyplot as plt
from collections import Counter


with open('b.csv', newline='') as archivo_csv:
    array_build_A = []
    array_build_B = []
    #Variable para la abundancia de munición en el mapa
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


def grafica_municion():
    abundanciaMunicion = []
    #Guardamos en la lista las respuestas
    for index in array_build_A:
        abundanciaMunicion.append(int(index[0]))  # Agregar el primer elemento convertido a entero a la lista "data"
    for index in array_build_B:
        abundanciaMunicion.append(int(index[0]))  # Agregar el primer elemento convertido a entero a la lista "data"
    # Crear la figura y los ejes
    frecuencias=dict(Counter(abundanciaMunicion))
    frecuenas_ordenadas = sorted(frecuencias.keys())
    etiquetas = []
    for valor in frecuenas_ordenadas:
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
    fig, ax = plt.subplots(2)
    # Crear el gráfico de pastel
    ax[0].set_title('Cantidad de munición a lo largo de los niveles')
    ax[0].pie(frecuencias.values(), labels=etiquetas,autopct='%1.1f%%', startangle=90)
    # Crear el gráfico de barras
    ax[1].bar(etiquetas,  height=frecuencias.values())
    ax[1].set_xlabel('Abundancia')
    ax[1].set_ylabel('Número de personas')
    plt.show()

def grafica_balance_armas():
    armas_build_A = []
    armas_build_B = []
    #Guardamos en la lista las respuestas
    for index in array_build_A:
        armas_build_A.append(index[1])  # Agregar el primer elemento convertido a entero a la lista "data"
    for index in array_build_B:
        armas_build_B.append(index[1])  # Agregar el primer elemento convertido a entero a la lista "data"

    # Crear la figura y los ejes
    frecuencias_build_A=dict(Counter(armas_build_A))
    frecuencias_build_B=dict(Counter(armas_build_B))
    frecuencias_build_A_ordenadas = sorted(frecuencias_build_A.keys())
    frecuencias_build_B_ordenadas = sorted(frecuencias_build_B.keys())

    etiquetas_build_A = []
    etiquetas_build_B = []
    for valor in frecuencias_build_A_ordenadas:
        if valor == "Sí":
            etiquetas_build_A.append("Sí")
        elif valor == "No":
            etiquetas_build_A.append("No")
        else:
            etiquetas_build_A.append("Depende de las circustancias")

    for valor in frecuencias_build_B_ordenadas:
        if valor == "Sí":
            etiquetas_build_B.append("Sí")
        elif valor == "No":
            etiquetas_build_B.append("No")
        else:
            etiquetas_build_B.append("Depende de las circustancias")
            
    fig, ax = plt.subplots(2)

    ax[0].set_title('¿Consideras que el cuchillo está balanceado en comparación a la pistola? - BUILD A')
    ax[0].pie(frecuencias_build_A.values(), labels=etiquetas_build_A,autopct='%1.1f%%', startangle=90)
    
    ax[1].set_title('¿Consideras que el cuchillo está balanceado en comparación a la pistola? - BUILD B')
    ax[1].pie(frecuencias_build_B.values(), labels=etiquetas_build_B,autopct='%1.1f%%', startangle=90)
    plt.show()

def grafica_apuntado_pistola():
    intuicion_apuntado = []
    frenetismo_apuntado = []
    #Guardamos en la lista las respuestas
    for index in array_build_A:
        intuicion_apuntado.append(int(index[2]))  
        frenetismo_apuntado.append(int(index[3]))
    for index in array_build_B:
        intuicion_apuntado.append(int(index[2]))  
        frenetismo_apuntado.append(int(index[3])) 

    # Crear la figura y los ejes
    frecuencias_intuicion=dict(Counter(intuicion_apuntado))
    frecuencias_frenetismo=dict(Counter(frenetismo_apuntado))
    frecuencias_intuicion_ordenadas = sorted(frecuencias_intuicion.keys())
    frecuencias_frenetismo_ordenadas = sorted(frecuencias_frenetismo.keys())
    etiquetas_intuicion = []
    etiquetas_frenetismo = []
    for valor in frecuencias_intuicion_ordenadas:
        if valor == 0:
            etiquetas_intuicion.append("0 nada intuitivo")
        elif valor == 1:
            etiquetas_intuicion.append("1 muy poco intuitivo")
        elif valor == 2:
            etiquetas_intuicion.append("2 poco intuitivo")
        elif valor == 3:
            etiquetas_intuicion.append("3 algo intuitivo")
        elif valor == 4:
            etiquetas_intuicion.append("4 bastante intuitivo")
        else:
            etiquetas_intuicion.append("5 muy intuitivo")
    for valor in frecuencias_frenetismo_ordenadas:
        if valor == 0:
            etiquetas_intuicion.append("0 nada frenético")
        elif valor == 1:
            etiquetas_frenetismo.append("1 muy poco frenético")
        elif valor == 2:
            etiquetas_frenetismo.append("2 poco frenético")
        elif valor == 3:
            etiquetas_frenetismo.append("3 algo frenético")
        elif valor == 4:
            etiquetas_frenetismo.append("4 bastante frenético")
        else:
            etiquetas_frenetismo.append("5 muy frenético")
        
    fig, ax = plt.subplots(2)
    ax[0].set_title('Intuición apuntado pistola')
    ax[0].bar(etiquetas_intuicion,  height=frecuencias_intuicion.values())
    ax[0].set_xlabel('Intuición')
    ax[0].set_ylabel('Número de personas')    
    ax[1].set_title('Frenetismo apuntado pistola')
    ax[1].bar(etiquetas_frenetismo,  height=frecuencias_frenetismo.values())
    ax[1].set_xlabel('Frenetismo')
    ax[1].set_ylabel('Número de personas')
    plt.show()

def grafica_dificultad_enemigos():
    enemigos_build_A = []
    enemigos_build_B = []
    #Guardamos en la lista las respuestas
    for index in array_build_A:
        enemigos_build_A.append(index[4])
    for index in array_build_B:
        enemigos_build_B.append(index[4]) 

 
    frecuencias_build_A=dict(Counter(enemigos_build_A))
    frecuencias_build_B=dict(Counter(enemigos_build_B))
    frecuancias_build_A_ordenadas = sorted(frecuencias_build_A.keys())
    frecuancias_build_B_ordenadas = sorted(frecuencias_build_B.keys())
    etiquetas_build_A = []
    etiquetas_build_B = []
    for valor in frecuancias_build_A_ordenadas:
        if valor == "0":
            etiquetas_build_A.append("0 Nula dificultad")
        elif valor == "1":
            etiquetas_build_A.append("1 Poca dificultad")
        elif valor == "2":
            etiquetas_build_A.append("2 Algo de dificultad")
        elif valor == "3":
            etiquetas_build_A.append("3 Bastante dificultad")
        elif valor == "4":
            etiquetas_build_A.append("4 Mucha dificultad")
        else:
            etiquetas_build_A.append("5 Dificultad extrema")

    for valor in frecuancias_build_B_ordenadas:
        if valor == "0":
            etiquetas_build_B.append("0 Nula dificultad")
        elif valor == "1":
            etiquetas_build_B.append("1 Poca dificultad")
        elif valor == "2":
            etiquetas_build_B.append("2 Algo de dificultad")
        elif valor == "3":
            etiquetas_build_B.append("3 Bastante dificultad")
        elif valor == "4":
            etiquetas_build_B.append("4 Mucha dificultad")
        else:
            etiquetas_build_B.append("5 Dificultad extrema")
            
    fig, ax = plt.subplots(2)

    ax[0].set_title('¿Cuál ha sido la dificultad para eliminar enemigos? - BUILD A')
    ax[0].bar(etiquetas_build_A,  height=frecuencias_build_A.values())
    ax[0].set_xlabel('Dificultad')
    ax[0].set_ylabel('Número de personas')
    
    ax[1].set_title('¿Cuál ha sido la dificultad para eliminar enemigos? - BUILD B')
    ax[1].bar(etiquetas_build_B,  height=frecuencias_build_B.values())
    ax[1].set_xlabel('Dificultad')
    ax[1].set_ylabel('Número de personas')
    plt.show()

def grafica_economizacion_municion():
    municion_build_A = []
    municion_build_B = []
    #Guardamos en la lista las respuestas
    for index in array_build_A:
        municion_build_A.append(index[10])  # Agregar el primer elemento convertido a entero a la lista "data"
    for index in array_build_B:
        municion_build_B.append(index[10])  # Agregar el primer elemento convertido a entero a la lista "data"

    # Crear la figura y los ejes
    frecuencias_build_A=dict(Counter(municion_build_A))
    frecuencias_build_B=dict(Counter(municion_build_B))
    etiquetas_build_A = []
    etiquetas_build_B = []
    frecuancias_build_A_ordenadas = sorted(frecuencias_build_A.keys())
    frecuancias_build_B_ordenadas = sorted(frecuencias_build_B.keys())
    for valor in frecuancias_build_A_ordenadas:
        if valor == "Sí":
            etiquetas_build_A.append("Sí")
        elif valor == "No":
            etiquetas_build_A.append("No")
        else:
            etiquetas_build_A.append("Uso nulo de la pistola")

    for valor in frecuancias_build_B_ordenadas:
        if valor == "Sí":
            etiquetas_build_B.append("Sí")
        elif valor == "No":
            etiquetas_build_B.append("No")
        else:
            etiquetas_build_B.append("Uso nulo de la pistola")
            
    fig, ax = plt.subplots(2)

    ax[0].set_title('¿El jugador ha economizado la munición que tenía? - BUILD A')
    ax[0].pie(frecuencias_build_A.values(), labels=etiquetas_build_A,autopct='%1.1f%%', startangle=90)
    
    ax[1].set_title('¿El jugador ha economizado la munición que tenía? - BUILD B')
    ax[1].pie(frecuencias_build_B.values(), labels=etiquetas_build_B,autopct='%1.1f%%', startangle=90)
    plt.show()

def grafica_frustracion_laser():
    frustracion_build_A = []
    frustracion_build_B = []
    #Guardamos en la lista las respuestas
    for index in array_build_A:
        frustracion_build_A.append(index[13])  # Agregar el primer elemento convertido a entero a la lista "data"
    for index in array_build_B:
        frustracion_build_B.append(index[13])  # Agregar el primer elemento convertido a entero a la lista "data"

    # Crear la figura y los ejes
    frecuencias_build_A=dict(Counter(frustracion_build_A))
    frecuencias_build_B=dict(Counter(frustracion_build_B))
    etiquetas_build_A = []
    etiquetas_build_B = []
    frecuancias_build_A_ordenadas = sorted(frecuencias_build_A.keys())
    frecuancias_build_B_ordenadas = sorted(frecuencias_build_B.keys())
    for valor in frecuancias_build_A_ordenadas:
        if valor == "Sí":
            etiquetas_build_A.append("Sí")
        else:
            etiquetas_build_A.append("No")
       
    for valor in frecuancias_build_B_ordenadas:
        if valor == "Sí":
            etiquetas_build_B.append("Sí")
        else:
            etiquetas_build_B.append("No")
            
    fig, ax = plt.subplots(2)

    ax[0].set_title('¿Se ha frustrado el jugador por los láseres? - BUILD A')
    ax[0].pie(frecuencias_build_A.values(), labels=etiquetas_build_A,autopct='%1.1f%%', startangle=90)
    
    ax[1].set_title('¿Se ha frustrado el jugador por los láseres? - BUILD B')
    ax[1].pie(frecuencias_build_B.values(), labels=etiquetas_build_B,autopct='%1.1f%%', startangle=90)
    plt.show()

def grafica_dificultad_enemigos_laseres():
    dificultad_build_A = []
    dificultad_build_B = []
    #Guardamos en la lista las respuestas
    for index in array_build_A:
        dificultad_build_A.append(index[15])  # Agregar el primer elemento convertido a entero a la lista "data"
    for index in array_build_B:
        dificultad_build_B.append(index[15])  # Agregar el primer elemento convertido a entero a la lista "data"

    # Crear la figura y los ejes
    frecuencias_build_A=dict(Counter(dificultad_build_A))
    frecuencias_build_B=dict(Counter(dificultad_build_B))
    frecuancias_build_A_ordenadas = sorted(frecuencias_build_A.keys())
    frecuancias_build_B_ordenadas = sorted(frecuencias_build_B.keys())
    etiquetas_build_A = []
    etiquetas_build_B = []
    for valor in frecuancias_build_A_ordenadas:
        if valor == "Enemigos":
            etiquetas_build_A.append("Enemigos")
        else:
            etiquetas_build_A.append("Láseres")
       
    for valor in frecuancias_build_B_ordenadas:
        if valor == "Enemigos":
            etiquetas_build_B.append("Enemigos")
        else:
            etiquetas_build_B.append("Láseres")
            
    fig, ax = plt.subplots(2)

    ax[0].set_title('¿Por qué ha sentido el jugador más peligro? - BUILD A')
    ax[0].pie(frecuencias_build_A.values(), labels=etiquetas_build_A,autopct='%1.1f%%', startangle=90)
    
    ax[1].set_title('¿Por qué ha sentido el jugador más peligro? - BUILD B')
    ax[1].pie(frecuencias_build_B.values(), labels=etiquetas_build_B,autopct='%1.1f%%', startangle=90)
    plt.show()
grafica_municion()
grafica_balance_armas()
grafica_apuntado_pistola()
grafica_dificultad_enemigos()
grafica_economizacion_municion()
grafica_frustracion_laser()
grafica_dificultad_enemigos_laseres()