import telemetria as t
import encuesta_entrevista as e
import numpy as np

t.initData()
e.initData()

correlacion = False
correlacionT = False
correlacionE = False

with open('./CorrelacionBuilds.txt', 'w') as file:

    #----------------OBJETIVO USO EQUITATIVO ARMAS----------------
    print("---OBJETIVO USO EQUITATIVO ARMAS---", file=file)
    print("RESULTADOS BUILD A:", file=file)
    if abs(t.porcentajesTiemposArmasBuilds[0][0] - t.porcentajesTiemposArmasBuilds[0][1]) > 20:
        print(" TELEMETRIA: NO ESTAN BALANCEADAS LAS ARMAS", file=file)
        correlacionT = False
    else:
        print(" TELEMETRIA: SI ESTAN BALANCEADAS LAS ARMAS", file=file)
        correlacionT = True

    armaBalanceada = np.argmax(e.porcentaje_balance_armas_build_A)
    armaMasUsada = np.argmax(e.porcentaje_uso_armas_build_A)

    if armaBalanceada == 0 and armaMasUsada == 2:
        print(" ENCUESTAS/ENTREVISTAS: SI ESTAN BALANCEADAS LAS ARMAS", file=file)
        correlacionE = True
    elif armaBalanceada == 1 and armaMasUsada != 2:
        print(" ENCUESTAS/ENTREVISTAS: NO ESTAN BALANCEADAS LAS ARMAS", file=file)
        correlacionE = False
    elif  armaBalanceada == 2 and armaMasUsada == 2:
        print(" ENCUESTAS/ENTREVISTAS: DEPENDE DE LAS CIRCUSTANCIAS", file=file)
        correlacionE = True
    else:
        print(" ENCUESTAS/ENTREVISTAS: NO HAY CORRELACION ENTRE DATOS DE ENCUESTA-ENTREVISTA", file=file)
        correlacionE = False


    if correlacionT == correlacionE:
        print(" EXISTE CORRELACION ENTRE AMBAS MEDICIONES", file=file)
    else:
        print(" NO EXISTE CORRELACION ENTRE AMBAS MEDICIONES", file=file)

    #--------------------------------------------------------------------------------
    
    print("RESULTADOS BUILD B:", file=file)
    if abs(t.porcentajesTiemposArmasBuilds[1][0] - t.porcentajesTiemposArmasBuilds[1][1]) > 20:
        print(" TELEMETRIA: NO ESTAN BALANCEADAS LAS ARMAS", file=file)
        correlacionT = False
    else:
        print(" TELEMETRIA: SI ESTAN BALANCEADAS LAS ARMAS", file=file)
        correlacionT = True

    armaBalanceada = np.argmax(e.porcentaje_balance_armas_build_B)
    armaMasUsada = np.argmax(e.porcentaje_uso_armas_build_B)

    if armaBalanceada == 0 and armaMasUsada == 2:
        print(" ENCUESTAS/ENTREVISTAS: SI ESTAN BALANCEADAS LAS ARMAS", file=file)
        correlacionE = True
    elif armaBalanceada == 1 and armaMasUsada != 2:
        print(" ENCUESTAS/ENTREVISTAS: NO ESTAN BALANCEADAS LAS ARMAS", file=file)
        correlacionE = False
    elif  armaBalanceada == 2 and armaMasUsada == 2:
        print(" ENCUESTAS/ENTREVISTAS: DEPENDE DE LAS CIRCUSTANCIAS", file=file)
        correlacionE = True
    else:
        print(" ENCUESTAS/ENTREVISTAS: NO HAY CORRELACION ENTRE DATOS DE ENCUESTA-ENTREVISTA", file=file)
        correlacionE = False

    if correlacionT == correlacionE:
        print(" EXISTE CORRELACION ENTRE AMBAS MEDICIONES", file=file)
    else:
        print(" NO EXISTE CORRELACION ENTRE AMBAS MEDICIONES", file=file)

    #----------------OBJETIVO LASER Y ENEMIGO----------------
    print("\n", file=file)
    print("---OBJETIVO ENEMIGO VS LASER---", file=file)

    print("RESULTADOS BUILD A:", file=file)
    muertesEneLaserA = abs(t.porcentajesTiposDeMuertesBuilds[0][0] + t.porcentajesTiposDeMuertesBuilds[0][1] - t.porcentajesTiposDeMuertesBuilds[0][2])
    if  (t.porcentajesTiposDeMuertesBuilds[0][1] / muertesEneLaserA)*100 > 20:
        correlacionT = True
        print(" TELEMETRIA: EL LASER RESULTA SER MAS PELIGROSO QUE LOS ENEMIGOS", file=file)
    else:
        correlacionT = False
        print(" TELEMETRIA: LOS ENEMIGOS RESULTAN SER MAS PELIGROSOS QUE LOS LASERES", file=file)

    if e.porcentaje_dificultad_enemigo_laser_build_A[1] >= 50:
        correlacionE = True
        print(" ENCUESTAS/ENTREVISTAS:EL LASER RESULTA SER MAS PELIGROSO QUE LOS ENEMIGOS", file=file)
    else:
        correlacionE = False
        print(" ENCUESTAS/ENTREVISTAS: LOS ENEMIGOS RESULTAN SER MAS PELIGROSOS QUE LOS LASERES", file=file)

    if correlacionT == correlacionE:
        print(" EXISTE CORRELACION ENTRE AMBAS MEDICIONES", file=file)
    else:
        print(" NO EXISTE CORRELACION ENTRE AMBAS MEDICIONES", file=file)

    #--------------------------------------------------------------------------------

    print("RESULTADOS BUILD B:", file=file)
    muertesEneLaserB = abs(t.porcentajesTiposDeMuertesBuilds[1][0] + t.porcentajesTiposDeMuertesBuilds[1][1] - t.porcentajesTiposDeMuertesBuilds[1][2])
    if  (t.porcentajesTiposDeMuertesBuilds[1][1] / muertesEneLaserB)*100 > 20:
        correlacionT = True
        print(" TELEMETRIA: EL LASER RESULTA SER MAS PELIGROSO QUE LOS ENEMIGOS", file=file)
    else:
        correlacionT = False
        print(" TELEMETRIA: LOS ENEMIGOS RESULTAN SER MAS PELIGROSOS QUE LOS LASERES", file=file)

    if e.porcentaje_dificultad_enemigo_laser_build_B[1] >= 50:
        correlacionE = True
        print(" ENCUESTAS/ENTREVISTAS:EL LASER RESULTA SER MAS PELIGROSO QUE LOS ENEMIGOS", file=file)
    else:
        correlacionE = False
        print(" ENCUESTAS/ENTREVISTAS: LOS ENEMIGOS RESULTAN SER MAS PELIGROSOS QUE LOS LASERES", file=file)

    if correlacionT == correlacionE:
        print(" EXISTE CORRELACION ENTRE AMBAS MEDICIONES", file=file)
    else:
        print(" NO EXISTE CORRELACION ENTRE AMBAS MEDICIONES", file=file)
        

    #----------------OBJETIVOS UTILIDAD Y FRECUENCIA DE APUNTADO----------------
    print("\n", file=file)
    print("---OBJETIVOS UTILIDAD Y FRECUENCIA DE APUNTADO---", file=file)

    print("RESULTADOS BUILD A:", file=file)
    porcentajeApuntadoA = t.apuntadoTiempoBuilds[0] / t.pistolaTiempoBuilds[0] * 100
    if porcentajeApuntadoA >= 20:
        print(" TELEMETRIA: SI SE USA EL APUNTADO DE FORMA FRECUENTE", file=file)
        correlacionT = True
    else:
        print(" TELEMETRIA: NO SE USA EL APUNTADO PRÁCTICAMENTE NADA", file=file)
        correlacionT = False

    # if (e.uso_apuntado_build_A[0])

    #--------------------------------------------------------------------------------

    print("RESULTADOS BUILD B:", file=file)
    porcentajeApuntadoB = t.apuntadoTiempoBuilds[1] / t.pistolaTiempoBuilds[1] * 100
    if porcentajeApuntadoB >= 20:
        print(" TELEMETRIA: SI SE USA EL APUNTADO DE FORMA FRECUENTE", file=file)
        correlacionT = True
    else:
        print(" TELEMETRIA: NO SE USA EL APUNTADO PRÁCTICAMENTE NADA", file=file)
        correlacionT = False

    if correlacionT == correlacionE:
        print(" EXISTE CORRELACION ENTRE AMBAS MEDICIONES", file=file)
    else:
        print(" NO EXISTE CORRELACION ENTRE AMBAS MEDICIONES", file=file)