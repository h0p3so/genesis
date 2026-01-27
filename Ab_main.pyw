import tkinter as tk
from tkinter import ttk
import time
import sys
from tkinter import messagebox
from datetime import datetime
import random
import threading


def obtener_fecha():
    FechaExacta = '%d/%m/%Y'
    hoy = datetime.today()
    FechaExacta_f = hoy.strftime(FechaExacta)
    return FechaExacta_f

if True:
    # Esto lo hago en un if, ya que si lo pongo en cualquier otra parte me da error en mi editor
    # Pycharm
    import B_bases as bdbd
    import Ac_main as ac
    import Ae_main as ae
    import C_notificaciones




def obtener_datos_de_preferencias_del_usu():
    # - Sacando preferencias del usuario -
    # - La variable "preferencias_usu_valores" sera una tupla con los valores
    # sobre las preferencias del usuario, si no sabes que campos son los de esa tabla
    # ve al archivo "B_bases", lo que nos importa de esta tupla es el valor 4
    # ya que ese valor contiene el id del usuario

    # Aca llamamos a un metodo que nos retorna todos los valores
    # de la tabla preferencias del usurio, tal vez el mas importante es el valor 4
    # de la lista:

    # Recordar: 1 es si, 0 es no
    # [0] = este valor no sirve en realidad
    # [1] = ¿Creo cuenta?
    # [2] = ¿Quieres mensajes de ayuda?
    # [3] = ¿Quieres que te enviemos correos?
    # [4] = id del usuario en la tabla de usuariosDelAPP

    # Entonces cuando veas que llaman a esta funcion
    # y solo usan el valor 4 de la lista que se retorno, sabran que quieren el id
    instancia_a_las_preferencias_del_usu = bdbd.preferencias_usuario()
    preferencias_usu_valores = instancia_a_las_preferencias_del_usu.extraer()
    return preferencias_usu_valores



class parteAmigos_de_ventana_home():

    def __init__(self, vH, Vamigos, btns = (None, None)):
        self.ventanaHome = vH
        self.ventaamigos = Vamigos

        # Ya saben, este contructor funciona igual que el de la clase
        # "parteHistorial_de_ventana_home"
        self.conjumntoBtns = btns


    def agregarAmigos(self):
        # Escondiendo ventanas padre e hija
        self.ventanaHome.iconify()
        self.ventaamigos.iconify()

        # bloqueando btn
        self.btn_agregaar = self.conjumntoBtns[0]
        self.btn_agregaar['state'] = 'disabled'

        self.ventanaAgregar = tk.Toplevel(self.ventaamigos)
        self.ventanaAgregar.config(bg = '#2a2a2a')
        self.ventanaAgregar.resizable(0,0)
        self.ventanaAgregar.title('Home/Amigos/Agregar')

        def cerrar_x():
            try:
                self.ventanaAgregar.destroy()
                self.ventanaHome.deiconify()
                self.ventaamigos.deiconify()
                self.btn_agregaar['state'] = 'normal'
            except:
                self.btn_agregaar['state'] = 'normal'
                self.ventanaAgregar.destroy()


        self.ventanaAgregar.protocol('WM_DELETE_WINDOW', cerrar_x)
        tk.Label(self.ventanaAgregar, text = '¿Como se llama tu amigo?', font = ('consolas', 13), bg = '#2a2a2a', fg = '#fff').pack(pady = 10, padx = 5)
        self.__nombreAmigo = tk.StringVar(self.ventanaAgregar)

        ttk.Entry(self.ventanaAgregar, textvariable = self.__nombreAmigo, font = ('consolas', 12)).pack(padx = 10)

        # Esta lista sirve para saber que amigos lo rechazaron
        # no podra volver a enviar solicitudes hasta que cierre y habra de nuevo la ventana
        # se usa en la funcion "ver"
        self.amigosFallidos = []

        # Esta variable la usaremos para saber cuantas veces el usuario ha intentado
        # agregar a la misma persona, se usa en la funcion "ver"
        self.intentos_agregar_a_la_misma = 0

        def ver():
            self.llamada_a_la_bd_usuarioAPP = bdbd.manejando_bd_sobre_usuarios_del_app()
            # Esta variabe serviara para saber si el usuario exisiste
            self.listaUsauiros = self.llamada_a_la_bd_usuarioAPP.extraer_nombres_de_usuarios()

            # Aca por decirlo de alguna manera voy a descomprimir la lista, ya que esta tiene tuplas en su
            # interior, entonces al descomprimirla quedara como una lista normal. EJ:
            # sin descomprimir: [('Juan12',), ('Camicas411',)]
            # depues: ['Juan12', Camicas411']
            self.listaNombres_descomprimida = []

            for i in self.listaUsauiros:
                for x in i:
                    self.listaNombres_descomprimida.append(x)

            print(self.listaNombres_descomprimida)
            print(self.amigosFallidos)
            # Este if lo que hace es ver si el nombre que busca el usuario tiene el APP o no
            # Coloco el metodo "capitalize" ya que los nombres de la bd empiezan con mayus
            if self.__nombreAmigo.get().capitalize() in self.listaNombres_descomprimida and self.__nombreAmigo.get() not in self.amigosFallidos:
                print('esta')

                # Como esto no es una red social, y tampoco existen dichos usuarios
                # Lo que voy a hacer para simular esto es generar un numero del cero al diez
                # entnces si me da un numero entre 0 a 5 acepta la solicitud, si da uno mayor no
                self.__acepta = random.randint(0, 10)
                print(self.__acepta)

                if self.__acepta <= 5:

                    try:
                        self.instancia_bd_amigos = bdbd.bd_amigos()
                        fecha_en_que_se_agrego = obtener_fecha()
                        self.instancia_bd_amigos.agregar_nuevo_amigo(self.__nombreAmigo.get(), fecha_en_que_se_agrego)
                        messagebox.showinfo('Home/Amigos/Agregar/Alerta', '¡Genial! ya son amigos :)')
                        self.__nombreAmigo.set('')
                    except:
                        messagebox.showinfo('Home/Amigos/Agregar/Alerta', '¡Upsss!, ya agregaste a esta persona')

                else:
                    messagebox.showinfo('Home/Amigos/Agregar/Alerta', '¡Upsss!, al parecer no han aceptado tu solicitud, intenta mas tarde.')

                    # vemos si el nombre ya se agrego a la lista o no
                    # Esto para no agregar repetidos
                    if self.__nombreAmigo in self.amigosFallidos:
                        pass
                    else:
                        self.amigosFallidos.append(self.__nombreAmigo.get().capitalize())

            else:
                messagebox.showwarning('Home/Amigos/Agregar/Alerta', '¡Upsss! al contacto que intentas agregar no existe, o te rechazo la primera vez que le enviaste la solicitud')
                #self.__nombreAmigo.set('')

            if self.__nombreAmigo.get().capitalize() in self.amigosFallidos:
                print('aca estamos!!!!!!!!!!!!!!')
                print(self.intentos_agregar_a_la_misma)
                self.intentos_agregar_a_la_misma+=1
                if self.intentos_agregar_a_la_misma == 5:
                    print('ya se bloqueo')

                    messagebox.showwarning('Home/Amigos/Agregar/Alerta', 'Cerraremos la cuenta un momento para que no puedas hacer mas spam, no te vayas ;)')

                    self.ventanaHome.destroy()
                    self.ventanaAgregar.destroy()
                    self.ventaamigos.destroy()

                    for espera___ in range(60):
                        time.sleep(1)
                        print(espera___)

                        if espera___ == 59:
                            volverAincio = ventana_home()
                            volverAincio.metodo_principal()


        ttk.Button(self.ventanaAgregar, text = 'Agregar.', command = ver).pack(pady = 10, padx = 5)





    def verAmigos(self):

        # Deshabilitando el boton para que no abran esta ventana mas de una vez
        self.btn_listaAmigos = self.conjumntoBtns[1]
        self.btn_listaAmigos['state'] = 'disabled'

        # Escondiendo ventana Home y ventana Historial (esto para que hayan tantas pantallas)
        self.ventanaHome.iconify()
        self.ventaamigos.iconify()

        self.listaAmigosVentana = tk.Toplevel(self.ventaamigos)
        self.listaAmigosVentana.resizable(0,0)
        self.listaAmigosVentana.title('Home/Amigos/Mis amigos')

        def si_c_cierra():
            try:
                self.listaAmigosVentana.destroy()
                self.ventanaHome.deiconify()
                self.ventaamigos.deiconify()
                self.btn_listaAmigos['state'] = 'normal'
            except:
                self.btn_listaAmigos['state'] = 'normal'
                self.listaAmigosVentana.destroy()


        self.listaAmigosVentana.protocol('WM_DELETE_WINDOW', si_c_cierra)


        self.columnas = ('Amigo', 'Fecha que se agrego')
        self.treeview = ttk.Treeview(self.listaAmigosVentana, height = 10, show = 'headings', columns = self.columnas)
        self.treeview.column('Fecha que se agrego', width = 200, anchor = 'center')
        self.treeview.column('Amigo', width = 200, anchor = 'center')

        self.treeview.heading('Amigo', text = 'Amigo/a')
        self.treeview.heading('Fecha que se agrego', text = 'Fecha que se agrego')
        self.treeview.pack()

        self.insntacia_mil_del_programa_jaja = bdbd.bd_amigos()
        self.resultado_amigos = self.insntacia_mil_del_programa_jaja.extraer_amigos()
        self.resultado_fecha = self.insntacia_mil_del_programa_jaja.extraer_fecha()

        self.cuantoSeRecorre = len(self.resultado_fecha)

        for i in range(self.cuantoSeRecorre):
            self.treeview.insert('', i, values = (self.resultado_amigos[i], self.resultado_fecha[i]))













class parteHistorial_de_ventana_home():

    # En esta clase todos los metodos se llamaran igual que el texto que aparece en cada boton de la ventana
    # Historial, ya que esta clase es el complemeto de aquella ventana.
    # Entonces cuando veas un metodo puedes ir a la clase "ventana_home", al metodo "historial"
    # y mirar el texto de cada boton, veras que cada boton tiene el texto igual a los metodos de esta clase

    # En el constructor pedimos la ventana padre la cual es la Home (la que se abre apenas se inicia sesion)
    # se pide mas que nada para controlar los eventos "iconify" y "deicnonify"
    # Tambien se pide la venta historial que es la que se abre cuando damos clic en el boton
    # del reloj que se encuentra en la ventanaHome, es decir la ventana historial es hija de ventana
    # Home, esta ventana la pedimos para poder eventos algunos son: cuando se cierre, mandarla a la barra de tareas (que se esconda) etc.
    # Y tambien pedimos una tupla con cuatro campos, estos campos de momemento estan en None
    # pero al momento de llamar esta clase la tupla se llenara con cuatro botones, esos botones son los mismos
    # que estan en; Clase: ventana_home()
    #               Metodo: historial()
    # si no sabes de que botones hablo ve a ese metodo ahi estaran organizados, y habara un comentario
    # mas a fondo
    def __init__(self, vHome, vHistorial, btnVH = (None, None, None, None)):
        self.ventanaHome = vHome
        self.ventanaHistorial = vHistorial
        self.botonesDeVentanaHistorial = btnVH
        # Campos de la tupla "botonesDeVentanaHistorial"
        # [0] = Es el boton de buscar registro
        # [1] = Es el boton de hacer registro
        # [2] = Es el boton de borrar registro
        # [3] = Ver todos los registros



    def buscar_registro(self):
        # Deshabilitando el boton para que no abran esta ventana mas de una vez
        self.btn_buscar = self.botonesDeVentanaHistorial[0]
        self.btn_buscar['state'] = 'disabled'

        # Escondiendo ventana Home y ventana Historial (esto para que hayan tantas pantallas)
        self.ventanaHome.iconify()
        self.ventanaHistorial.iconify()

        # Creando/personalizando ventana
        self.ventanaBuscar = tk.Toplevel(self.ventanaHistorial)


        def en_caso_de_cierre():
            try:
                self.ventanaHome.deiconify()
                self.ventanaHistorial.deiconify()
                self.ventanaBuscar.destroy()
                self.btn_buscar['state'] = 'normal'
            except:
                self.ventanaBuscar.destroy()
                self.btn_buscar['state'] = 'normal'

        self.ventanaBuscar.protocol('WM_DELETE_WINDOW', en_caso_de_cierre)
        self.ventanaBuscar.resizable(0, 0)
        self.ventanaBuscar.config(bg = '#2a2a2a')
        self.ventanaBuscar.title('Home/Historial/Buscar')
        self.variable_sobre_id = tk.IntVar(self.ventanaBuscar)

        tk.Label(self.ventanaBuscar, text = 'Escribe el id que quieras buscar.', font = ('consolas', 13), bg = '#2a2a2a', fg = '#fff').pack(pady = 10, padx = 10)
        tk.Entry(self.ventanaBuscar, textvariable = self.variable_sobre_id, font = ('consolas', 12), justify = 'center').pack(pady = 5, padx = 10)
        #self.variable_sobre_id.set(1)

        def buscar():
            print(self.variable_sobre_id.get())
            self.extraerDatos_i = bdbd.bd_dinero()
            # la variable valores puede ser una tupla o puede ser un false
            # ya que al metodo que llama si es que llega a fallar dara False
            self.valores = self.extraerDatos_i.buscar_registro_por_id(self.variable_sobre_id.get())

            if self.valores is False:
                messagebox.showwarning('Home/Historial/Buscar/Alerta', 'No hay un registro con este id, revisa bien')
            else:
                print(self.valores)
                self.mostrarDatos = f'''Este es el registro de la fecha: {self.valores[1]}
                Dinero total: {self.valores[2]}
                Dinero ingresado: {self.valores[3]}
                Dinero retirado: {self.valores[4]}
                Dinero de amigos: {self.valores[5]}
                Dinero para amigos: {self.valores[6]}
                Dinero a fundaciones: {self.valores[7]}
                '''
                messagebox.showinfo('Home/Historial/Buscar/Alerta', self.mostrarDatos)

        ttk.Button(self.ventanaBuscar, text = 'Buscar.', command = buscar).pack(pady = 10, padx = 10)



    def hacer_registro(self):
        # Deshabilitando el boton para que no abran esta ventana mas de una vez
        self.btn_hacer_r = self.botonesDeVentanaHistorial[1]
        self.btn_hacer_r['state'] = 'disabled'

        def extraer_ultimo_registro():
            # Esta funcion extrae el ultimo registro de la tbal dinero
            # y lo retorna, si llega a fallar retorna un False lo cual nos
            # indicara que no hay un registro del cual partir ppara hacer un nuevo
            # registro, valga la redundancia
            try:
                # Sacamos los valores del ultimo registro para hacer una copia de ellos
                self.instancia_a_la_bd = bdbd.bd_dinero()
                self.retorno_tupla = self.instancia_a_la_bd.sacando_registro_de_la_fecha_mas_reciente()

                # Pasamos de tupla a lista
                self.valoresList = list(self.retorno_tupla)


                # como el metodo "sacando_registro_de_la_fecha_mas_reciente" da todo_
                # lo que hay en la ultima fila, la fecha estara repetida si hacemos un registro
                # tal cual nos da los valores, entonces aca cambiare la fecha que nos retorna por la del
                # momento en el que haga el registro
                self.valoresList[1] = obtener_fecha()

                print(self.valoresList[1:])
                return self.valoresList

            except:
                return False

        self.false_o_datos = extraer_ultimo_registro()
        try:
            print(self.false_o_datos[1:])
        except:
            print(self.false_o_datos)

        try:
            # Guardamos los datos mediante una excepcion
            # ya que pueden ocurrir dos fallos
            # 1. La fecha del registro esta repetida
            # 2. No haya un registro del cual partir
            self.__dineroTotal = (self.false_o_datos[3] + self.false_o_datos[5]) - (self.false_o_datos[4] + self.false_o_datos[6] + self.false_o_datos[7])
            print(self.__dineroTotal)
            self.__guardarValores = [self.false_o_datos[1], self.__dineroTotal, self.false_o_datos[3], self.false_o_datos[4], self.false_o_datos[5], self.false_o_datos[6], self.false_o_datos[7]]

            self.instancia_a_la_bd.hacer_registro(self.__guardarValores)
            print('Listo!!!!!!!!!!!!!!')
            messagebox.showinfo('Home/Historial/Hacer/Alerta', 'Registro hecho con exito')
            self.btn_hacer_r['state'] = 'normal'

        except:
            # Recordar que si es false, es porque no hay registros para extraer
            if self.false_o_datos is False:
                print('No hay registros')

                self.instancia_a_tabla_dinero = bdbd.bd_dinero()
                self.instancia_a_tabla_repocitorio = bdbd.repositorio_bd_dinero()

                # sacando valores de la tabla repocitorio
                self.valoresRepo = self.instancia_a_tabla_repocitorio.extraerRegistro()
                print(self.valoresRepo)

                self.__dineroTotal = (self.valoresRepo[3] + self.valoresRepo[5]) - (self.valoresRepo[4] + self.valoresRepo[6] + self.valoresRepo[7])

                self.guardar = [self.valoresRepo[1], self.__dineroTotal, self.valoresRepo[3], self.valoresRepo[4], self.valoresRepo[5], self.valoresRepo[6], self.valoresRepo[7]]
                self.instancia_a_tabla_dinero.hacer_registro(self.guardar)
                self.instancia_a_tabla_repocitorio.borrar_registros()

                self.ventanaHome.destroy()
                self.ventanaHistorial.destroy()
                time.sleep(1)
                volviendoAiniciar = ventana_home()
                volviendoAiniciar.metodo_principal()

            else:
                messagebox.showwarning('Home/Historial/Hacer/Alerta', 'Solo puedes hacer un registro por dia, vuelve mañana.')
                self.btn_hacer_r['state'] = 'normal'



    def borrar_registros(self):
        self.btn_borrar = self.botonesDeVentanaHistorial[2]
        self.btn_borrar['state'] = 'disabled'

        self.question = messagebox.askyesno('Home/Historial/Borrar', '¿Estas seguro de que quieres borrar todos los registros?')

        if self.question:
            try:
                self.instancia_a_tabla_dinero = bdbd.bd_dinero()
                self.instancia_a_tabla_repocitorio = bdbd.repositorio_bd_dinero()

                self.ultimoRegistro = self.instancia_a_tabla_dinero.sacando_registro_de_la_fecha_mas_reciente()

                print(self.ultimoRegistro[1:])

                self.instancia_a_tabla_repocitorio.crearTabla()
                self.instancia_a_tabla_repocitorio.hacer_registro(self.ultimoRegistro[1:])
                self.instancia_a_tabla_dinero.borrar_registros()
                print('exito')

                self.ventanaHome.destroy()
                self.ventanaHistorial.destroy()
                time.sleep(1)
                volviendoAiniciar = ventana_home()
                volviendoAiniciar.metodo_principal()
            except:
                messagebox.showwarning('Home/Historial/Borrar/Alerta', 'No hay registros para borrar')
                self.btn_borrar['state'] = 'normal'


    def ver_todos_registros(self):
        # Deshabilitando el boton para que no abran esta ventana mas de una vez
        self.btn_ver = self.botonesDeVentanaHistorial[3]
        self.btn_ver['state'] = 'disabled'

        # Escondiendo ventana Home y ventana Historial (esto para que hayan tantas pantallas)
        self.ventanaHome.iconify()
        self.ventanaHistorial.iconify()

        self.ventana_registros = tk.Toplevel(self.ventanaHistorial)
        self.ventana_registros.resizable(0, 0)
        self.ventana_registros.title('Home/Historial/Registros')

        def si_c_cierra():
            try:
                self.ventanaHome.deiconify()
                self.ventanaHistorial.deiconify()
                self.ventana_registros.destroy()
                self.btn_ver['state'] = 'normal'
            except:
                self.ventana_registros.destroy()
                self.btn_ver['state'] = 'normal'


        self.ventana_registros.protocol('WM_DELETE_WINDOW', si_c_cierra)

        self.columnas = ('Id', 'Fecha')
        self.treeview = ttk.Treeview(self.ventana_registros, height = 10, show = 'headings', columns = self.columnas)
        self.treeview.column('Id', width = 200, anchor = 'center')
        self.treeview.column('Fecha', width = 200, anchor = 'center')
        self.treeview.heading('Id', text = 'Id')
        self.treeview.heading('Fecha', text = 'Fecha')
        self.treeview.pack()


        self.instancia_a_bd = bdbd.bd_dinero()
        self.listdeFechas = self.instancia_a_bd.extraer_todas_fechas()
        self.Listaid = self.instancia_a_bd.extraer_todos_id()

        self.cuantoSeRecorre = len(self.Listaid)

        for i in range(self.cuantoSeRecorre):
            self.treeview.insert('', i, values = (self.Listaid[i], self.listdeFechas[i]))




class ventana_home():

    def __init__(self):
        self.ventanaHome = tk.Tk()

        # Recordar da una tupla!!
        self.preferencias_usuario = obtener_datos_de_preferencias_del_usu()

        # Botones de la venatana home
        self.btn_historial = tk.Button(self.ventanaHome)
        self.btn_amigos = tk.Button(self.ventanaHome)
        self.btn_retiro_ingreso = tk.Button(self.ventanaHome)
        self.btn_amienviar = tk.Button(self.ventanaHome)
        self.btn_yo = tk.Button(self.ventanaHome)



    def historial(self):
        # Bloqueamos el btn historial para que no abusen de el
        self.btn_historial['state'] = 'disabled'

        # Creando/Personalizando la ventana
        self.ventana_historial = tk.Tk()
        self.ventana_historial.resizable(0, 0)
        self.ventana_historial.config(bg = '#2a2a2a')
        self.ventana_historial.title('Home/Historial')
        def c_cierra():
            self.btn_historial['state'] = 'normal'
            self.ventana_historial.destroy()
        self.ventana_historial.protocol('WM_DELETE_WINDOW', c_cierra)

        tk.Label(self.ventana_historial, text='¿Que quieres hacer?', bg='#2a2a2a', fg='#fff',font=('consolas', 12)).pack(pady=10, padx = 10)

        self.btn_buscr_registro = ttk.Button(self.ventana_historial,
                   text='Buscar registro.',
                   command=lambda: self.instancia_de_procesos_historial.buscar_registro()
                   )
        self.btn_buscr_registro.pack(pady=10)


        self.btn_hacer_registro = ttk.Button(self.ventana_historial,
                   text='Hacer registro.',
                   command = lambda: self.instancia_de_procesos_historial.hacer_registro()
                   )
        self.btn_hacer_registro.pack(pady=10)


        self.btn_borrar_registro = ttk.Button(self.ventana_historial,
                   text='Borrar registros.',
                   command = lambda: self.instancia_de_procesos_historial.borrar_registros()
                   )
        self.btn_borrar_registro.pack(pady=10)


        self.btn_todos_registros = ttk.Button(self.ventana_historial,
                   text='Ver todos los registros.',
                   command = lambda: self.instancia_de_procesos_historial.ver_todos_registros()
                   )
        self.btn_todos_registros.pack(pady=10)

        # Esta tupla agrupa los cuatro botones de esta ventana, para pasarlos como argumento a la siguiente instancia;
        self.tupladeLosBtns = (self.btn_buscr_registro, self.btn_hacer_registro, self.btn_borrar_registro, self.btn_todos_registros)
        self.instancia_de_procesos_historial = parteHistorial_de_ventana_home(self.ventanaHome, self.ventana_historial, self.tupladeLosBtns)

        self.ventana_historial.mainloop()



    def amigos(self):
        # Bloqueamos el btn historial para que no abusen de el
        self.btn_amigos['state'] = 'disabled'

        # Creando/Personalizando la ventana
        self.ventana_amigos = tk.Tk()
        self.ventana_amigos.resizable(0, 0)
        self.ventana_amigos.config(bg='#2a2a2a')
        self.ventana_amigos.title('Home/Amigos')

        def en_caso_de_cierre():
            self.btn_amigos['state'] = 'normal'
            self.ventana_amigos.destroy()

        self.ventana_amigos.protocol('WM_DELETE_WINDOW', en_caso_de_cierre)
        tk.Label(self.ventana_amigos, text='¿Que quieres hacer?', bg='#2a2a2a', fg='#fff',font=('consolas', 12)).pack(pady=10, padx=10)

        self.agregar = ttk.Button(self.ventana_amigos,
                        text = 'Agregar amigos.',
                        command = lambda: self.instancia_de_procesos_amigos.agregarAmigos())
        self.agregar.pack(pady = 10)


        self.veramigos = ttk.Button(self.ventana_amigos,
                        text = 'Ver mis amigos.',
                        command = lambda: self.instancia_de_procesos_amigos.verAmigos())
        self.veramigos.pack(pady = 10)

        self.tuplaBtns = (self.agregar, self.veramigos)
        self.instancia_de_procesos_amigos = parteAmigos_de_ventana_home(self.ventanaHome, self.ventana_amigos, self.tuplaBtns)

        self.ventana_amigos.mainloop()






    def metodo_principal(self):
        # Personalizando la ventana Home
        self.ventanaHome.geometry('320x550+550+100')
        self.ventanaHome.resizable(0,0)
        self.ventanaHome.title('Home')
        self.ventanaHome.config(bg = '#2a2a2a')

        # llamando funcion que crea notificaciones
        hilo_notificaciones = threading.Thread(target=C_notificaciones.encuanto_se_crearNotificacion)
        hilo_notificaciones.start()



        def cerrar_home():
            # Se pregunta si se quiere salir de la ventana Home, y como se supone que es la ventana
            # padre, se deben cerrar TODAS las ventanas. Entonces si se cierra la ventana padre se debe acabr
            # todo_ el programa
            self.pregunta = messagebox.askyesno('Home/Alerta', '¿Seguro que quieres salir?')
            if self.pregunta:
                sys.exit()


        self.ventanaHome.protocol('WM_DELETE_WINDOW', cerrar_home)


        try:
            # Todo_ esto se hace mediante una excepcion ya que puede que no haya ni un solo
            # registro, abajo de este comentario debe haber una lista vacia llamada "valoresLista"
            # esta lista no tienen ningun valor dentro ya que se llenara
            # dependiendo los valores que se obtengan mediante la llamada al metodo
            # "sacando_registro_de_la_fecha_mas_reciente" de la clase "bd_dinero"
            # de igual modo lo puedes ver mas abajo a la hora de acabar del try
            self.valoresLista = []

            # Sacando ultimo registro de la bd para mostrar
            # el dinero con el que cuenta el usuario

            self.instancia_ultimo_registro = bdbd.bd_dinero()
            # Okey, esta variable "valores_registro" sera una tupla con ocho campos
            # [0] = id del campo
            # [1] = Fecha del registro
            # [2] = Dinero total
            # [3] = Dinero Ingresado
            # [4] = Dinero retirado
            # [5] = Dinero de amigos
            # [6] = Dinero para amigos
            # [7] = Dinero hacia fundaciones
            self.valores_registro = self.instancia_ultimo_registro.sacando_registro_de_la_fecha_mas_reciente()

            for valorXvalor in self.valores_registro:
                self.valoresLista.append(valorXvalor)

        except:
            # Si no se cumple en try como ya sabran viene aca y de igual modo se crea la lista vacia
            # todo_ esto para saber si hay un registro en la base de datos el cual mostrar
            # o no, si es que hay se mostraran, sino saldra un mensaje diciendo que no hay registros jaja
            self.valoresLista = []


        if not self.valoresLista:
            tk.Label(self.ventanaHome, text = 'No hay registros.', font = ('consolas', 14), bg = '#2a2a2a', fg = '#fff').pack(pady = 10)

            # Recordar que hay una opcion sobre ver mensajes de ayuda
            # aca vemos si esta activada la opcion
            if self.preferencias_usuario[2] == 1:
                tk.Label(self.ventanaHome, text='Si quieres hacer un registro\nve al boton del reloj.', font=('consolas', 12), bg='#2a2a2a', fg='#fff').pack(pady=40)

        else:
            print(self.valoresLista)

            self.label_fecha = 'Fecha del registro: {}'.format(self.valoresLista[1])
            self.label_dinero_total = 'Dinero total: {}'.format(self.valoresLista[2])
            self.label_dinero_ingresado = 'Dinero ingresado: {}'.format(self.valoresLista[3])
            self.label_dinero_retirado = 'Dinero retirado: {}'.format(self.valoresLista[4])
            self.label_de_amigos = 'Dinero de amigos: {}'.format(self.valoresLista[5])
            self.label_dinero_para_amigos = 'Dinero para amigos: {}'.format(self.valoresLista[6])
            self.label_a_fundaciones = 'Dinero a fundaciones: {}'.format(self.valoresLista[7])

            tk.Label(self.ventanaHome, text = self.label_fecha, font = ('consolas', 13), bg = '#2a2a2a', fg = '#fff').pack(pady = 10, padx = 10)
            tk.Label(self.ventanaHome, text = self.label_dinero_total, font = ('consolas', 13), bg = '#2a2a2a', fg = '#fff').pack(pady = 10, padx = 10)
            tk.Label(self.ventanaHome, text = self.label_dinero_ingresado, font = ('consolas', 13), bg = '#2a2a2a', fg = '#fff').pack(pady = 10, padx = 10)
            tk.Label(self.ventanaHome, text = self.label_dinero_retirado, font = ('consolas', 13), bg = '#2a2a2a', fg = '#fff').pack(pady = 10, padx = 10)
            tk.Label(self.ventanaHome, text=self.label_de_amigos, font=('consolas', 13), bg='#2a2a2a',fg='#fff').pack(pady=10, padx=10)
            tk.Label(self.ventanaHome, text=self.label_dinero_para_amigos, font=('consolas', 13), bg='#2a2a2a', fg='#fff').pack(pady=10, padx=10)
            tk.Label(self.ventanaHome, text=self.label_a_fundaciones, font=('consolas', 13), bg='#2a2a2a', fg='#fff').pack(pady=10, padx=10)


        # diseñando boton del histrial
        self.imagen_reloj = tk.PhotoImage(file='imagnes/btn_reloj.png')
        self.reloj_mejorado = self.imagen_reloj.subsample(12, 12)
        self.btn_historial.config(image = self.reloj_mejorado, bg = '#2a2a2a', cursor = 'hand2', activebackground = '#2a2a2a')
        self.btn_historial.place(x = 10, y = 490)
        self.btn_historial['command'] = self.historial

        # diseñando boton de amigos
        self.imagen_amigo = tk.PhotoImage(file='imagnes/btn_amigo.png')
        self.amigo_mejorado = self.imagen_amigo.subsample(12, 12)
        self.btn_amigos.config(image=self.amigo_mejorado, bg='#2a2a2a', cursor='hand2', activebackground='#2a2a2a')
        self.btn_amigos.place(x=70, y=490)
        self.btn_amigos['command'] = self.amigos

        # diseñando boton retiro e ingreso dinero
        self.imagen_cel = tk.PhotoImage(file = 'imagnes/btn_ingresar_retirar (2).png')
        self.cel_mejorado = self.imagen_cel.subsample(12,12)
        self.btn_retiro_ingreso.config(image = self.cel_mejorado, bg = '#2a2a2a', cursor='hand2', activebackground='#2a2a2a')
        self.btn_retiro_ingreso.place(x = 130, y = 490)

        def llamando_codigo_retiro_ingreso():
            inst = ac.ingreso_retiro(self.ventanaHome, self.btn_retiro_ingreso)
            inst.principal()

        self.btn_retiro_ingreso['command'] = llamando_codigo_retiro_ingreso


        # diseñando boton enviar dinero a amigos
        self.imagen_amienviar = tk.PhotoImage(file='imagnes/btn_enviarAmigos.png')
        self.amienviar_mejorado = self.imagen_amienviar.subsample(12, 12)
        self.btn_amienviar.config(image=self.amienviar_mejorado, bg='#2a2a2a', cursor='hand2',activebackground='#2a2a2a')
        self.btn_amienviar.place(x=190, y=490)

        def llamando_codigo_enviaramigos():
            inst = ac.enviarAmigos(self.ventanaHome, self.btn_amienviar)
            inst.main_()

        self.btn_amienviar['command'] = llamando_codigo_enviaramigos


        # diseñando boton mi usuario
        self.imagen_yo = tk.PhotoImage(file='imagnes/btn_yo.png')
        self.yo_mejorado = self.imagen_yo.subsample(12, 12)
        self.btn_yo.config(image=self.yo_mejorado, bg='#2a2a2a', cursor='hand2',activebackground='#2a2a2a')
        self.btn_yo.place(x=250, y=490)

        def miUsu():
            self.ventanaHome.iconify()
            self.btn_yo['state'] = 'disabled'
            instancia_ = ae.mi_usuario(self.ventanaHome, self.btn_yo)

        self.btn_yo['command'] = miUsu




        self.ventanaHome.mainloop()



#a = ventana_home()
#a.metodo_principal()