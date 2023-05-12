import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px
import matplotlib.ticker as ticker
import numpy as np

#____________METODOS PARA EXTRAER METRICAS____________

def distanciaKillEne(eventos):
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
    return distanciasMatarEne        
 
def tiempoApuntado(eventos):
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
    return aimingTiempo

def tiempoUsoArmas(eventos):
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
    return cuchilloTiempo,pistolaTiempo


#____________METODOS PARA VISUALIZAR DATOS____________

def heatMapDeads(eventos,tipoMuerte=None):
    '''
    tipoMuerte puede ser "ENEMY" o "LASER", si no se pone nada son ambas
    '''
    if tipoMuerte:
        filtros = [tipoMuerte]
    else:
        filtros = ["ENEMY", "LASER"]
    # Límites de posiciones dentro del juego
    limiteXneg = -32.6041
    limiteXpos = 42.9243546
    limiteYneg = -33.3769646
    limiteYpos = 23.59616
    # Leer la imagen
    img = plt.imread('mapa.png')

    # Generar los datos del mapa de calor
    muertes = [[e["posX"], e["posY"]] for e in eventos['POS_PLAYER_DEAD'] if e["dead"] in filtros]
    x = [m[0] for m in muertes]
    y = [m[1] for m in muertes]

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(10, 10))

    # Crear el mapa de calor
    hb = ax.hexbin(x, y, gridsize=30, cmap='plasma', linewidths=.5, mincnt=1, alpha=0.95)

    # Agregar la imagen como fondo
    ax.imshow(img, extent=[limiteXneg, limiteXpos, limiteYneg, limiteYpos], aspect='auto',)

    # Establecer la misma escala en ambas direcciones y ajustar los límites de los ejes
    ax.set_aspect('equal')

    ax.set_xlim([limiteXneg, limiteXpos])
    ax.set_ylim([limiteYneg, limiteYpos])

    # Agregar la barra de colores
    cb = plt.colorbar(hb)
    # Establecer el formato de los ticks para que solo muestre valores enteros
    cb.ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))

    titulo = "Mapa de calor de muertes causadas por "
    if(len(filtros) == 2):
        titulo += "enemigos y láseres"
    elif(filtros[0] == "ENEMY"):
        titulo += "enemigos"
    elif(filtros[0] == "LASER"):
        titulo += "láseres"
    
    plt.title(titulo)

    # Mostrar la figura
    plt.show()

def graficoCircular(titulo, datos, labels, colors):
    plt.pie(datos, labels=labels, colors=colors, autopct="%0.1f %%")
    plt.title(titulo)
    plt.show()

def timelineUsoArmas(eventos):
    #
## TIMELINE 
 # Creamos una lista de eventos de prueba
    aux = eventos["CHANGE_WEAPON"] + eventos["POS_PLAYER_DEAD"] + eventos["INI_LVL"] + eventos["END_LVL"]
    
    y_values = []
    x_values = []
    ammo_values = []

    aux = sorted(aux, key=lambda k: k['timestamp'])
    for evento in aux:
        if(evento.get('tipo') == "INI_LVL"):
            y_values.append("cuchillo")
            x_values.append(evento.get('timestamp'))
            actualWeapon = "KNIFE"
            actualAmmo = 5
            ammo_values.append(actualAmmo)

        elif(evento.get('tipo') == "END_LVL"):
            x_values.append(evento.get('timestamp'))

        # Si ha muerto contabilizar el tiempo que llevaba segun el arma
        elif(evento.get('tipo') == "POS_PLAYER_DEAD"):
            if(actualWeapon == "PISTOL" or actualAmmo < 5):
                x_values.append(evento.get('timestamp'))
                actualWeapon = "KNIFE"
                y_values.append("cuchillo")
                actualAmmo = 5
                ammo_values.append(actualAmmo)

        # Teniendo la pistola cambio a cuchillo
        elif(evento.get('tipo') == "CHANGE_WEAPON" and evento.get('weapon') == 'KNIFE') and actualWeapon == "PISTOL":
            actualWeapon = "KNIFE"
            x_values.append(evento.get('timestamp'))
            y_values.append("cuchillo")
            ammo_values.append(evento.get('ammo'))
            actualAmmo = evento.get('ammo')
        # Teniendo el cuchillo cambio a pistola
        elif(evento.get('tipo') == "CHANGE_WEAPON" and evento.get('weapon') == 'PISTOL') and actualWeapon == "KNIFE":
            actualWeapon = "PISTOL"
            x_values.append(evento.get('timestamp'))
            y_values.append("pistola")
            ammo_values.append(evento.get('ammo'))
            actualAmmo = evento.get('ammo')

    aux = x_values[0]
    x_values_end = x_values.copy()
    colors1 = y_values.copy()

    #Dependiendo de y_values, se le asigna un color a colors1
    for x in range(len(y_values)):
        if y_values[x] == 'pistola':
            colors1[x] = 'Pistola'
        elif y_values[x] == 'cuchillo':
            colors1[x] = 'Cuchillo'
        else:
            colors1[x] = 'black'



    for x in range(len(x_values)):
        if x < len(x_values) - 1:
            totalSegundos = x_values[x + 1] - aux
            minutos = totalSegundos // 60
            segundos = totalSegundos % 60

            x_values_end[x] = pd.to_datetime(f'{minutos}:{segundos}', format='%M:%S')
        else:
            totalSegundos = x_values[x] - aux
            minutos = totalSegundos // 60
            segundos = totalSegundos % 60

            x_values_end[x] = pd.to_datetime(f'{minutos}:{segundos}', format='%M:%S')
        if(x_values[x] != aux):
            totalSegundos = x_values[x] - aux
            minutos = totalSegundos // 60
            segundos = totalSegundos % 60

            x_values[x] = pd.to_datetime(f'{minutos}:{segundos}', format='%M:%S')
        else:
            totalSegundos = x_values[x] - aux
            minutos = totalSegundos // 60
            segundos = totalSegundos % 60

            x_values[x] = pd.to_datetime(f'{minutos}:{segundos}', format='%M:%S')

    auxData = pd.DataFrame()

    #dar a auxdata los valores de x_values y y_values
    auxData['x_values'] = x_values
    auxData['time_end'] = x_values_end
    auxData['Armas'] = y_values
    auxData['Leyenda'] = colors1
    auxData['ammo'] = ammo_values

    fig = px.timeline(auxData,
                    x_start='x_values',
                    x_end='time_end',
                    y="Armas",
                    text="ammo",
                    color="Leyenda")

    fig.update_layout(xaxis=dict(tickformat="%M:%Ss"))
    fig.update_layout(font=dict(size=20))
    fig.show()

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

    # EVENTOS DE LA TELEMETRÍA
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

    # Guardar todos los eventos segun el tipo
    for evento in datos:
        eventos[evento["tipo"]].append(evento)


#-----------------------------------------------------------------------------------------
#-----------------------------------CALCULO DE METRICAS-----------------------------------
#-----------------------------------------------------------------------------------------

#________Tiempo medio del uso de la pistola y del cuchillo________
    cuchilloTiempo, pistolaTiempo = tiempoUsoArmas(eventos)

#________Número de veces que el jugador cambia de arma________
    print("CAMBIOS DE ARMAS: ",len(eventos['CHANGE_WEAPON']))

#________Número de usos de cada arma________
    contUsoCuchillo = sum(1 for evento in eventos['POS_PLAYER_ATTACK'] if evento.get('weapon') == 'KNIFE')
    contUsoPistola = sum(1 for evento in eventos['POS_PLAYER_ATTACK']  if evento.get('weapon') == 'PISTOL')

    print("USO DE CUCHILLO: ",contUsoCuchillo)
    print("USO DE PISTOLA: ",contUsoPistola)

#________Número de veces que el jugador mata con cada una de las armas________
    contKillsCuchillo = sum(1 for evento in eventos['POS_PLAYER_KILL']  if evento.get('weapon') == 'KNIFE')
    contKillsPistola = sum(1 for evento in eventos['POS_PLAYER_KILL']  if evento.get('weapon') == 'PISTOL')
    killsTotales = contKillsPistola+contKillsCuchillo

    print("KILLS TOTALES: ", killsTotales)
    print("KILLS CON CUCHILLO: ",contKillsCuchillo, "Porcentaje: " , (contKillsCuchillo/killsTotales)*100, "%")
    print("KILLS CON PISTOLA: ",contKillsPistola, "Porcentaje: " , (contKillsPistola/killsTotales)*100, "%")

#________Número de veces que el jugador muere por colisionar con un láser________
    contDeadLaser = sum(1 for evento in eventos['POS_PLAYER_DEAD']  if evento.get('dead') == 'LASER')

#________Posición en la que muere el jugador cuando colisiona con láseres________
    posDeadLaser = [(evento['posX'], evento['posY']) for evento in filter(lambda e: e.get('dead') == 'LASER', eventos['POS_PLAYER_DEAD'])]
    # print("POS DEAD CON LASER: ",posDeadLaser)
    
#________Posición del enemigo al eliminar al jugador________
    posEnemigoKill = [(evento['posX'], evento['posY']) for evento in eventos['POS_ENEMY_KILL']]
    contKillsDeEnemigos = len(posEnemigoKill)

    print("KILLS DE ENEMIGOS: ", contKillsDeEnemigos)
    # print("POS KILL ENEMIGO: ", posEnemigoKill)

#________Número de veces que el jugador muere por el disparo de un enemigo________
    contDeadEnemigo = sum(1 for evento in eventos['POS_PLAYER_DEAD']  if evento.get('dead') == 'ENEMY')

    contSuicidios = contDeadEnemigo - contKillsDeEnemigos #Al suicidarte con un rebote de bala se marca como que te ha matado un enemigo
    deadsTotales = contDeadEnemigo+contDeadLaser
    contDeadEnemigo -= contSuicidios
    porcentajesTiposDeMuertes = [(contDeadEnemigo/deadsTotales)*100,(contDeadLaser/deadsTotales)*100,(contSuicidios/deadsTotales)*100]

    print("DEADS TOTALES: ", deadsTotales)
    print("DEAD CON ENEMIGO: ",contDeadEnemigo, "Porcentaje: " , porcentajesTiposDeMuertes[0], "%")
    print("DEAD CON LASER: ",contDeadLaser, "Porcentaje: " , porcentajesTiposDeMuertes[1], "%")
    print("DEAD CON SUICIDIO: ",contSuicidios, "Porcentaje: " , porcentajesTiposDeMuertes[2], "%")

#________Posición en la que el jugador muere por un enemigo________
    posDeadEnemigo = [(evento['posX'], evento['posY']) for evento in filter(lambda e: e.get('dead') == 'ENEMY', eventos['POS_PLAYER_DEAD'])]
    # print("POS DEAD CON ENEMIGO: ",posDeadEnemigo)

#________Tiempo medio que el jugador está apuntando con la pistola________
    aimingTiempo = tiempoApuntado(eventos)
    
    print("TIEMPO AIMING: ",aimingTiempo, "s")

#________Distancia enemigo-jugador al matar a un enemigo________
    distancias = distanciaKillEne(eventos)


#-----------------------------------------------------------------------------------------
#-----------------------------------FIN CALCULO DE METRICAS-------------------------------
#-----------------------------------------------------------------------------------------    


#-----------------------------------------------------------------------------------------
#-------------------------------------DATOS VISUALES--------------------------------------
#-----------------------------------------------------------------------------------------
    # tiposArmas = ["CUCHILLO","PISTOLA"]
    # tiposMuertes = ["ENEMIGO","LASER","SUICIDIO"]
    # colors = ['#ef476f', '#00b4d8', '#f2e8cf']

    # # Mostrar el porcentaje del uso total de cada arma en el tiempo
    # tiempoArmas = cuchilloTiempo + pistolaTiempo    # Deberia ser el tiempo total
    # porcentajesTiemposArmas = [(cuchilloTiempo/tiempoArmas) * 100, (pistolaTiempo/tiempoArmas) * 100] 
    # graficoCircular('Porcentaje del uso de cada arma en el tiempo', porcentajesTiemposArmas, tiposArmas, colors)

    # # Las veces con las que se ataca con cada arma
    # vecesUsoArmas = contUsoCuchillo + contUsoPistola   
    # porcentajesUsoArmas = [(contUsoCuchillo/vecesUsoArmas) * 100, (contUsoPistola/vecesUsoArmas) * 100] 
    # graficoCircular('Porcentaje de ataque con cada arma', porcentajesUsoArmas, tiposArmas, colors)

    # # Las veces con las que se ataca con cada arma ???????????????
    # porcentajesUsoArmas = [(contUsoCuchillo/killsTotales) * 100, (contUsoPistola/killsTotales) * 100] 
    # graficoCircular('Porcentaje de kills con cada arma en comparación a su uso', porcentajesUsoArmas, tiposArmas, colors)

    # # Un timeline que recoja el uso de cada arma en el tiempo y con la información de la munición.

    # # El número de asesinatos con cada arma y su ratio de efectividad (asesinatos/ataque).
    # usos = [contUsoCuchillo, contUsoPistola]
    # asesinatos= [contKillsCuchillo, contKillsPistola]
    # print('Efectividad cuchillo:', (contKillsCuchillo/contUsoCuchillo)*100, "%")
    # print('Efectividad pistola:', (contKillsPistola/contUsoPistola)*100, "%")


    # # crear un gráfico de barras con dos series de datos
    # x = range(len(tiposArmas))
    # plt.bar([i - 0.2 for i in x], usos, width=0.3, align='center', label='Usos', color='#a8dadc')
    # plt.bar([i + 0.2 for i in x], asesinatos, width=0.3, align='center', label='Asesinatos', color='#e63946')

    # # añadir etiquetas de los ejes y la leyenda
    # plt.xlabel('Armas')
    # plt.ylabel('Valores')
    # plt.xticks(x, tiposArmas)
    # plt.legend()

    # for i, v in enumerate(usos):
    #     plt.text(i - 0.2, v + 0.5, str(v), color='#4a6263', fontweight='bold', ha='center', va='bottom')
    # for i, v in enumerate(asesinatos):
    #     plt.text(i + 0.2, v + 0.5, str(v), color='#541519', fontweight='bold', ha='center', va='bottom')

    # # mostrar el gráfico
    # plt.show()

    # # Gráfico distancias y arma
    # dPistola = []
    # dCuchillo= []
    # for d in distancias:
    #     if d['Arma'] == 'PISTOL':
    #         dPistola.append(d['Dist'])
    #     elif d['Arma'] == 'KNIFE':
    #         dCuchillo.append(d['Dist'])

    # plt.bar(dPistola, dPistola, color = 'red', width=0.015, alpha=0.8, label= 'Pistola')
    # plt.bar(dCuchillo, dCuchillo, color = 'blue', width=0.015, alpha=0.5, label= 'Cuchillo')
    # plt.xlabel('Distancia')
    # plt.ylabel('Distancia')
    # plt.title('Distancias de las kills y arma usada')
    # plt.legend(loc='best')
    # plt.show()

    # # Tipos de muertes
    # graficoCircular('Causas de muertes del jugador', porcentajesTiposDeMuertes, tiposMuertes, colors)

    # # MAPA DE CALOR TODAS LAS MUERTES
    # heatMapDeads(eventos)
    # # MAPA DE CALOR CON LAS MUERTES DE ENEMIGOS
    # heatMapDeads(eventos, "ENEMY")
    # # MAPA DE CALOR CON LAS MUERTES DE LASERES
    # heatMapDeads(eventos, "LASER")

    # listas para guardar los timestamps y tipos de muerte
    timestampsLaser = []
    timestampsEnemigo = []
    timestampsSuicidio = []
    eventosSuicidio = []
    tiempoInicio = eventos["INI_LVL"][0].get("timestamp")

    # extraer la información de timestamp y tipo de muerte de cada muerte
    cont = 0
    for e in eventos['POS_PLAYER_DEAD']:
        if cont > len(eventos["POS_ENEMY_KILL"]):
            break
        if(e['dead'] == 'ENEMY' and e.get('timestamp') == eventos["POS_ENEMY_KILL"][cont].get('timestamp')):
            cont+=1
        elif e['dead'] == 'ENEMY':
            eventosSuicidio.append(e)
            timestampsSuicidio.append(e["timestamp"]-tiempoInicio)
            
    for e in eventos["POS_PLAYER_DEAD"]:
        if e['dead'] == 'ENEMY':
            timestampsEnemigo.append(e["timestamp"]-tiempoInicio)

        elif e['dead'] == 'LASER':
            timestampsLaser.append(e["timestamp"]-tiempoInicio)
      

    # crear la figura y el eje
    fig, ax = plt.subplots()

    # graficar los puntos en el timeline
    for i in range(len(timestampsEnemigo)):
        ax.scatter(timestampsEnemigo[i], 0, color="green", s=50, alpha=0.5)
    for i in range(len(timestampsLaser)):
        ax.scatter(timestampsLaser[i], 0, color="red", s=50, alpha=0.5)
    for i in range(len(timestampsSuicidio)):
        ax.scatter(timestampsSuicidio[i], 0, color="orange", s=50, alpha=0.75)

    # configurar el eje x
    ax.set_xlabel('Timestamp')

    # ocultar el eje y
    ax.get_yaxis().set_visible(False)

    color_map = {"LASER": "red", "SUICIDIO": "orange", "ENEMIGO": "green"}
    # mostrar la leyenda de colores
    for tipo_muerte, color in color_map.items():
        ax.scatter([], [], color=color, label=tipo_muerte)

    ax.legend(loc='upper left', framealpha=1)

    # mostrar el gráfico
    plt.show()

    timelineUsoArmas(eventos)
#-----------------------------------------------------------------------------------------
#-----------------------------------FIN DATOS VISUALES------------------------------------
#-----------------------------------------------------------------------------------------


main()
