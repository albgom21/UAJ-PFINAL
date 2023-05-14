import telemetria as t
import encuesta_entrevista as e

t.initData()
e.initData()

# OBJETIVOS USO EQUITATIVO ARMAS
print("---OBJETIVOS USO EQUITATIVO ARMAS---")

print("RESULTADOS BUILD A:")
if abs(t.porcentajesTiemposArmasBuilds[0][0] - t.porcentajesTiemposArmasBuilds[0][1]) > 20:
    print("NO ESTAN BALANCEADAS LAS ARMAS SEGUN TELEMETRIA")
else:
    print("SI ESTAN BALANCEADAS LAS ARMAS SEGUN TELEMETRIA")

# if e.balances_armas_build_A[0] >= 50:
#     print("SI ESTAN BALANCEADAS LAS ARMAS SEGUN ENCUESTAS/ENTREVISTAS")
# elif e.balances_armas_build_A[1] >= 50:
#     print("NO ESTAN BALANCEADAS LAS ARMAS SEGUN ENCUESTAS/ENTREVISTAS")
# else:
#     print("DEPENDE DE LAS CIRCUSTANCIAS SEGUN ENCUESTAS/ENTREVISTAS")


print("RESULTADOS BUILD B:")
if abs(t.porcentajesTiemposArmasBuilds[1][0] - t.porcentajesTiemposArmasBuilds[1][1]) > 20:
    print("NO ESTAN BALANCEADAS LAS ARMAS SEGUN TELEMETRIA")
else:
    print("SI ESTAN BALANCEADAS LAS ARMAS SEGUN TELEMETRIA")

# if e.balances_armas_build_B[0] >= 50:
#     print("SI ESTAN BALANCEADAS LAS ARMAS SEGUN ENCUESTAS/ENTREVISTAS")
# elif e.balances_armas_build_B[1] >= 50:
#     print("NO ESTAN BALANCEADAS LAS ARMAS SEGUN ENCUESTAS/ENTREVISTAS")
# else:
#     print("DEPENDE DE LAS CIRCUSTANCIAS SEGUN ENCUESTAS/ENTREVISTAS")

# OBJETIVOS LASER



# OBJETIVOS DIFICULTAD ENEMIGOS



# OBJETIVOS UTILIDAD Y FRECUENCIA DE APUNTADO
    #creo que hace falta guardarse el apuntado en telemetria