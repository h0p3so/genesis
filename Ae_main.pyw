import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


if True:
    import B_bases as bd
    import D_validadores as valid




class mi_usuario:


    def notificaciones(self):
        self.__que_configurar_ventana.iconify()
        self.__notificaciones_btn['state'] = 'disabled'

        self.verNotificacionesVentana = tk.Toplevel(self.__que_configurar_ventana)
        self.verNotificacionesVentana.title('Home/Mi usuario/Notifaciones')
        self.verNotificacionesVentana.resizable(0, 0)

        def cerrar_la_ultima_del_programa():
            try:
                self.__que_configurar_ventana.deiconify()
                self.ventanaHome.deiconify()
                self.verNotificacionesVentana.destroy()
                self.__notificaciones_btn['state'] = 'normal'
            except:
                self.verNotificacionesVentana.destroy()
                self.__notificaciones_btn['state'] = 'normal'
        self.verNotificacionesVentana.protocol('WM_DELETE_WINDOW', cerrar_la_ultima_del_programa)


        self.columnas = ('Notificacion', 'Fecha')
        self.treeview = ttk.Treeview(self.verNotificacionesVentana, height = 20, show = 'headings', columns = self.columnas)
        self.treeview.column('Notificacion', width = 400, anchor = 'center')
        self.treeview.column('Fecha', width = 400, anchor = 'center')

        self.treeview.heading('Notificacion', text = 'Notificacion/es')
        self.treeview.heading('Fecha', text = 'Fecha')
        self.treeview.pack()

        self.instancia_notificaciones = bd.bd_notificaciones()
        self.__notificaciones_valores = self.instancia_notificaciones.extraer_notificacion_es()
        self.__fechas_valores = self.instancia_notificaciones.extraer_fecha_s()

        self.cuantoSeRecorre = len(self.__fechas_valores)

        for i in range(self.cuantoSeRecorre):
            self.treeview.insert('', i, values = (self.__notificaciones_valores[i], self.__fechas_valores[i]))





    def editar_perfil(self):
        # Escondemos ventanas para que no se vea tanto regero
        self.ventanaHome.iconify()
        self.__que_configurar_ventana.iconify()

        # Sacando id de nuestro usuario, la variable "preferenciasUsu_datos"
        # entonces etentos
        self.preferenciasUsu_i = bd.preferencias_usuario()
        self.preferenciasUsu_datos = self.preferenciasUsu_i.extraer()


        self.__datosHastaElMomento_i = bd.manejando_bd_sobre_usuarios_del_app()
        # Recordar que da una lista con tuplas dentro; [('Juan',), ('Un ejemplo',)]
        # por lo cual ahora la vamos a recorer para que sea una lista normal
        # Esta instancia la hacemos solo para que el usuario vea cuales son sus datos
        self.__datos = self.__datosHastaElMomento_i.extraerTodosValores_porId(self.preferenciasUsu_datos[4])

        self.listaDatos = []

        for i in self.__datos:
            for x in i:
                self.listaDatos.append(x)

        print(self.listaDatos)

        # Personalizando/Creando ventana ------------------------------------------------------------
        self.verDatosVentana = tk.Toplevel(self.__que_configurar_ventana)
        def cerrar():
            try:
                self.ventanaHome.deiconify()
                self.__que_configurar_ventana.deiconify()
                self.verDatosVentana.destroy()
                self.btnClic['state'] = 'normal'
            except:
                self.verDatosVentana.destroy()
                self.btnClic['state'] = 'normal'
        self.verDatosVentana.protocol('WM_DELETE_WINDOW', cerrar)
        self.verDatosVentana.resizable(0,0)
        self.verDatosVentana.config(bg = '#2a2a2a')
        self.verDatosVentana.title('Home/Mi usuario/Datos')
        self.verDatosVentana.geometry('450x300')
        # Personalizando/Creando ventana ------------------------------------------------------------


        tk.Label(self.verDatosVentana, text = 'Estos son tus datos', font = ('consolas', 13), bg = '#2a2a2a', fg = '#fff').place(x = 10, y = 10)


        # Campo nombre ---------------------------------------------------------------------------------------------------------
        tk.Label(self.verDatosVentana, text='Nombre usuario:', font=('consolas', 13), bg='#2a2a2a', fg='#fff').place(x = 10, y = 50)
        self.nombre_usu = tk.StringVar(self.verDatosVentana)
        self.nombre_usu.set(self.listaDatos[1])
        self.campoNombre = tk.Entry(self.verDatosVentana, textvariable = self.nombre_usu, font = ('consolas', 12))
        self.campoNombre.place(x = 10, y = 80)


        # Campo coontraseña ---------------------------------------------------------------------------------------------------------
        tk.Label(self.verDatosVentana, text='Contraseña:', font=('consolas', 13), bg='#2a2a2a', fg='#fff').place(x = 220, y = 50)
        self.contra_usu = tk.StringVar(self.verDatosVentana)
        self.contra_usu.set(self.listaDatos[2])
        self.campoContra = tk.Entry(self.verDatosVentana, textvariable=self.contra_usu, font=('consolas', 12))
        self.campoContra.place(x = 220, y = 80)


        # Campo correo ---------------------------------------------------------------------------------------------------------
        tk.Label(self.verDatosVentana, text='Correo:', font=('consolas', 13), bg='#2a2a2a', fg='#fff').place(x = 10, y = 120)
        self.correo_usu = tk.StringVar(self.verDatosVentana)
        self.correo_usu.set(self.listaDatos[3])
        self.campoCorreo = tk.Entry(self.verDatosVentana, textvariable=self.correo_usu, font=('consolas', 12))
        self.campoCorreo.place(x=10, y=150)


        # Campo Numero ---------------------------------------------------------------------------------------------------------
        tk.Label(self.verDatosVentana, text='Numero:', font=('consolas', 13), bg='#2a2a2a', fg='#fff').place(x=220, y = 120)
        self.numero_usu = tk.StringVar(self.verDatosVentana)
        self.numero_usu.set(self.listaDatos[5])
        self.campoNumero = tk.Entry(self.verDatosVentana, textvariable=self.numero_usu, font=('consolas', 12))
        self.campoNumero.place(x=220, y=150)


        # Agrupamos los campos para manipularlos todos en vez de uno en uno
        self.campos_list = [self.campoNombre, self.campoContra, self.campoCorreo, self.campoNumero]


        # Aca ponemos los campos deshabilitados para que no pueda modificarlos
        # a menos que le den al boton modificar
        for deshabilitar in self.campos_list:
            deshabilitar['state'] = 'disabled'


        # Aca creamos un boton para poder modificar los datos ----------------------------------------------------------
        def modicar_datos_F():
            # Hablitamos el boton "btn_guardar" Esto para que una
            # vez alterados los datos se guarden los cambios
            self.btn_guardar['state'] = 'normal'

            # Hablitamos todos los campos, para que puedan ser modificados
            self.campoNombre['state'] = 'normal'
            self.campoNumero['state'] = 'normal'
            self.campoCorreo['state'] = 'normal'
            self.campoContra['state'] = 'normal'

        self.btn_modificar = ttk.Button(self.verDatosVentana, text = 'Modificar.')
        self.btn_modificar.place(x = 30, y = 200)
        self.btn_modificar['command'] = modicar_datos_F
        # Aca creamos un boton para poder modificar los datos ----------------------------------------------------------


        # Aca creamos un boton para poder guardar los cambios ----------------------------------------------------------
        self.btn_guardar = ttk.Button(self.verDatosVentana, text='Guardar.')
        self.btn_guardar.place(x=110, y=200)

        def guardar_cambios():

            # Creamos la instancia para cambiar los valores si es que pasan la validacion
            cambiar_valores_i = bd.manejando_bd_sobre_usuarios_del_app()

            # aca vemos que campos fueron alterados

            # Nombre +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            if self.nombre_usu.get() != self.listaDatos[1]:

                # self.preferenciasUsu_datos[4]: Es el id de nuestro usuario
                # aclaracion por que usuara mucho aca

                instancia_cambiar_nombre = valid.class_validar_nombre(self.nombre_usu.get())
                # Recordar que el metodo "retorno" da True o False
                estaBien_nombre = instancia_cambiar_nombre.retorno()

                # Sacando todos los nombres de usuario para ver si no esta repetido
                instancia_nombres_delApp = bd.manejando_bd_sobre_usuarios_del_app()
                lista_nombres_ = instancia_nombres_delApp.extraer_nombres_de_usuarios()

                lista_nombres_usuarios_permanente = []

                for i in lista_nombres_:
                    for x in i:
                        lista_nombres_usuarios_permanente.append(x)


                if estaBien_nombre and self.nombre_usu.get() not in lista_nombres_usuarios_permanente:
                    cambiar_valores_i.editar_capo_contra_por_id(self.preferenciasUsu_datos[4], self.nombre_usu.get())
                    messagebox.showinfo('Home/Mi usuario/Datos/Alerta', 'Se ha cambiado exitosamente el nombre de usuario')
                else:
                    messagebox.showwarning('Home/Mi usuario/Datos/Alerta', 'Revisa el nombre y asegurate que tenga numeros, si los tiene posiblemente el nombre ya esta en uso')
            # Nombre +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


            # Contra +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            if self.contra_usu.get() != self.listaDatos[2]:
                instancia_validar_contra = valid.class_validar_contra(self.contra_usu.get())
                estaBien_contra = instancia_validar_contra.contra_alfanumerica_y_retorno()

                if estaBien_contra:
                    cambiar_valores_i.editar_capo_Nombre_por_id(self.preferenciasUsu_datos[4], self.contra_usu.get())
                    messagebox.showinfo('Home/Mi usuario/Datos/Alerta','Se ha cambiado exitosamente la contraseña')

                else:
                    messagebox.showwarning('Home/Mi usuario/Datos/Alerta', 'Asegurate de que la contraseña cuente con una longitud mayor o igual a 10, que tenga mayusculas, signos, numeros y minusculas')
            # Contra +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


            # Correo +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            if self.correo_usu.get() != self.listaDatos[3]:
                instancia_cambiar_correo = valid.class_validar_correo(self.correo_usu.get())
                estaBien_correo = instancia_cambiar_correo.retorno()

                if estaBien_correo:
                    cambiar_valores_i.editar_capo_correo_por_id(self.preferenciasUsu_datos[4], self.correo_usu.get())
                    messagebox.showinfo('Home/Mi usuario/Datos/Alerta', 'Se ha cambiado exitosamente el correo')
                else:
                    messagebox.showwarning('Home/Mi usuario/Datos/Alerta', 'Asegurate de que el correo este bien escrito')
            # Correo +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


            # Numero +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            if self.numero_usu.get() != self.listaDatos[5]:
                instancia_cambiar_numero = valid.class_validaor_prefijo_y_numero('', self.numero_usu.get())
                estaBien_numero = instancia_cambiar_numero.validando_numero_y_retorno()

                if estaBien_numero:
                    cambiar_valores_i.editar_capo_numero_por_id(self.preferenciasUsu_datos[4], self.numero_usu.get())
                    messagebox.showinfo('Home/Mi usuario/Datos/Alerta', 'Se ha cambiado exitosamente el numero.')
                else:
                    messagebox.showwarning('Home/Mi usuario/Datos/Alerta', 'Asegurate de que el numero este bien escrito')
            # Numero +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


        # Estas dos lineas por la sangria se entiende que
        # son parte de la configuracion del boton
        self.btn_guardar['command'] = guardar_cambios
        self.btn_guardar['state'] = 'disabled'
        # Aca creamos un boton para poder guardar los cambios ----------------------------------------------------------





    def __init__(self, ventanaHome, btn):


        self.ventanaHome = ventanaHome
        self.btnClic = btn

        # Creando/Personalizando ventana
        self.__que_configurar_ventana = tk.Tk()
        self.__que_configurar_ventana.config(bg = '#2a2a2a')
        self.__que_configurar_ventana.resizable(0, 0)

        def cerrar_():
            self.__que_configurar_ventana.destroy()
            self.btnClic['state'] = 'normal'
            self.ventanaHome.deiconify()

        self.__que_configurar_ventana.protocol('WM_DELETE_WINDOW', cerrar_)
        self.__que_configurar_ventana.title('Home/Mi usuario')



        tk.Label(self.__que_configurar_ventana, text = '¿Que quieres hacer?', font = ('consolas', 13), bg = '#2a2a2a', fg = '#fff').pack(pady = 10, padx = 10)

        # Creando los dos botones de la ventana
        # los metodos de estos btns estan es esta clase

        self.__editarDatos = ttk.Button(self.__que_configurar_ventana)
        self.__editarDatos.config(text = 'Editar mis datos.')
        self.__editarDatos.pack(pady = 10, padx = 10)
        self.__editarDatos['command'] = self.editar_perfil



        # Extraemos cuantas notificaciones tiene
        # el usuario
        self.__notificaciones_I = bd.preferencias_usuario()
        # El valor que nos interesa es el 5
        self.__valores = self.__notificaciones_I.extraer()



        self.__notificaciones_btn = ttk.Button(self.__que_configurar_ventana)
        self.__notificaciones_btn.config(text='Notificaciones [{}].'.format(self.__valores[5]))
        self.__notificaciones_btn.pack(pady=10, padx=10)
        self.__notificaciones_btn['command'] = self.notificaciones

        self.__que_configurar_ventana.mainloop()