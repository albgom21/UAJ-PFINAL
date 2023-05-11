import os
import json
import matplotlib.pyplot as plt

def main():
    # # Para leer todos los json de una carpeta
    # # Carpeta donde se encuentran los archivos JSON
    # carpeta = './json_files'

    # # Recorrer todos los archivos en la carpeta
    # for archivo in os.listdir(carpeta):
    #     if archivo.endswith('.json'):
    #         # Abrir el archivo JSON y leer su contenido
    #         with open(os.path.join(carpeta, archivo), 'r') as f:
    #             contenido = json.load(f)
    #         # Hacer algo con el contenido del archivo

    # Leer datos de archivos json
    with open('./Datos/BAVictor.json', 'r') as f:
        datos = json.load(f)

    eventos = {
    "INI_SESSION": [],
    "END_SESSION": [],
    "INI_LVL": [],
    "END_LVL": [],
    "CHANGE_WEAPON": [],
    "POS_PLAYER_ATTACK": [],
    "POS_PLAYER_KILL": [],
    "POS_PLAYER_DEAD": [],
    "PRESS_BUTTON": [],
    "POS_ENEMY_DEAD": [],
    "POS_ENEMY_KILL": [],
    "AIMING": [],
    "NOT_AIMING": []
    }

    for evento in datos:
        eventos[evento["tipo"]].append(evento)

#-----------------------------------CALCULO DE METRICAS-----------------------------------
#________Tiempo medio del uso de la pistola y del cuchillo________
    auxTiempo = eventos["INI_SESSION"][0].get('timestamp')  # Tiempo de inicio
    actualWeapon = "KNIFE"                         # Arma actual 
    cuchilloTiempo = 0                             # Tiempo de uso en seg del cuchillo
    pistolaTiempo = 0                              # Tiempo de uso en seg de la pistola


    # Unir las dos listas en una nueva lista auxiliar
    aux = eventos["CHANGE_WEAPON"] + eventos["POS_PLAYER_DEAD"]

    # Ordenar la lista combinada por timestamp
    aux = sorted(aux, key=lambda k: k['timestamp'])

    for evento in aux:
        # Si ha muerto contabilizar el tiempo que llevaba segun el arma
        if(evento.get('tipo') == "POS_PLAYER_DEAD"):
            if(actualWeapon == "PISTOL"):
                pistolaTiempo += evento.get('timestamp') - auxTiempo
            elif(actualWeapon == "KNIFE"):
                cuchilloTiempo += evento.get('timestamp') - auxTiempo
            actualWeapon = "KNIFE"
            auxTiempo = evento.get('timestamp')

        # Teniendo la pistola cambio a pistola
        if(evento.get('tipo') == "CHANGE_WEAPON" and evento.get('weapon') == 'KNIFE') and actualWeapon == "PISTOL":
            actualWeapon = "KNIFE"
            pistolaTiempo += evento.get('timestamp') - auxTiempo
            auxTiempo = evento.get('timestamp')
        # Teniendo el cuchillo cambio a pistola
        elif(evento.get('tipo') == "CHANGE_WEAPON" and evento.get('weapon') == 'PISTOL') and actualWeapon == "KNIFE":
            actualWeapon = "PISTOL"
            cuchilloTiempo += evento.get('timestamp') - auxTiempo
            auxTiempo = evento.get('timestamp')

    # Contabilizar tiempo que se llevaba con el arma al acabar la sesión / nivel
    lastTime = 0
    if len(eventos["END_LVL"]) > 0: # Si se termino el nivel
        lastTime = eventos["END_LVL"][0].get('timestamp')
    else:
        lastTime = eventos['END_SESSION'][0].get('timestamp')
    if(actualWeapon == "PISTOL"):
        pistolaTiempo += lastTime - auxTiempo
    elif(actualWeapon == "KNIFE"):
        cuchilloTiempo += lastTime - auxTiempo
    
    print("Tiempo cuchillo: ", cuchilloTiempo, "s")
    print("Tiempo pistola: ", pistolaTiempo, "s" )

#________Número de veces que el jugador cambia de arma________
    print("CAMBIOS DE ARMAS: ",len(eventos['CHANGE_WEAPON']))

#________Número de usos de cada arma________
    contUsoCuchillo = sum(1 for evento in eventos['POS_PLAYER_ATTACK'] if evento.get('weapon') == 'KNIFE')
    print("USO DE CUCHILLO: ",contUsoCuchillo)

    contUsoPistola = sum(1 for evento in eventos['POS_PLAYER_ATTACK']  if evento.get('weapon') == 'PISTOL')
    print("USO DE PISTOLA: ",contUsoPistola)

#________Número de veces que el jugador mata con cada una de las armas________
    contKillsCuchillo = sum(1 for evento in eventos['POS_PLAYER_KILL']  if evento.get('weapon') == 'KNIFE')
    print("KILLS CON CUCHILLO: ",contKillsCuchillo)

    contKillsPistola = sum(1 for evento in eventos['POS_PLAYER_KILL']  if evento.get('weapon') == 'PISTOL')
    print("KILLS CON PISTOLA: ",contKillsPistola)

#________Número de veces que el jugador muere por colisionar con un láser________
    contDeadLaser = sum(1 for evento in eventos['POS_PLAYER_DEAD']  if evento.get('dead') == 'LASER')
    print("DEAD CON LASER: ",contDeadLaser)

#________Posición en la que muere el jugador cuando colisiona con láseres________
    posDeadLaser = [(evento['posX'], evento['posY']) for evento in filter(lambda e: e.get('dead') == 'LASER', eventos['POS_PLAYER_DEAD'])]
    print("POS DEAD CON LASER: ",posDeadLaser)
    
#________Número de veces que el jugador muere por el disparo de un enemigo________
    contDeadEnemigo = sum(1 for evento in eventos['POS_PLAYER_DEAD']  if evento.get('dead') == 'ENEMY')
    print("DEAD CON ENEMIGO: ",contDeadEnemigo)

#________Posición en la que el jugador muere por un enemigo________
    posDeadEnemigo = [(evento['posX'], evento['posY']) for evento in filter(lambda e: e.get('dead') == 'ENEMY', eventos['POS_PLAYER_DEAD'])]
    print("POS DEAD CON ENEMIGO: ",posDeadEnemigo)

#________Posición del enemigo al eliminar al jugador________
    posEnemigoKill = [(evento['posX'], evento['posY']) for evento in eventos['POS_ENEMY_KILL']]
    print("POS KILL ENEMIGO: ",posEnemigoKill)

#________Tiempo medio que el jugador está apuntando con la pistola________
    aiming = False
    aimingTiempo = 0
    auxTiempo = 0
    # Unir las dos listas en una nueva lista auxiliar
    aux = eventos["CHANGE_WEAPON"] + eventos["POS_PLAYER_DEAD"] + eventos['AIMING'] + eventos["NOT_AIMING"]

    # Ordenar la lista combinada por timestamp
    aux = sorted(aux, key=lambda k: k['timestamp'])

    for evento in aux:
        if(evento.get('tipo') == "AIMING"):
            aiming = True
            auxTiempo = evento.get('timestamp')
        elif((evento.get('tipo') == "NOT_AIMING" or evento.get('tipo') == "POS_PLAYER_DEAD" or evento.get('tipo') == "CHANGE_WEAPON") and aiming):
            aiming = False
            aimingTiempo += evento.get('timestamp') - auxTiempo
    
    print("TIEMPO AIMING: ",aimingTiempo, "s")
    
#-----------------------------------DATOS VISUALES-----------------------------------
    #------Objetivo sobre uso equitativo de armas------
    # Mostrar el porcentaje del uso total de cada arma.
 
    tiempoArmas = cuchilloTiempo + pistolaTiempo    # Deberia ser el tiempo total
    porcentajesTiemposArmas = [(cuchilloTiempo/tiempoArmas) * 100, (pistolaTiempo/tiempoArmas) * 100] 
    nombres = ["CUCHILLO","PISTOLA"]
    colors = ['#ef476f', '#00b4d8',]
    plt.pie(porcentajesTiemposArmas, labels=nombres, colors=colors, autopct="%0.1f %%")
    plt.title('Porcentaje del uso en el timepo de cada arma')
    plt.show()

    # Las veces con las que se ataca con cada arma.
    vecesUsoArmas = contUsoCuchillo + contUsoPistola   
    porcentajesUsoArmas = [(contUsoCuchillo/vecesUsoArmas) * 100, (contUsoPistola/vecesUsoArmas) * 100] 
    nombres = ["CUCHILLO","PISTOLA"]
    plt.pie(porcentajesUsoArmas, labels=nombres,colors=colors, autopct="%0.1f %%")
    plt.title('Porcentaje del ataque con cada arma')
    plt.show()

    # Un timeline que recoja el uso de cada arma en el tiempo y con la información de la munición.

    # El número de asesinatos con cada arma y su ratio de efectividad (asesinatos/ataque).
    armas = ['CUCHILLO', 'PISTOLA']
    usos = [contUsoCuchillo, contUsoPistola]
    asesinatos= [contKillsCuchillo, contKillsPistola]
    #efectividad = [(contKillsCuchillo/contUsoCuchillo)*100, (contKillsPistola/contUsoPistola)*100]


    # crear un gráfico de barras con dos series de datos
    x = range(len(armas))
    plt.bar([i - 0.2 for i in x], usos, width=0.3, align='center', label='Usos', color='#a8dadc')
    plt.bar([i + 0.2 for i in x], asesinatos, width=0.3, align='center', label='Asesinatos', color='#e63946')

    # añadir etiquetas de los ejes y la leyenda
    plt.xlabel('Armas')
    plt.ylabel('Valores')
    plt.xticks(x, armas)
    plt.legend()

    for i, v in enumerate(usos):
        plt.text(i - 0.2, v + 0.5, str(v), color='#4a6263', fontweight='bold', ha='center', va='bottom')
    for i, v in enumerate(asesinatos):
        plt.text(i + 0.2, v + 0.5, str(v), color='#541519', fontweight='bold', ha='center', va='bottom')

    # mostrar el gráfico
    plt.show()

    # Distancia enemigo-jugador al matar a un enemigo.
    distanciasMatarEne = []
    # Comprobar que haya el mismo numero de muertes de enemigos que kills haya hecho el jugador
    if(len(eventos['POS_ENEMY_DEAD']) == len(eventos['POS_PLAYER_KILL'])):
        for i, evento in enumerate(eventos['POS_ENEMY_DEAD']):
            if(evento.get('timestamp') == eventos['POS_PLAYER_KILL'][i].get('timestamp')):
                x1 = eventos['POS_PLAYER_KILL'][i].get('posX')
                y1 = eventos['POS_PLAYER_KILL'][i].get('posY')

                x2 = evento.get('posX')
                y2 = evento.get('posY')
                distancia = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                info = {
                    'Dist': distancia,
                    'Arma': eventos['POS_PLAYER_KILL'][i].get('weapon'),              
                }
                distanciasMatarEne.append(info)
        
    print("Distancias: ",distanciasMatarEne)
    
main()

#----------------------------EVENTOS DE LA TELEMETRÍA----------------------------
# INI_SESSION
# END_SESSION
# INI_LVL
# END_LVL
# CHANGE_WEAPON
# POS_PLAYER_ATTACK
# POS_PLAYER_KILL
# POS_PLAYER_DEAD
# PRESS_BUTTON
# POS_ENEMY_DEAD
# POS_ENEMY_KILL
# AIMING
# NOT_AIMING