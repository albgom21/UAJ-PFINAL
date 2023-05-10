import json
import matplotlib.pyplot as plt


def main():
    with open('./Datos/BAVictor.json', 'r') as f:
        datos = json.load(f)

    event_ini_session = []
    event_end_session = []
    event_ini_lvl = []
    event_end_lvl = []
    event_change_weapon = []
    event_pos_player_attack = []
    event_pos_player_kill = []
    event_pos_player_dead = []
    event_press_button =[]
    event_pos_enemy_dead=[]
    event_pos_enemy_kill=[]
    event_aiming =[]
    event_not_aiming =[]
    
    event_change_weapon_and_dead = []
    events_for_aiming_time = []
    events_for_distance = []

    for evento in datos:
       
        if(evento['tipo'] == "INI_SESSION"):          
            event_ini_session.append(evento)
        elif(evento['tipo'] == "END_SESSION"):          
            event_end_session.append(evento)
        elif(evento['tipo'] == "INI_LVL"):          
            event_ini_lvl.append(evento)
        elif(evento['tipo'] == "END_LVL"):          
            event_end_lvl.append(evento)    
        elif(evento['tipo'] == "CHANGE_WEAPON"):          
            event_change_weapon.append(evento)    
            event_change_weapon_and_dead.append(evento)
            events_for_aiming_time.append(evento)
        elif(evento['tipo'] == "POS_PLAYER_ATTACK"):          
            event_pos_player_attack.append(evento)
        elif(evento['tipo'] == "POS_PLAYER_KILL"):          
            event_pos_player_kill.append(evento)
        elif(evento['tipo'] == "POS_PLAYER_DEAD"):          
            event_pos_player_dead.append(evento)
            event_change_weapon_and_dead.append(evento)
            events_for_aiming_time.append(evento)
        elif(evento['tipo'] == "PRESS_BUTTON"):          
            event_press_button.append(evento)
        elif(evento['tipo'] == "POS_ENEMY_DEAD"):          
            event_pos_enemy_dead.append(evento)
        elif(evento['tipo'] == "POS_ENEMY_KILL"):          
            event_pos_enemy_kill.append(evento)
        elif(evento['tipo'] == "AIMING"):          
            event_aiming.append(evento)
            events_for_aiming_time.append(evento)
        elif(evento['tipo'] == "NOT_AIMING"):          
            event_not_aiming.append(evento)    
            events_for_aiming_time.append(evento)

#-----------------------------------CALCULO DE METRICAS-----------------------------------
# Tiempo medio del uso de la pistola y del cuchillo
    # Tiempo de inicio con el cuchillo
    auxTiempo = event_ini_lvl[0].get('timestamp')
    actualWeapon = "KNIFE"
    cuchilloTiempo = 0
    pistolaTiempo = 0
    for evento in event_change_weapon_and_dead:
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

    
    lastTime = 0
    if(len(event_end_lvl) > 0):
        lastTime = event_end_lvl[0].get('timestamp')
    else:
        lastTime = event_end_session[0].get('timestamp')

    # Contar el tiempo que se llevaba con el arma al acabar la sesion
    if(actualWeapon == "PISTOL"):
        pistolaTiempo += lastTime - auxTiempo
    elif(actualWeapon == "KNIFE"):
        cuchilloTiempo += lastTime - auxTiempo

    print("Tiempo cuchillo: ", cuchilloTiempo, "s")
    print("Tiempo pistola: ", pistolaTiempo, "s" )

# Número de veces que el jugador cambia de arma
    print("CAMBIOS DE ARMAS: ",len(event_change_weapon))

# Número de usos de cada arma
    contUsoCuchillo = sum(1 for evento in event_pos_player_attack if evento.get('weapon') == 'KNIFE')
    print("USO DE CUCHILLO: ",contUsoCuchillo)

    contUsoPistola = sum(1 for evento in event_pos_player_attack if evento.get('weapon') == 'PISTOL')
    print("USO DE PISTOLA: ",contUsoPistola)

# Número de veces que el jugador mata con cada una de las armas
    contKillsCuchillo = sum(1 for evento in event_pos_player_kill if evento.get('weapon') == 'KNIFE')
    print("KILLS CON CUCHILLO: ",contKillsCuchillo)

    contKillsPistola = sum(1 for evento in event_pos_player_kill  if evento.get('weapon') == 'PISTOL')
    print("KILLS CON PISTOLA: ",contKillsPistola)

# Número de veces que el jugador muere por colisionar con un láser
    contDeadLaser = sum(1 for evento in event_pos_player_dead  if evento.get('dead') == 'LASER')
    print("DEAD CON LASER: ",contDeadLaser)

# Posición en la que muere el jugador cuando colisiona con láseres
    posDeadLaser = [(evento['posX'], evento['posY']) for evento in filter(lambda e: e.get('dead') == 'LASER', event_pos_player_dead)]
    print("POS DEAD CON LASER: ",posDeadLaser)
    
# Número de veces que el jugador muere por el disparo de un enemigo
    contDeadEnemigo = sum(1 for evento in event_pos_player_dead  if evento.get('dead') == 'ENEMY')
    print("DEAD CON ENEMIGO: ",contDeadEnemigo)

# Posición en la que el jugador muere por un enemigo
    posDeadEnemigo = [(evento['posX'], evento['posY']) for evento in filter(lambda e: e.get('dead') == 'ENEMY', event_pos_player_dead)]
    print("POS DEAD CON ENEMIGO: ",posDeadEnemigo)

# Posición del enemigo al eliminar al jugador
    posEnemigoKill = [(evento['posX'], evento['posY']) for evento in event_pos_enemy_kill]
    print("POS KILL ENEMIGO: ",posEnemigoKill)

# Tiempo medio que el jugador está apuntando con la pistola
    aiming = False
    aimingTiempo = 0
    auxTiempo = 0
    for evento in events_for_aiming_time:
        if(evento.get('tipo') == "AIMING"):
            aiming = True
            auxTiempo = evento.get('timestamp')
        elif((evento.get('tipo') == "NOT_AIMING" or evento.get('tipo') == "POS_PLAYER_DEAD" or evento.get('tipo') == "CHANGE_WEAPON") and aiming):
            aiming = False
            aimingTiempo += evento.get('timestamp') - auxTiempo
    
    print("TIEMPO AIMING: ",aimingTiempo, "s")
    

    #------Objetivo sobre uso equitativo de armas------
    # Mostrar el porcentaje del uso total de cada arma.
 
    tiempoArmas = cuchilloTiempo + pistolaTiempo    # Deberia ser el tiempo total
    porcentajesTiemposArmas = [(cuchilloTiempo/tiempoArmas) * 100, (pistolaTiempo/tiempoArmas) * 100] 
    nombres = ["CUCHILLO","PISTOLA"]
    plt.pie(porcentajesTiemposArmas, labels=nombres, autopct="%0.1f %%")
    plt.title('Porcentaje del uso en el timepo de cada arma')
    plt.show()

    # Las veces con las que se ataca con cada arma.
    vecesUsoArmas = contUsoCuchillo + contUsoPistola   
    porcentajesUsoArmas = [(contUsoCuchillo/vecesUsoArmas) * 100, (contUsoPistola/vecesUsoArmas) * 100] 
    nombres = ["CUCHILLO","PISTOLA"]
    plt.pie(porcentajesUsoArmas, labels=nombres, autopct="%0.1f %%")
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
    plt.bar([i - 0.2 for i in x], usos, width=0.3, align='center', label='Usos')
    plt.bar([i + 0.2 for i in x], asesinatos, width=0.3, align='center', label='Asesinatos')

    # añadir etiquetas de los ejes y la leyenda
    plt.xlabel('Armas')
    plt.ylabel('Valores')
    plt.xticks(x, armas)
    plt.legend()

    for i, v in enumerate(usos):
        plt.text(i - 0.2, v + 0.5, str(v), color='blue', fontweight='bold', ha='center', va='bottom')
    for i, v in enumerate(asesinatos):
        plt.text(i + 0.2, v + 0.5, str(v), color='orange', fontweight='bold', ha='center', va='bottom')

    # mostrar el gráfico
    plt.show()

    # Distancia enemigo-jugador al matar a un enemigo.
    distanciasMatarEne = []
    # Comprobar que haya el mismo numero de muertes de enemigos que kills haya hecho el jugador
    if(len(event_pos_enemy_dead) == len(event_pos_player_kill)):
        cont = 0
        for evento in event_pos_enemy_dead:
            if(evento.get('timestamp') == event_pos_player_kill[cont].get('timestamp')):
                x1 = event_pos_player_kill[cont].get('posX')
                y1 = event_pos_player_kill[cont].get('posY')

                x2 = evento.get('posX')
                y2 = evento.get('posY')
                distancia = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                info = {
                    'Dist': distancia,
                    'Arma': event_pos_player_kill[cont].get('weapon'),              
                }
                distanciasMatarEne.append(info)
                cont+=1
        

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

