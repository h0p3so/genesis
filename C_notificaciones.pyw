import datetime
import time
import random
from datetime import datetime as dt

if True: import B_bases as bd

def obtener_fecha():
    FechaExacta = '%d/%m/%Y'
    hoy = dt.today()
    FechaExacta_f = hoy.strftime(FechaExacta)
    return FechaExacta_f


def crear_notificacion():
    # Sacando amigos del usuario
    ints_amigos = bd.bd_amigos()
    amigos_ = ints_amigos.extraer_amigos()
    amigos_lista = []

    for i in amigos_:
        for x in i:
            amigos_lista.append(x)

    print(amigos_lista)

    if not amigos_lista:
        print('No hay amigos')
    else:
        # aca escojemos un amigo al azar
        cantidad_de_amigos = len(amigos_lista)
        numero = random.randint(0, cantidad_de_amigos)
        amigo = amigos_lista[numero]

        cantidaDeDinero_a_enviar = [10000, 30000, 50000, 70000, 100000, 300000, 500000, 700000, 1000000]
        queCifra = random.randint(0, 8)
        cantidad_que_se_envia = cantidaDeDinero_a_enviar[queCifra]

        mensaje_notificacion = 'Tu amigo {} te ha enviado {}'.format(amigo, cantidad_que_se_envia)
        print(mensaje_notificacion)

        # Añadiendo notificacion
        agnadir_notificacion_i = bd.bd_notificaciones()
        agnadir_notificacion_i.agnadir(mensaje_notificacion, obtener_fecha())

        # actualizando el numero de notificaciones
        cambiar_N_notificaciones_i = bd.preferencias_usuario()
        datos_de_la_tabla = cambiar_N_notificaciones_i.extraer()
        cambiar_N_notificaciones_i.cambiar_N_notificaciones(datos_de_la_tabla[5]+1)

        # Sacamos los valores de la tabla dinero
        instancia_a_bd_dinero = bd.bd_dinero()
        # Si no sabes que campos tiene la tabla ve "B_bases" > "bd_dinero()" > "crear_tabla_dinero"
        valores_de_la_tabla_dinero = instancia_a_bd_dinero.sacando_registro_de_la_fecha_mas_reciente()

        # Actualizamos el campo dineroTotal
        actualizacion_dineroTotal = cantidad_que_se_envia + valores_de_la_tabla_dinero[2]
        instancia_a_bd_dinero.cambiar_valor_total(actualizacion_dineroTotal, valores_de_la_tabla_dinero[0])

        # Aumentamos el campo dineroEnviadoDeAmigos
        actualizacion_dineroDeAmigos = cantidad_que_se_envia + valores_de_la_tabla_dinero[5]
        instancia_a_bd_dinero.cambiar_valor_deAmigos(actualizacion_dineroDeAmigos, valores_de_la_tabla_dinero[0])

        # Alertando al usuario
        from tkinter import messagebox
        mensaje_notificacion = 'Tu amigo {} te ha enviado {}'.format(amigo, cantidad_que_se_envia)
        print(mensaje_notificacion)
        messagebox.showinfo('¡¡Urra!!', mensaje_notificacion)




        print('ESTA HECHOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO0000000000000000000000')





def encuanto_se_crearNotificacion():

    dia_de_hoy_hora = datetime.datetime.today()
    # Esta variable nos ayudara para escojer un elemento de la lista
    # "hora_de_posibles_notificaciones"
    numero_al_azar = random.randint(1, 15)

    hora_de_posibles_notificaciones = [
        dia_de_hoy_hora + datetime.timedelta(minutes = 3),
        dia_de_hoy_hora + datetime.timedelta(minutes = 2),
        dia_de_hoy_hora + datetime.timedelta(minutes = 4),
        dia_de_hoy_hora + datetime.timedelta(seconds = 140),
        dia_de_hoy_hora + datetime.timedelta(minutes = 4),
        dia_de_hoy_hora + datetime.timedelta(minutes = 3),
        dia_de_hoy_hora + datetime.timedelta(minutes = 10),
        dia_de_hoy_hora + datetime.timedelta(seconds = 15),
        dia_de_hoy_hora + datetime.timedelta(minutes = 12),
        dia_de_hoy_hora + datetime.timedelta(minutes = 12),
        dia_de_hoy_hora + datetime.timedelta(seconds = 1100),
        dia_de_hoy_hora + datetime.timedelta(seconds = 92),
        dia_de_hoy_hora + datetime.timedelta(seconds = 255),
        dia_de_hoy_hora + datetime.timedelta(minutes = 4),
        dia_de_hoy_hora + datetime.timedelta(minutes = 6)
    ]

    hastaQhora = hora_de_posibles_notificaciones[numero_al_azar]
    print(hastaQhora)

    print(dia_de_hoy_hora)

    for i in range(0, 100000000000):
        print(i)
        time.sleep(1)
        aumentandoHorActual = dia_de_hoy_hora + datetime.timedelta(seconds=i)
        print(aumentandoHorActual)

        if aumentandoHorActual == hastaQhora:
            crear_notificacion()
            break