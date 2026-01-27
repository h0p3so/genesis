# Librerias necesarias de instalar: pygame, textblob y gtts
# para instalarlas solo abren la cmd y escriben el comando "pip install 'nombreLibreria'"

from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as ms
import webbrowser
import smtplib
import threading
import time
import random


if True: import B_bases as bd; import D_validadores


def correos_(mensaje, asunto, destinatario):
    message = 'Subject: {}\n\n{}'.format(asunto, mensaje)
    server = smtplib.SMTP('smtp.gmail.com')
    server.starttls()
    server.login('pruebasdecodigojuandiego8420@gmail.com', 'alitasapanadas2018')
    server.sendmail('pruebasdecodigojuandiego8420@gmail.com', destinatario, message)
    server.quit()


# - funcion para obtener la fecha exacta en el momento que se llama.
def obtener_fecha():
    FechaExacta = '%d/%m/%Y'
    hoy = datetime.today()
    FechaExacta_f = hoy.strftime(FechaExacta)
    return FechaExacta_f

def obtener_hora():
    HoraExacta = '%I:%M.%S %p'
    hoy = datetime.today()
    HoraExacta_f = hoy.strftime(HoraExacta)
    return HoraExacta_f




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
    # [5] = Numero de notificaciones

    # Entonces cuando veas que llaman a esta funcion
    # y solo usan el valor 4 de la lista que se retorno, sabran que quieren el id
    instancia_a_las_preferencias_del_usu = bd.preferencias_usuario()
    preferencias_usu_valores = instancia_a_las_preferencias_del_usu.extraer()
    return preferencias_usu_valores


codigo_olvido = None


class ventana_inicio_sesion():

    def __init__(self):

        self.ventana = tk.Tk()
        self.instancia_a_bd_todos_los_usuarios = bd.manejando_bd_sobre_usuarios_del_app()
        self.instancia_a_las_preferencias_del_usu = bd.preferencias_usuario()

        # Botones que se usan durante toda la clase mas no en un solo metodo
        # por eso estan en el constructor
        self.botonLogo_y_calificar = tk.Button(self.ventana)
        self.btn_olvido_datos = tk.Button(self.ventana)
        self.btn_acceder = tk.Button(self.ventana)

        # Variables que contienen los entry
        self.contrase_usuario = tk.StringVar()
        self.nuemero_usuario = tk.StringVar()

        # Esta variable sirve para contar las veces que el usuario a intentado
        # entrar pero fallo, se explica mejor en el metodo "puede_iniciar_o_no"
        self.intentos_ = 0


    def puede_iniciar_o_no(self):
        print(self.contrase_usuario.get())
        print(self.nuemero_usuario.get())

        self.instancia_a_la_base = bd.manejando_bd_sobre_usuarios_del_app()

        id_usu = obtener_datos_de_preferencias_del_usu()
        self.contra_usu_de_bd = self.instancia_a_la_base.extraer_contra_por_id(id_usu[4])
        self.numero_usu_de_bd = self.instancia_a_la_base.extraer_numero_por_id(id_usu[4])

        print(self.contra_usu_de_bd[0])
        print(self.numero_usu_de_bd[0])

        if self.contra_usu_de_bd[0] == self.contrase_usuario.get() and self.numero_usu_de_bd[0] == self.numero_entry.get():

            self.ventana.destroy()
            time.sleep(1)

            import Ab_main
            llamando_alhome = Ab_main.ventana_home()
            llamando_alhome.metodo_principal()

            print('u.u')
        else:
            self.intentos_+=1

            if self.intentos_ == 5:
                # Esta variable sirve por si se siguen cometiendo fallos, la variable
                # tendra la hora exacta en la que se registraron los primeros cinco fallos
                # esta variable tambien se usara cuando hayan muchos fallos ya que se enviara un correo
                # de advertencia al usuario
                self.hora_de_los_cinco_fallos = obtener_hora()

                self.btn_acceder['state'] = 'disabled'
                self.btn_olvido_datos['state'] = 'disabled'
                ms.showwarning('Inicio sesion/Alerta', 'Se bloqueara la cuenta unos segundos ya que has fallado cinco veces')
                for i in range(0, 20):
                    time.sleep(1)
                    print(i)
                self.btn_acceder['state'] = 'normal'
                # Aqui cambio el valor de la variable intentos para que no vuelva a entrar a este if
                # sino que entre a uno donde tenga que esperar mas
                self.intentos_ = 6

            if self.intentos_ == 11:
                self.btn_acceder['state'] = 'disabled'
                self.btn_olvido_datos['state'] = 'disabled'
                ms.showwarning('Inicio sesion/Alerta', 'Se bloqueara la cuenta unos segundos ya que has fallado diez veces contando los intentos de antes')
                for i in range(0, 120):
                    time.sleep(1)
                    print(i)
                self.btn_acceder['state'] = 'normal'
                # Volvemos a modificar el valor de la variable "intentos_" para que no entre en este if ni en el de arriba
                self.intentos_ = 12

            if self.intentos_ == 22:
                # Aca en este if ya le enviaremos un correo al usuario, diciendo que estan intentando entrar a su cuenta

                # Sacando correo del usuario, para poder enviar el correo
                import B_bases
                id_usuario = obtener_datos_de_preferencias_del_usu()
                adverntencia_i = B_bases.manejando_bd_sobre_usuarios_del_app()
                correo = adverntencia_i.extraer_correo_por_id(id_usuario[4])

                # Preparadando el correo
                self.mensaje = f'''
                Estan tratando de entrar a tu cuenta, ten cuidado
                Numero de intentos: {self.intentos_}
                Hora de los cinco primeros fallos: {self.hora_de_los_cinco_fallos}
                '''
                hilo_correo_advertencia = threading.Thread(target=correos_, args=(self.mensaje, 'Hey, cuidado!!', correo,))
                hilo_correo_advertencia.start()


                self.btn_acceder['state'] = 'disabled'
                ms.showwarning('Inicio sesion/Alerta', 'Okey, esto ya no es normal. Ten cuidado con lo que haces...')
                for i in range(0, 320):
                    time.sleep(1)
                    print(i)
                self.btn_acceder['state'] = 'normal'
                self.intentos_ = 40

            if self.intentos_ == 40:
                self.btn_acceder['state'] = 'disabled'
                self.btn_olvido_datos['state'] = 'disabled'




    def complemento_de_se_me_olvidaron_los_datos(self):

        # Destruyo la ventana padre para que no se multiplique la ventana
        self.ventana.destroy()

        self.newContra = tk.Tk()
        self.newContra.config(bg='#2a2a2a')
        self.newContra.resizable(0, 0)
        self.newContra.title('Inicio sesion/Olvido/Nueva contraseña')

        def x_si_c_cierra():
            try:
                self.newContra.destroy()
                llamando_de_nuevo_a_la_vemtana = ventana_inicio_sesion()
                llamando_de_nuevo_a_la_vemtana.main_ventana_inicio_sesion()
            except:
                pass


        self.newContra.protocol('WM_DELTE_WINDOW', x_si_c_cierra)

        tk.Label(self.newContra, text='Crea una nueva contraseña', font=('consolas', 12), bg='#2a2a2a', fg='#fff').pack(pady=10, padx=10)
        self.campoUno = ttk.Entry(self.newContra, font=('consolas', 12), justify='center')
        self.campoUno.focus()
        self.campoUno.pack()

        tk.Label(self.newContra, text='Repite la contraseña', font=('consolas', 12), bg='#2a2a2a', fg='#fff').pack(pady=10, padx=10)
        self.campoDos = ttk.Entry(self.newContra, font=('consolas', 12), justify='center')
        self.campoDos.focus()
        self.campoDos.pack()

        def no_ver_campos():
            self.campoUno['show'] = '-'
            self.campoDos['show'] = '-'

        ttk.Button(self.newContra, text='No ver.', cursor='hand2', command=no_ver_campos).pack(pady=10)

        def listo():
            # importando los validadores
            instancia_para_validar_uno = D_validadores.class_validar_contra(self.campoUno.get())
            retornoDeCampo_uno = instancia_para_validar_uno.contra_alfanumerica_y_retorno()

            instancia_para_validar_dos = D_validadores.class_validar_contra(self.campoDos.get())
            retornoDeCampo_dos = instancia_para_validar_dos.contra_alfanumerica_y_retorno()


            if self.campoUno.get() == self.campoDos.get() and retornoDeCampo_uno and retornoDeCampo_dos:
                id_del_usu = obtener_datos_de_preferencias_del_usu()
                import B_bases
                instancia_para_cambiar_contra = B_bases.manejando_bd_sobre_usuarios_del_app()
                instancia_para_cambiar_contra.editar_capo_contra_por_id(id_del_usu[4], self.campoUno.get())
                ms.showinfo('Inicio sesion/Olvido/Nueva contraseña/Alerta', 'Se ha cambiado correctamente la contraseña, espera mientras actualizamos los datos.')
                self.newContra.destroy()
                time.sleep(2)

                volviendo_al_inicio = ventana_inicio_sesion()
                volviendo_al_inicio.main_ventana_inicio_sesion()

            else:
                ms.showwarning('Inicio sesion/Olvido/Nueva contraseña/Alerta', 'Asegurate de que las contraseñas coincidan, y tambien que tengan mayusculas, minusculas, signos y que tenga mas de ocho caracteres')

        ttk.Button(self.newContra, text='Listo.', command=listo).pack(pady=10)




    def se_me_olvidaron_los_datos(self):
        self.pregunta = ms.askyesno('Inicio sesion/Alerta', '¿Has olviados los datos con los que te registraste?')
        if self.pregunta:

            # Llamando a la funcion que da las preferencias del usuario junto a su id
            self.preferencias_usu_valores = obtener_datos_de_preferencias_del_usu()
            # - Sacando el correo del usuario para saludarlo -
            self.correoDelUsuario = self.instancia_a_bd_todos_los_usuarios.extraer_correo_por_id(self.preferencias_usu_valores[4])

            ms.showinfo('Inicio sesion/Alerta', 'Se te enviara un codigo de cienco digitos al correo que nos otorgaste "{}", espera unos segudnos'.format(self.correoDelUsuario[0]))
            self.btn_olvido_datos['state'] = 'disabled'

            global codigo_olvido
            codigo_olvido = random.randint(999, 10000)
            self.correoConCodigo_hilo = threading.Thread(target = correos_, args = ('Al parecer has olvidado tus datos...',
                                                                                    'Este es tu cofigo {}'.format(codigo_olvido),
                                                                                    self.correoDelUsuario[0]))
            self.correoConCodigo_hilo.start()

            # Creacion de la vetana para introducir el codigo
            self.ventnaCodigo = tk.Toplevel(self.ventana)

            def en_caso_de_cierre():
                try:
                    self.ventnaCodigo.destroy()
                    self.btn_olvido_datos['state'] = 'normal'
                    self.ventana.deiconify()
                except:
                    self.ventnaCodigo.destroy()
                    self.btn_olvido_datos['state'] = 'normal'

            self.ventnaCodigo.protocol('WM_DELETE_WINDOW', en_caso_de_cierre)
            self.ventnaCodigo.title('Inicio sesion/Olvidos')
            self.ventnaCodigo.config(bg='#2a2a2a')
            self.ventnaCodigo.resizable(0, 0)

            tk.Label(self.ventnaCodigo, text='Introduce el codgio que te enviamos', font=('consolas', 12), bg='#2a2a2a',fg='#fff').pack(pady=10, padx=10)
            self.lo_que_escriba_el_usu = tk.IntVar()
            self.introducir_codigo = ttk.Entry(self.ventnaCodigo, font=('consolas', 12), justify='center', textvariable = self.lo_que_escriba_el_usu)
            self.introducir_codigo.focus()
            self.introducir_codigo.pack(pady=10, padx=10)

            def hecho():
                print(codigo_olvido)
                print(self.lo_que_escriba_el_usu.get())

                if codigo_olvido == self.lo_que_escriba_el_usu.get():
                    self.complemento_de_se_me_olvidaron_los_datos()
                else:
                    ms.showwarning('Inicio sesion/Olvidos/Alerta', 'Los codigos no coinciden')
                    self.lo_que_escriba_el_usu.set(0)

            ttk.Button(self.ventnaCodigo, text='Listo', command = hecho).pack(pady=10)



    def calificar_app(self):
        # Se deshabilita el boton para no crear varias ventanas
        self.botonLogo_y_calificar['state'] = 'disabled'

        self.ventana_calificar = tk.Toplevel(self.ventana)
        self.ventana_calificar.config(bg = '#2a2a2a')
        self.ventana_calificar.title('Inicio sesion/Calificar')
        self.ventana_calificar.resizable(0, 0)

        def en_caso_de_cerrar():
            # Si se llega a cerrar la ventana; la destruimos y
            # regresamos al boton "botonLogo_y_calificar" a su estado normal
            self.ventana_calificar.destroy()
            self.botonLogo_y_calificar['state'] = 'normal'

        self.ventana_calificar.protocol('WM_DELETE_WINDOW', en_caso_de_cerrar)
        self.ventana_calificar.geometry('300x200')

        # Guardando las reacciones
        self.mala      = tk.PhotoImage(file = 'imagnes/mal.png')
        self.masomenos = tk.PhotoImage(file = 'imagnes/maso.png')
        self.buena     = tk.PhotoImage(file = 'imagnes/megusta.png')

        tk.Label(self.ventana_calificar, text = 'Califica nuestra APP.', font = ('consolas', 12), bg = '#2a2a2a', fg = '#fff').place(x = 10, y = 10)
        self.gusto = tk.StringVar()

        def def_buena():
            self.gusto.set('buena.')
            eleccion()

        def def_maso():
            self.gusto.set('maso menos.')
            eleccion()

        def def_mala():
            self.gusto.set('mala.')
            eleccion()

        def eleccion():
            tk.Label(self.ventana_calificar,
                     text = 'La aplicacion te parece: {}'.format(self.gusto.get()),
                     font = ('consolas', 10), bg = '#2a2a2a',
                     fg = '#fff', width = 40).place(x = 10, y = 110)

        self.buena_mejorada = self.buena.subsample(18, 18)
        self.btn_buena = tk.Button(self.ventana_calificar, image = self.buena_mejorada, bg = '#2a2a2a', activebackground = '#2a2a2a')
        self.btn_buena['command'] = def_buena
        self.btn_buena.place(x = 20, y = 50)

        self.maso_mejorada = self.masomenos.subsample(18, 18)
        self.btn_maso = tk.Button(self.ventana_calificar, image=self.maso_mejorada, bg='#2a2a2a', activebackground='#2a2a2a')
        self.btn_maso['command'] = def_maso
        self.btn_maso.place(x=140, y=50)

        self.mala_mejorada = self.mala.subsample(20, 20)
        self.btn_mala = tk.Button(self.ventana_calificar, image=self.mala_mejorada, bg='#2a2a2a', activebackground='#2a2a2a')
        self.btn_mala['command'] = def_mala
        self.btn_mala.place(x=243, y=50)

        def gracias_x_calificar():

            if self.gusto.get() == '':
                ms.showwarning('Inicio sesion/Calificar/Alerta', 'No has sellecionado una raccion.')

            elif self.gusto.get() == 'maso menos.' or self.gusto.get() == 'mala.':
                # Se crea una ventana nueva para que el usuario escriba que le gustaria ver en el APP

                # minimizando las demas ventanaas
                self.ventana.iconify()
                self.ventana_calificar.iconify()

                ventana_por_que_no_gustar_jaja = tk.Tk()
                ventana_por_que_no_gustar_jaja.resizable(0, 0)
                ventana_por_que_no_gustar_jaja.geometry('300x300+222+222')
                ventana_por_que_no_gustar_jaja.title('Inicio sesion/Calificar/Que debemos mejorar')

                def si_c_cierra():
                    self.ventana.deiconify()
                    self.ventana_calificar.deiconify()
                    ventana_por_que_no_gustar_jaja.destroy()

                ventana_por_que_no_gustar_jaja.protocol('WM_DELETE_WINDOW', si_c_cierra)

                ttk.Label(ventana_por_que_no_gustar_jaja, text='¿Que debemos mejorar?', font=('consolas', 12)).grid(row=0, column=0, pady=10, padx=10)

                zonatext = tk.Text(ventana_por_que_no_gustar_jaja, width=25, height=10, font=('consolas', 12))
                zonatext.grid(row=1, column=0, padx=5)
                scroll = tk.Scrollbar(ventana_por_que_no_gustar_jaja, command=zonatext.yview)
                scroll.grid(row=1, column=1, sticky="nsew", padx=0)
                zonatext.config(yscrollcommand=scroll.set)

                def done_():
                    propuesta = zonatext.get(1.0, 2.0)
                    hilo_enviar_propuesta = threading.Thread(target = correos_, args = (propuesta, 'Propuesta nueva.', 'pruebasdecodigojuandiego8420@gmail.com',))
                    hilo_enviar_propuesta.start()
                    ms.showinfo('Inicio sesion/Calificar/Que debemos mejorar/alerta', '¡Muchas gracias por tu comentario!, lo tendremos en cuenta')
                    ventana_por_que_no_gustar_jaja.destroy()
                    self.ventana.deiconify()
                    self.ventana_calificar.deiconify()

                ttk.Button(ventana_por_que_no_gustar_jaja, text='Enviar.', command=done_).grid(row=2, column=0, padx=10, pady=10)

            else:
                ms.showinfo('Inicio sesion/Calificar/Alerta', 'Muchas gracias, seguiremos trabajanod para que te guste el doble.')

        self.btn_enviar = ttk.Button(self.ventana_calificar, text = 'Enviar.', command = gracias_x_calificar).place(x = 100, y = 150)
        self.ventana_calificar.mainloop()



    def main_ventana_inicio_sesion(self):

        self.ventana.resizable(0, 0)
        self.ventana.geometry('320x550')
        self.ventana.title('Inico sesion.')
        self.ventana.config(bg = '#2a2a2a')


        self.preferencias_usu_valores = obtener_datos_de_preferencias_del_usu()
        # - Sacando el nombre del usuario para saludarlo -
        self.nombreDelUsuario = self.instancia_a_bd_todos_los_usuarios.extraer_nombre_por_id(self.preferencias_usu_valores[4])
        print(self.nombreDelUsuario[0])


        # Boton con el logo del app, cuando se le de clic al logo
        # se le mandara a otra ventana para que califique el APP
        self.imagen_logo_ruta = tk.PhotoImage(file = 'imagnes/logoapp.png')
        self.mejorando_imagen = self.imagen_logo_ruta.subsample(2, 2)
        self.botonLogo_y_calificar.config(image = self.mejorando_imagen, bg = '#2a2a2a')
        self.botonLogo_y_calificar.config(cursor = 'hand2', activebackground = '#2a2a2a')
        self.botonLogo_y_calificar.place(x = 100, y = 15)
        self.botonLogo_y_calificar.config(command = self.calificar_app)

        # Saludando al usuario
        self.saludo = '¡Hola de nuevo, {}!'.format(self.nombreDelUsuario[0])
        tk.Label(self.ventana, text = self.saludo, font = ('consolas', 14), fg = '#fff', bg = '#2a2a2a').place(x = 10, y = 190)


        # Entry para poner el numero de telefono
        tk.Label(self.ventana, text = 'Numero:', font = ('consolas',12), fg = '#fff', bg = '#2a2a2a').place(x = 10, y = 240)
        self.imagen_usuario = tk.PhotoImage(file = 'imagnes/usuario_inicio_sesion.png')
        self.imagen_usuario_mejora = self.imagen_usuario.subsample(17, 17)
        tk.Label(self.ventana, image = self.imagen_usuario_mejora, bg = '#2a2a2a').place(x = 10, y = 270)
        self.numero_entry = tk.Entry(self.ventana, font = ('consolas', 12), bg = '#2a2a2a', fg = '#fff', width = 25, textvariable = self.nuemero_usuario)
        self.numero_entry.focus()
        self.numero_entry.place(x = 50, y = 275)

        # Entry para poner la contra del usuario

        tk.Label(self.ventana, text = 'Contraseña:', font = ('consolas',12), fg = '#fff', bg = '#2a2a2a').place(x = 10, y = 325)
        self.imagen_contra = tk.PhotoImage(file = 'imagnes/contrasena_inicio_sesion.png')
        self.imagen_contra_mejora = self.imagen_contra.subsample(17, 17)
        tk.Label(self.ventana, image = self.imagen_contra_mejora, bg = '#2a2a2a').place(x = 10, y = 355)
        self.contra_entry = tk.Entry(self.ventana, font = ('consolas', 12), bg = '#2a2a2a', fg = '#fff', width = 25)
        self.contra_entry.config(show = '-', textvariable = self.contrase_usuario)
        self.contra_entry.place(x = 50, y = 355)

        # Boton para ver/no ver el campo contraseña
        def ver():
            # deshabilitando el boton "btnNover" para que no se bugue
            self.btnver['state'] = 'disabled'

            # Mostrando contenido del Entry
            self.vercontra = tk.Entry(self.ventana, textvariable = self.contrase_usuario, font=('consolas', 11), bg='#2a2a2a',fg='#fff')
            self.vercontra.place(x=10, y= 400)
            self.vercontra.config(state = 'disabled')

            def nover():
                self.vercontra.destroy()
                self.btnnoVer.destroy()
                self.btnver['state'] = 'normal'
            # Boton para no ver
            self.btnnoVer = tk.Button(self.ventana, text = 'No ver', font = ('consolas', 8), fg = '#fff', bg = '#2a2a2a', activebackground = '#2a2a2a', activeforeground = '#fff')
            self.btnnoVer.config(command = nover)
            self.btnnoVer.place(x = 210, y = 385)


        self.btnver = tk.Button(self.ventana, text = 'Ver.', font = ('consolas', 8))
        self.btnver.config(command = ver, fg = '#fff', bg = '#2a2a2a', activebackground = '#2a2a2a', activeforeground = '#fff')
        self.btnver.place(x = 265, y = 385)


        # Boton para acceder
        self.btn_acceder.config(
                  text = 'Entrar.',
                  font = ('consolas', 11),
                  bg = '#2a2a2a', fg = '#fff',
                  activebackground = '#2a2a2a',
                  activeforeground = '#fff',
                  command = self.puede_iniciar_o_no)
        self.btn_acceder.place(x = 230, y = 500)

        # Boton por si se le olvidaro sus datos
        self.btn_olvido_datos.config(text='Los olvide.',
                  font=('consolas', 11),
                  bg='#2a2a2a', fg='#fff',
                  activebackground='#2a2a2a',
                  activeforeground='#fff',
                  command = self.se_me_olvidaron_los_datos)
        self.btn_olvido_datos.place(x=15, y=500)

        self.ventana.mainloop()





class ventana_crear_cuenta():

    def __init__(self):
        # Estas variables estan en el constructor ya que seran usadas durante toda la clase, no solo en un metodo
        self.ventana    = tk.Tk()
        self.var_nombre = tk.StringVar()
        self.var_correo = tk.StringVar()
        self.var_contra = tk.StringVar()
        self.var_numero = tk.StringVar()
        self.valorContraDistinta = tk.IntVar()
        self.quePais = ttk.Combobox(self.ventana, width=(5 + 1))


    def ventana_de_preferencias(self, pais):
        self.pais_usu = pais
        self.escoge = tk.Toplevel(self.ventana)
        self.escoge.title('Crear cuenta/preferencias')
        self.escoge.resizable(0, 0)
        self.mensajes_ayuda = tk.IntVar()
        self.enviarme_correos = tk.IntVar()

        ttk.Label(self.escoge, text = 'Escoge lo que quieras para tu APP', font = ('consolas', 16)).grid(row = 0, column = 0)
        tk.Checkbutton(self.escoge, text = 'Mensajes de apoyo para enteder a usar el APP', variable = self.mensajes_ayuda).grid(row = 1, column = 0, pady = 5, padx=10)
        tk.Checkbutton(self.escoge, text = 'Enviarme correos, cuando ocurra algo', variable = self.enviarme_correos).grid(row = 2, column = 0, pady = 5, padx = 10)

        def done():
            self.cambiar_valores = bd.preferencias_usuario()
            # Esta funcion trabaja con los valores de las variables "mensajes_ayuda" y "enviarme_correos"
            # si las variables valen uno es porque estan activadas.

            # Dependiendo sus acciones en la ventana
            # se activaran opciones en el programa
            if self.enviarme_correos.get() == 1 and self.mensajes_ayuda.get() == 1:
                self.cambiar_valores.cambiar_valor_mensajes_ayuda()
                self.cambiar_valores.cambiar_valor_enviarme_correos()
            elif self.enviarme_correos.get() == 1 and self.mensajes_ayuda.get() == 0:
                self.cambiar_valores.cambiar_valor_enviarme_correos()
            elif self.enviarme_correos.get() == 0 and self.mensajes_ayuda.get() == 1:
                self.cambiar_valores.cambiar_valor_mensajes_ayuda()

            # Esta es la llamada al metodo que cambiara
            # el estado de sue cuenta, es decir
            # en la base de datos ya no estara un 0, sino un 1
            # lo que indica que ya tiene una cuenta, tambien se explica
            # en el if __name__ == '__main__'
            self.cambiar_valores.cambiar_valor_creo_cuenta()

            # Aca lo que hacemos es sacar el id del ultimo
            # registro en la base de datos de los usarios del APP
            a = bd.manejando_bd_sobre_usuarios_del_app()
            # Aca lo guardamos en esta variable
            # y luego creamos otra que se llama "id_vdd"
            # el contenido de esta variable sera el resultado de la primera variable
            # (obtener_id) mas uno.
            # El resutado sera el id del nuevo usuario, esto lo hago
            # para cuando tenga que hacer una consulta, sobre su correo, nombre etc
            # ese valor (el de la variable "id_vdd") lo alamaceno
            # en la tabla privada del usuario, la que se llama "preferencias_usuario",
            # que esta en la clase "preferencias_usuario" en el archivo "B_bases"
            obtener_id = a.extraer_ultimo_usuario()
            id_vdd = obtener_id[0]+1
            print(id_vdd)
            self.cambiar_valores.cambiar_valor_id(id_vdd)

            # Creamos una tabla de envios para amigos, donde se llevara el registro de los envios
            historialAmigos = bd.historial_de_envio_a_amigos()
            historialAmigos.crearBase()

            # Creamos tabla notificaciones
            tabla_notificaciones_i = bd.bd_notificaciones()
            tabla_notificaciones_i.crearTabla_noti()

            ms.showinfo('Crear cuenta/preferencias/alerta', '¡Has creado tu cuenta exitosamente!, cierra y vuelve a empezar')

            def guardarDatos():
                # Guradando los datos del usuario en la base de datos donde estan
                # todos los usuarios
                self.guadar_new_usu = bd.manejando_bd_sobre_usuarios_del_app()
                self.guadar_new_usu.ingresar_nuevo_usu(self.var_nombre.get().capitalize(), self.var_contra.get(), self.var_correo.get().lower(), self.pais_usu, self.var_numero.get())
            guardarDatos()


            def crear_bd_amigos_y_dinero():
                # Crea dos tablas mas para que el usuario pueda
                # agregar amigos y tener un registro de su dinero apartir de fechas
                tablaamigos = bd.bd_amigos().crear_tabla_amigos()
                tabladinero = bd.bd_dinero().crear_tabla_dinero(obtener_fecha())

            crear_bd_amigos_y_dinero()



            self.ventana.destroy()

        ttk.Button(self.escoge, text='¡Hecho!', command = done).grid(row = 3, column = 0, pady = 10)




    def la_validacion_fue_correcta(self, pais):
        self.pais_usu = pais
        # Este metodo es complemento del metodo "validar_campos"
        # ya que en ese metodo habia mucho codigo, y podria ser feo de ver

        # Mandando un correo al usuario
        self.mensaje = '''
        Estos son los datos con los que te registraste:
        Nombre de usuario: {}
        Numero de telefono: {}
        Pais: {}
        Fecha de creacion: {}
        Hora de creacion: {}
        '''.format(self.var_nombre.get(), self.var_numero.get(), self.pais_usu, obtener_fecha(), obtener_hora())

        self.asunto = 'Hola, {} has creado tu cuenta con exito!'.format(self.var_nombre.get().capitalize())
        self.enviar_correo_hilo = threading.Thread(target = correos_, args = (self.mensaje, self.asunto, self.var_correo.get().lower(),))
        self.enviar_correo_hilo.start()

        # y ahora para terminar, le decimos al usuario que quiere
        # para su APP, en ese metedodo termina todo sobe crear cuenta
        self.ventana_de_preferencias(self.pais_usu)



    def validar_campos(self):
        # Guardo los valores en una lista para que no me toque llamar cada variable con el metodo "get()", asi sera mas facil leer el codigo
        self.lista_campos = [self.var_nombre.get(), self.var_correo.get(), self.var_contra.get(), self.var_numero.get(), self.valorContraDistinta.get(), self.quePais.get()]

        if self.lista_campos[0] == '' or self.lista_campos[1] == '' or self.lista_campos[2] == '' or self.lista_campos[3] == '':
            ms.showwarning('Crea cuenta/alerta', 'Tienes que llenar todos los campos')
        else:
            import D_validadores as valid
            # - empezaremos a validar los datos
            # - la "i" la final indica instancia

            self.validar_nombre_i = valid.class_validar_nombre(self.lista_campos[0])
            self.retorno_nombre = self.validar_nombre_i.retorno()

            self.validar_correo_i = valid.class_validar_correo(self.lista_campos[1])
            self.retoro_correo = self.validar_correo_i.retorno()

            # - Aca viene la parte del checkbox, si el usuario le ha dado clic la variable
            # - llamada 'valorContraDistinta' valdra uno ya que el usuario quiere una contraseña de solo numeros,
            # - sino dio clic en el checkbox la variable valdra cero por lo cual el usuario quiere
            # - una contraseña alfanumerica, dependiendo de eso se llamara a un metodo o al otro

            if self.lista_campos[4] == 1:
                # - contraseña de solo numeros
                self.validar_contra_i = valid.class_validar_contra(self.lista_campos[2])
                self.retoro_contra = self.validar_contra_i.contra_numeros_y_retorno()
            else:
                # - contraseña alfanumerica
                self.validar_contra_i = valid.class_validar_contra(self.lista_campos[2])
                self.retoro_contra = self.validar_contra_i.contra_alfanumerica_y_retorno()

            self.validar_numero_y_prefijo_i = valid.class_validaor_prefijo_y_numero(self.lista_campos[5], self.lista_campos[3])
            self.retorno_prefijo = self.validar_numero_y_prefijo_i.retorno_prefijo()
            self.retorno_numero = self.validar_numero_y_prefijo_i.validando_numero_y_retorno()

            # - llamando a una clase del archivo "B_bases", esto para saber si el nombre esta repetido o no
            import B_bases as bd
            self.ya_esta_este_nombre_i = bd.manejando_bd_sobre_usuarios_del_app()
            self.lista_de_nombresDeUsuario = self.ya_esta_este_nombre_i.extraer_nombres_de_usuarios()

            # esta lista esta vacia, luego la llenaremos con los nombres que nos retorne el metodo "extraer_nombres_de_usuarios()"
            self.listaDeNombres_new = []

            def descomponiendo_el_retorno():
                for i in self.lista_de_nombresDeUsuario:
                    for j in i:
                        self.listaDeNombres_new.append(j)
            descomponiendo_el_retorno()

            def comprobando_si_el_nombre_esta_o_no():
                # Recordar que todos los datos que el usuario ingresa
                # en la ventana, se guardan en una lista, llamada "lista_campos"

                # Pongo el metodo capitalize ya que si el usuario pone todo
                # en mayusculas este if ira totalmente al else,
                # ya que todos los nombres de la base de datos empiezan con mayuscula
                if self.lista_campos[0].capitalize() in self.listaDeNombres_new:
                    return True
                else:
                    return False


            # - Evaluando los retornos [deben ser todos verdaderos para que pase la prueba]
            if self.retorno_nombre and self.retoro_correo and self.retoro_contra and self.retorno_numero and comprobando_si_el_nombre_esta_o_no() == False:
                # Lo hice en otro metodo para que estuviera mas organizado
                self.la_validacion_fue_correcta(self.retorno_prefijo)

            else:
                ms.showwarning('Crear cuenta/alerta', 'Revisa los campos, puede que esten mal escritos. A continuacion se te notificara de ello.')
                if self.retorno_nombre is False:
                    ms.showwarning('Crear cuenta/alerta', 'Debes tener en cuenta que es un nombre de usuario.\nPor lo cual debes tener en cuenta que tiene que tener numeros.')

                if self.retoro_correo is False:
                    sabes_que_es_un_correo = ms.askyesno('Crear cuenta/alerta', 'El correo esta mal escrito, ¿Sabes que es un correo electronico?')
                    if sabes_que_es_un_correo == False:
                        webbrowser.open_new_tab('https://edu.gcfglobal.org/es/crear-un-correo-electronico/aprende-a-crear-un-correo-gmail/1/')

                if self.retoro_contra is False:
                    ms.showwarning('Crear cuenta/alerta', 'Asegurate de que la contraseña sea segura y supere los diez caracteres.')

                if self.retorno_numero is False:
                    ms.showwarning('Crear cuenta/alerta','Asegurate que el numero tenga diez caracteres.')

                if comprobando_si_el_nombre_esta_o_no():
                    ms.showwarning('Crear cuenta/alerta', 'El nombre que esocgiste ya esta en uso.')



    def main_ventana_crear_cuenta(self):
        # Personalizado ventana
        self.ventana.geometry('320x550')
        self.ventana.resizable(0, 0)
        self.ventana.title('Crea cuenta.')
        self.ventana.config(bg = '#2a2a2a')

        # - mensajes de bienvendida - #
        tk.Label(self.ventana, text = '¡Bienvenido a DCVS!', font = ('consolas', 19), bg = '#2a2a2a', fg = '#fff').pack(pady = 10)
        tk.Label(self.ventana, text='¡Crea una cuenta para empezar!', font=('consolas', 11), bg = '#2a2a2a', fg = '#fff').place(x = 10, y = 70)

        # - Campo para colocar nombre - #
        tk.Label(self.ventana, text='Nombre de usuario:', font=('consolas', 11), bg = '#2a2a2a', fg = '#fff').place(x=10, y=110)
        tk.Entry(self.ventana, font = ('consolas', 12), width = 30, bg = '#2a2a2a', fg = '#fff', textvariable = self.var_nombre).place(x = 10, y = 135)

        # - Campo para colocar correo - #
        tk.Label(self.ventana, text='Correo electronico:', font=('consolas', 11), bg = '#2a2a2a', fg = '#fff').place(x=10, y=180)
        tk.Entry(self.ventana, font=('consolas', 12), width=30, bg='#2a2a2a', fg='#fff', textvariable = self.var_correo).place(x=10, y=205)

        # - Campo para colocar contraseña - #
        tk.Label(self.ventana, text='Crea una contraseña:', font=('consolas', 11), bg = '#2a2a2a', fg = '#fff').place(x=10, y=250)
        campo_contra = tk.Entry(self.ventana, font=('consolas', 12), width=25, bg='#2a2a2a', fg='#fff', textvariable = self.var_contra)
        campo_contra.place(x = 10, y = 275)

        # - Este boton le da la opcion al usuario de no ver lo que ingresa en el campo contraseña - #
        def NOVER():
            campo_contra.config(show = '*')

        tk.Button(self.ventana,
                  text = 'No ver.',
                  bg='#2a2a2a',
                  fg='#fff',
                  font = ('consolas', 10),
                  command = NOVER
        ).place(x = 245, y = 275)


        # este Checkbox sirve como una opcion para saber si el usuario quiere que su contraseña sea mas dificil
        # si activa el checkButton afectara el campo, ya que cambiara algunas cosas (se explica en la parte de validacion de datos)
        def cambioValor_contra():
            # Creo que esto no es necesario explicar
            if self.valorContraDistinta.get() == 1:
                self.mensaje_sobre_contra['text'] = 'Contraseña alfanumerica.'
            else:
                self.mensaje_sobre_contra['text'] = 'Contraseña con solo numeros.'

        self.contra_numeros = tk.Checkbutton(self.ventana, variable=self.valorContraDistinta)
        self.contra_numeros.config(bg = '#2a2a2a', activebackground = '#2a2a2a')
        self.contra_numeros.place(x = 10, y = 300)
        self.contra_numeros.config(command = cambioValor_contra)
        self.mensaje_sobre_contra = tk.Label(self.ventana, text = 'Contraseña con solo numeros.', font = ('consolas', 10))
        self.mensaje_sobre_contra.config(bg = '#2a2a2a', fg = '#fff')
        self.mensaje_sobre_contra.place(x = 30, y = 302)

        # - Campo para colocar Numero - #
        tk.Label(self.ventana, text='Numero telefonico:', font=('consolas', 11), bg='#2a2a2a', fg='#fff').place(x=10, y= 340)
        # Este comboBox servira para saber de que pais es el usuario
        self.quePais.place(x = 10, y = (370-2))
        self.quePais['values'] = ('+57', '+58', '+506', '+54', '+51', '+1', '+7')
        self.quePais.current(0)
        tk.Entry(self.ventana, font=('consolas', 12), width=23, bg='#2a2a2a', fg='#fff', textvariable = self.var_numero).place(x = 75, y = 368)


        tk.Button(self.ventana, text = '¡Listo!', font = ('consolas', 11), bg='#2a2a2a', fg='#fff', cursor = 'hand2', command = self.validar_campos).place(x = 235, y = 500)
        tk.Button(self.ventana,
                  text = 'Ayuda',
                  font = ('consolas', 11),
                  bg='#2a2a2a', fg='#fff',
                  cursor = 'hand2',
                  command = lambda: webbrowser.open_new_tab('https://blog.cobiscorp.com/aplicaciones-moviles')
        ).place(x = 20, y = 500)

        self.ventana.mainloop()



if __name__ == '__main__':

    # Esta es una instancia a una clase del archivo
    # "B_Bases.pyw", la clase se llama "preferencias_usuario"
    # en esta clase se creo una tabla con tres columnas
    # sin incluir el id
    import B_bases as bd
    princpal = bd.preferencias_usuario()
    princpal.crearTabla()

    # Llamamos al metodo para extraer los valores de la tabla
    # esto nos retornara una lista
    extraerValor = princpal.extraer()

    # Evaluamos el segundo campo de la tabla
    # en este campo se puede ver si el usuario
    # ya creo la cuenta, lo especifica con un 1 o 0
    # 1: Ya creo, 0: No creo
    if extraerValor[1] == 0:
        # Entonces si el usuario no ha creado cuenta
        # llamamos a la ventana para crear cuenta
        crea_una_cuenta = ventana_crear_cuenta()
        crea_una_cuenta.main_ventana_crear_cuenta()

    else:
        inicia_sesion = ventana_inicio_sesion()
        inicia_sesion.main_ventana_inicio_sesion()