import csv
import ftfy
import matplotlib.pyplot as plt
from collections import Counter
array_build_A = []
array_build_B = []
abundancia_municion = []
balances_armas_build_A = []
balances_armas_build_B = []
intuicion_apuntado = []
frenetismo_apuntado = []
dificultad_enemigos_build_A = []
dificultad_enemigos_build_B = []
municion_build_A = []
municion_build_B = []
frustracion_laser_build_A = []
frustracion_laser_build_B = []
dificultad_build_A = []
dificultad_build_B = []
uso_apuntado_build_A = []
uso_apuntado_build_B = []
COLORS = ['#ef476f', '#00b4d8', '#f2e8cf', '#06d6a0', '#118ab2', '#ffcdb2']
DIFFICULTY_COLORS = ['#ebb9ff', '#a06bff','#7c3aed', '#ff52b4', '#ff2052', '#9b1b30']

def initData():
    with open('Datos/encuesta_entrevista.csv', newline='') as archivo_csv:
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

    for i in array_build_A:
        abundancia_municion.append(int(i[0]))
        balances_armas_build_A.append(i[1])
        intuicion_apuntado.append(int(i[2]))
        frenetismo_apuntado.append(int(i[3]))
        dificultad_enemigos_build_A.append(int(i[4]))
        municion_build_A.append(i[10])
        frustracion_laser_build_A.append(i[13])
        dificultad_build_A.append(i[15])
        uso_apuntado_build_A.append(i[16])

    for i in array_build_B:
        abundancia_municion.append(int(i[0]))
        balances_armas_build_B.append(i[1])
        intuicion_apuntado.append(int(i[2]))
        frenetismo_apuntado.append(int(i[3]))
        dificultad_enemigos_build_B.append(int(i[4]))
        municion_build_B.append(i[10])
        frustracion_laser_build_B.append(i[13])
        dificultad_build_B.append(i[15])
        uso_apuntado_build_B.append(i[16])

def grafica_municion():
    # Inicializar etiquetas y alturas de la gráfica
    frecuencias=[0,0,0,0,0,0]
    for i in abundancia_municion:
        frecuencias[i] = frecuencias[i]+1
    etiquetas = ["Muy escasa", "Bastante escasa", "Escasa", "Abundante", "Bastante abundante", "Muy abundante"]
    
    # Crear el gráfico de barras
    plt.title('Cantidad de munición a lo largo de los niveles')
    plt.bar(etiquetas, height=frecuencias, color=DIFFICULTY_COLORS)
    plt.show()

def grafica_balance_armas():
    # Inicializar etiquetas y frecuencias de la gráfica
    frecuencias_build_A=[0,0,0]
    frecuencias_build_B=[0,0,0]
    for i in balances_armas_build_A:
        if(i == "Sí"):
            frecuencias_build_A[0] = frecuencias_build_A[0]+1
        elif(i == "No"):
            frecuencias_build_A[1] = frecuencias_build_A[1]+1
        else: frecuencias_build_A[2] = frecuencias_build_A[2]+1
    
    for i in balances_armas_build_B:
        if(i == "Sí"):
            frecuencias_build_B[0] = frecuencias_build_B[0]+1
        elif(i == "No"):
            frecuencias_build_B[1] = frecuencias_build_B[1]+1
        else: frecuencias_build_B[2] = frecuencias_build_B[2]+1
    etiquetas = ["Sí", "No", "Depende de las circustancias"]

    # Crear el gráfico pie
    fig, ax = plt.subplots(2)
    ax[0].set_title('¿Consideras que el cuchillo está balanceado en comparación a la pistola? - BUILD A')
    ax[0].pie(frecuencias_build_A, labels=etiquetas,autopct='%1.1f%%', startangle=90, colors=COLORS)

    ax[1].set_title('¿Consideras que el cuchillo está balanceado en comparación a la pistola? - BUILD B')
    ax[1].pie(frecuencias_build_B, labels=etiquetas,autopct='%1.1f%%', startangle=90, colors=COLORS)
    plt.show()

def grafica_apuntado_pistola():
    # Inicializar etiquetas y alturas de la gráfica
    frecuencias_intuicion=[0,0,0,0,0,0]
    frecuencias_frenetismo=[0,0,0,0,0,0]
    for i in intuicion_apuntado:
        frecuencias_intuicion[i] = frecuencias_intuicion[i] + 1
    for i in frenetismo_apuntado:
        frecuencias_frenetismo[i] = frecuencias_frenetismo[i] + 1
    etiquetas_intuicion = ["Nada intuitivo", "Muy poco intuitivo", "Poco intuitivo", "Algo intuitivo", "Bastante intuitivo", "Muy intuitivo"]
    etiquetas_frentismo = ["Nada frenético", "Muy poco frenético", "Poco frenético", "Algo frenético", "Bastante frenético", "Muy frenético"]

    # Crear el gráfico de barras
    fig, ax = plt.subplots(2)
    fig.subplots_adjust(hspace=0.8)
    ax[0].set_title('Intuición apuntado pistola')
    ax[0].bar(etiquetas_intuicion,  height=frecuencias_intuicion, color=DIFFICULTY_COLORS)
    ax[0].set_xticklabels(etiquetas_intuicion, rotation=45, fontsize=8)
    ax[0].set_ylabel('Número de personas')
    ax[1].set_title('Frenetismo apuntado pistola')
    ax[1].bar(etiquetas_frentismo,  height=frecuencias_frenetismo, color=DIFFICULTY_COLORS)
    ax[1].set_xticklabels(etiquetas_frentismo, rotation=45, fontsize=8)
    ax[1].set_ylabel('Número de personas')
    plt.show()

def grafica_dificultad_enemigos():
    frecuencias_build_A= [0,0,0,0,0,0]
    frecuencias_build_B= [0,0,0,0,0,0]
    fig, ax = plt.subplots(2)
    etiquetas = ["0 Nula dificultad", "1 Poca dificultad", "2 Algo de dificultad", "3 Bastante dificultad", "4 Mucha dificultad", "5 Dificultad extrema"]
    for d in dificultad_enemigos_build_A:
        frecuencias_build_A[d] = frecuencias_build_A[d]+1
    for d in dificultad_enemigos_build_B:
        frecuencias_build_B[d] = frecuencias_build_B[d]+1
    
    ax[0].set_title('¿Cuál ha sido la dificultad para eliminar enemigos? - BUILD A')
    ax[0].bar(etiquetas,  height=frecuencias_build_A, color = DIFFICULTY_COLORS)
    ax[1].set_title('¿Cuál ha sido la dificultad para eliminar enemigos? - BUILD B')
    ax[1].bar(etiquetas,  height=frecuencias_build_B, color = DIFFICULTY_COLORS)
    plt.show()

def grafica_economizacion_municion():
    # Inicializar etiquetas y frecuencias de la gráfica
    frecuencias_build_A=[0,0,0]
    frecuencias_build_B=[0,0,0]
    for i in municion_build_A:
        if(i == "Sí"):
            frecuencias_build_A[0] = frecuencias_build_A[0]+1
        elif(i == "No"):
            frecuencias_build_A[1] = frecuencias_build_A[1]+1
        else: frecuencias_build_A[2] = frecuencias_build_A[2]+1
    
    for i in municion_build_B:
        if(i == "Sí"):
            frecuencias_build_B[0] = frecuencias_build_B[0]+1
        elif(i == "No"):
            frecuencias_build_B[1] = frecuencias_build_B[1]+1
        else: frecuencias_build_B[2] = frecuencias_build_B[2]+1    
    etiquetas = ["Sí", "No", "Uso nulo de la pistola"]

    # Crear el gráfico pie
    fig, ax = plt.subplots(2)
    ax[0].set_title('¿El jugador ha economizado la munición que tenía? - BUILD A')
    ax[0].pie(frecuencias_build_A, labels=etiquetas, autopct='%1.1f%%', startangle=90, colors = COLORS)

    ax[1].set_title('¿El jugador ha economizado la munición que tenía? - BUILD B')
    ax[1].pie(frecuencias_build_B, labels=etiquetas, autopct='%1.1f%%', startangle=90, colors = COLORS)
    plt.show()

def grafica_frustracion_laser():
    # Inicializar etiquetas y frecuencias de la gráfica
    frecuencias_build_A=[0,0]
    frecuencias_build_B=[0,0]
    for i in frustracion_laser_build_A:
        if(i == "Sí"):
            frecuencias_build_A[0] = frecuencias_build_A[0]+1
        elif(i == "No"):
            frecuencias_build_A[1] = frecuencias_build_A[1]+1
        else: frecuencias_build_A[2] = frecuencias_build_A[2]+1
    
    for i in frustracion_laser_build_B:
        if(i == "Sí"):
            frecuencias_build_B[0] = frecuencias_build_B[0]+1
        elif(i == "No"):
            frecuencias_build_B[1] = frecuencias_build_B[1]+1
        else: frecuencias_build_B[2] = frecuencias_build_B[2]+1    
    etiquetas = ["Sí", "No"]
   
    fig, ax = plt.subplots(2)

    ax[0].set_title('¿Se ha frustrado el jugador por los láseres? - BUILD A')
    ax[0].pie(frecuencias_build_A, labels=etiquetas,autopct='%1.1f%%', startangle=90, colors = COLORS)

    ax[1].set_title('¿Se ha frustrado el jugador por los láseres? - BUILD B')
    ax[1].pie(frecuencias_build_B, labels=etiquetas, autopct='%1.1f%%', startangle=90, colors = COLORS)
    plt.show()

def grafica_dificultad_enemigos_laseres():
    # Inicializar etiquetas y frecuencias de la gráfica
    frecuencias_build_A=[0,0]
    frecuencias_build_B=[0,0]
    for i in dificultad_build_A:
        if(i == "Enemigos"):
            frecuencias_build_A[0] = frecuencias_build_A[0]+1
        else: frecuencias_build_A[1] = frecuencias_build_A[1]+1
    
    for i in dificultad_build_B:
        if(i == "Enemigos"):
            frecuencias_build_B[0] = frecuencias_build_B[0]+1
        else: frecuencias_build_B[1] = frecuencias_build_B[1]+1    
    etiquetas = ["Enemigos", "Láseres"]

    # Crear el gráfico pie
    fig, ax = plt.subplots(2)
    ax[0].set_title('¿Por qué ha sentido el jugador más peligro? - BUILD A')
    ax[0].pie(frecuencias_build_A, labels=etiquetas, autopct='%1.1f%%', startangle=90, colors = COLORS)

    ax[1].set_title('¿Por qué ha sentido el jugador más peligro? - BUILD B')
    ax[1].pie(frecuencias_build_B, labels=etiquetas, autopct='%1.1f%%', startangle=90, colors = COLORS)
    plt.show()

initData()
# grafica_municion()
# grafica_balance_armas()
# grafica_apuntado_pistola()
# grafica_dificultad_enemigos()
# grafica_economizacion_municion()
# grafica_frustracion_laser()
# grafica_dificultad_enemigos_laseres()