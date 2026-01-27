import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import smtplib
import threading
from datetime import datetime

if True:
    import B_bases as bd
    import Ad_main as ad


def correos_(mensaje, asunto, destinatario):
    message = 'Subject: {}\n\n{}'.format(asunto, mensaje)
    server = smtplib.SMTP('smtp.gmail.com')
    server.starttls()
    server.login('pruebasdecodigojuandiego8420@gmail.com', 'alitasapanadas2018')
    server.sendmail('pruebasdecodigojuandiego8420@gmail.com', destinatario, message)
    server.quit()

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


class ingreso_retiro():

    def __init__(self, vh, btn):
        self.ventanaHome = vh
        # este hace referencia al boton con un celular y una flecha que aparece en la ventana home
        self.btn_ingreso_retiro = btn

        self.ventana_i_r = tk.Tk()
        self.ingresar_btn = ttk.Button(self.ventana_i_r)
        self.retirar_btn = ttk.Button(self.ventana_i_r)


    def ingresar(self):
        self.ingresar_btn['state'] = 'disabled'
        self.ventanaHome.iconify()
        self.ventana_i_r.iconify()

        self.ingresarVentana = tk.Toplevel(self.ventana_i_r)
        self.ingresarVentana.config(bg = '#2a2a2a')
        self.ingresarVentana.resizable(0, 0)
        self.ingresarVentana.title('Home/Retiros e ingresos/Ingresar')

        def enCasoDeCierre():
            try:
                self.ingresarVentana.destroy()
                self.ventanaHome.deiconify()
                self.ventana_i_r.deiconify()
                self.ingresar_btn['state'] = 'normal'
            except:
                self.ingresarVentana.destroy()
                self.ingresar_btn['state'] = 'normal'


        self.ingresarVentana.protocol('WM_DELETE_WINDOW', enCasoDeCierre)

        tk.Label(self.ingresarVentana, text = '¿Cuanto dinero quieres ingresar?', font = ('consolas', 13), bg = '#2a2a2a', fg = '#fff').pack(pady = 10, padx = 10)

        self.__dineroIngresar = tk.IntVar(self.ingresarVentana)
        self.__campoIngreso = ttk.Entry(self.ingresarVentana, textvariable = self.__dineroIngresar, justify = 'center')
        self.__campoIngreso.pack(pady = 10, padx = 10)

        def listo_para_ingresar():

            if self.__dineroIngresar.get() >= 10000 and self.__dineroIngresar.get() <= 1000000:

                # extraer dinero total > cambiar valor de dinero ingresado > sumar el dinero ingresado al total
                extraerDatosDeDinero = bd.bd_dinero()
                registroMasReciente = extraerDatosDeDinero.sacando_registro_de_la_fecha_mas_reciente()
                print(registroMasReciente)

                # Haciendo suma del dineroIngresado + ingreso, esto para actualizar bd
                nuevoDineroINgresado = registroMasReciente[3] + self.__dineroIngresar.get()
                extraerDatosDeDinero.ingresar_dinero(nuevoDineroINgresado, registroMasReciente[0])

                # Haciendo suma del dineroTotal + ingreso, esto para actualizar bd
                nuevoDineroTotal = registroMasReciente[2]+self.__dineroIngresar.get()
                print(nuevoDineroTotal)
                extraerDatosDeDinero.cambiar_valor_total(nuevoDineroTotal, registroMasReciente[0])

                messagebox.showinfo('Home/Retiros e ingresos/Ingresar/Alerta', '¡Has ingresado {} exitosamente a tu cuenta!, cuando cieeres el APP se veran los cambios :)'.format(self.__dineroIngresar.get()))

            else:
                print('No se puede ingresar menos de 10000')


        ttk.Button(self.ingresarVentana, text = 'Listo', command = listo_para_ingresar ).pack(pady = 10, padx = 10)




    def extraer(self):
        self.retirar_btn['state'] = 'disabled'
        self.ventanaHome.iconify()
        self.ventana_i_r.iconify()

        self.retirarVentana = tk.Toplevel(self.ventana_i_r)
        self.retirarVentana.config(bg='#2a2a2a')
        self.retirarVentana.resizable(0, 0)
        self.retirarVentana.title('Home/Retiros e ingresos/Retirar')

        def enCasoDeCierre_protocolo():
            try:
                self.retirarVentana.destroy()
                self.ventanaHome.deiconify()
                self.ventana_i_r.deiconify()
                self.retirar_btn['state'] = 'normal'
            except:
                self.retirarVentana.destroy()
                self.retirar_btn['state'] = 'normal'


        self.retirarVentana.protocol('WM_DELETE_WINDOW', enCasoDeCierre_protocolo)

        tk.Label(self.retirarVentana, text = '¿Cuantos quieres retirar?', bg = '#2a2a2a', fg = '#fff').pack(pady = 10, padx = 10)

        self.__cuantos = tk.IntVar(self.retirarVentana)
        self.__cuantos.set(0)


        def millon(): self.__cuantos.set(1000000); retiro_valor()
        def setecientos(): self.__cuantos.set(700000); retiro_valor()
        def quinientos(): self.__cuantos.set(500000); retiro_valor()
        def trecientos(): self.__cuantos.set(300000); retiro_valor()
        def cien(): self.__cuantos.set(100000); retiro_valor()
        def setenta(): self.__cuantos.set(70000); retiro_valor()
        def cinquenta(): self.__cuantos.set(50000); retiro_valor()
        def treinta(): self.__cuantos.set(30000); retiro_valor()
        def diez(): self.__cuantos.set(10000); retiro_valor()


        def retiro_valor():
            pregunta = messagebox.askquestion('Home/Retiros e ingresos/Retirar/Alerta', '¿Estas seguro de retirar {}?'.format(self.__cuantos.get()))

            if pregunta:
                extraerDatosDeDinero = bd.bd_dinero()
                registroMasReciente = extraerDatosDeDinero.sacando_registro_de_la_fecha_mas_reciente()
                if self.__cuantos.get() <= registroMasReciente[2]:

                    print(registroMasReciente)
                    self.retirarVentana.destroy()

                    # Sumando el registro de dineroRetirado mas reciente mas el retiro nuevo
                    valorRetirado = self.__cuantos.get() + registroMasReciente[4]
                    extraerDatosDeDinero.retirar_dinero(valorRetirado, registroMasReciente[0])

                    # Actualizando el dinero total; la resta del dineroTotal mas reciente menos el retiro
                    nuevoValor_dineroTotal = registroMasReciente[2] - self.__cuantos.get()
                    extraerDatosDeDinero.cambiar_valor_total(nuevoValor_dineroTotal, registroMasReciente[0])

                    messagebox.showinfo('Home/Retiros e ingresos/Retirar/Alerta', 'Proceso hecho con exito, cierra abre y veras los cambios')

                    # Aca vemos si el usuario al crear su cuenta, selecciono la opcion de
                    # que le envien correos de aviso
                    instan_preferenciasUsu = bd.preferencias_usuario()
                    preferencias_lista = instan_preferenciasUsu.extraer()

                    if preferencias_lista[3] == 1:
                        # Extraer correo del usuario para el aviso
                        extraer_correo_i = bd.manejando_bd_sobre_usuarios_del_app()
                        extraer_correo_real = extraer_correo_i.extraer_correo_por_id(preferencias_lista[4])

                        fecha = obtener_fecha()
                        hora = obtener_hora()
                        mensaje_aviso = 'Has retirado {} el dia {} a la hora {}\nQue tengas un buen dia :)'.format(self.__cuantos.get(), fecha, hora)
                        enviar_aviso_hilo = threading.Thread(target=correos_, args=(mensaje_aviso, 'Hey, Hola!', extraer_correo_real))
                        enviar_aviso_hilo.start()


                    self.ventanaHome.deiconify()
                    self.ventana_i_r.deiconify()
                    self.retirar_btn['state'] = 'normal'



                else:
                    messagebox.showerror('Home/Retiros e ingresos/Retirar/Alerta', 'No tienes esa catidad de dinero')



        ttk.Button(self.retirarVentana, text = '1.000.000', command = millon).pack(pady = 10, padx = 10)
        ttk.Button(self.retirarVentana, text = '700.000'  , command = setecientos).pack(padx = 10)
        ttk.Button(self.retirarVentana, text = '500.000'  , command = quinientos).pack(pady = 10, padx = 10)
        ttk.Button(self.retirarVentana, text = '300.000'  , command = trecientos).pack(padx = 10)
        ttk.Button(self.retirarVentana, text = '100.000'  , command = cien).pack(pady = 10, padx = 10)
        ttk.Button(self.retirarVentana, text = '70.000'   , command = setenta).pack(padx = 10)
        ttk.Button(self.retirarVentana, text = '50.000'   , command = cinquenta).pack(pady = 10, padx = 10)
        ttk.Button(self.retirarVentana, text = '30.000'   , command = treinta).pack(padx = 10)
        ttk.Button(self.retirarVentana, text = '10.000'   , command = diez).pack(pady = 10, padx = 10)


    def principal(self):
        # lo de siempre, deshabilitando el boton para que no abran mas de una vez esto
        self.btn_ingreso_retiro['state'] = 'disabled'

        self.ventana_i_r.config(bg = '#2a2a2a')
        self.ventana_i_r.resizable(0, 0)
        self.ventana_i_r.title('Home/Retiros e ingresos')

        def if_se_cierra():
            self.ventana_i_r.destroy()
            self.btn_ingreso_retiro['state'] = 'normal'

        self.ventana_i_r.protocol('WM_DELETE_WINDOW', if_se_cierra)

        tk.Label(self.ventana_i_r, text = '¿Que quieres hacer?', font = ('consolas', 13), bg = '#2a2a2a', fg = '#fff').pack(pady = 10, padx = 10)

        self.ingresar_btn.config(text = 'Ingresar.', command = self.ingresar)
        self.ingresar_btn.pack(pady = 10, padx = 10)


        self.retirar_btn.config(text='Retirar.', command = self.extraer)
        self.retirar_btn.pack(padx = 10, pady = 10)


        self.ventana_i_r.mainloop()




class enviarAmigos():

    def __init__(self, ventaHome, btn):
        self.ventanaHome = ventaHome
        self.btndeHome = btn
        self.quehacer_ventana = tk.Tk()
        self.enviarAmigosbtn = ttk.Button(self.quehacer_ventana)
        self.enviaRegistros_btn = ttk.Button(self.quehacer_ventana)



    def veRegistros(self):
        self.rgistrosVentana = tk.Toplevel(self.quehacer_ventana)
        self.rgistrosVentana.resizable(0,0)

        def cerrar():
            try:
                self.enviarAmigosbtn['state'] = 'normal'
                self.ventanaHome.deiconify()
                self.quehacer_ventana.deiconify()
                self.rgistrosVentana.destroy()
            except:
                self.rgistrosVentana.destroy()
                self.enviarAmigosbtn['state'] = 'normal'

        self.rgistrosVentana.protocol('WM_DELETE_WINDOW', cerrar)

        self.rgistrosVentana.title('Home/Enviar amigos/Registros')
        self.columnas = ('Para quien', 'Dinero enviado', 'Descripcion', 'Fecha')

        self.arbol = ttk.Treeview(self.rgistrosVentana, height = 15, show = 'headings', columns = self.columnas)

        self.arbol.column('Para quien', width = 200, anchor = 'center')
        self.arbol.column('Dinero enviado', width = 200, anchor = 'center')
        self.arbol.column('Descripcion', width = 200, anchor = 'center')
        self.arbol.column('Fecha', width = 200, anchor = 'center')

        self.arbol.heading('Para quien', text = 'Para quien')
        self.arbol.heading('Dinero enviado', text = 'Dinero enviado')
        self.arbol.heading('Descripcion', text = 'Descripcion')
        self.arbol.heading('Fecha', text = 'Fecha')

        self.arbol.pack()

        self.datos = bd.historial_de_envio_a_amigos()
        self.paraQuienValores = self.datos.extraerDatos_paraQuien()
        self.dineroenviadoValores = self.datos.extraerDatos_DineroEnviado()
        self.descripcionValores = self.datos.extraerDatos_Descripcion()
        self.fechasValores = self.datos.extraerDatos_Fecha()


        self.cuantoSeRecorre = len(self.paraQuienValores)

        for i in range(self.cuantoSeRecorre):
            self.arbol.insert('', i, values = (self.paraQuienValores[i], self.dineroenviadoValores[i], self.descripcionValores[i], self.fechasValores[i]))




    def main_(self):
        self.btndeHome['state'] = 'disabled'

        self.quehacer_ventana.config(bg = '#2a2a2a')
        self.quehacer_ventana.resizable(0,0)
        self.quehacer_ventana.title('Home/Enviar amigos')

        def cerrar():
            self.quehacer_ventana.destroy()
            self.btndeHome['state'] = 'normal'

        self.quehacer_ventana.protocol('WM_DELETE_WINDOW', cerrar)

        tk.Label(self.quehacer_ventana, text = '¿Que quieres hacer?', font = ('consolas', 13), bg = '#2a2a2a', fg = '#fff').pack(pady = 10, padx =10)

        def enviar_dinero():
            self.enviarAmigosbtn['state'] = 'disabled'
            self.ventanaHome.iconify()
            self.quehacer_ventana.iconify()
            llamar_ventana = ad.enviarAmigos_class(self.ventanaHome, self.quehacer_ventana, self.enviarAmigosbtn)

        self.enviarAmigosbtn.config(text = 'Enviar dinero.', command = enviar_dinero)
        self.enviarAmigosbtn.pack(padx = 10, pady = 10)


        def ver_registros():
            self.enviarAmigosbtn['state'] = 'disabled'
            self.ventanaHome.iconify()
            self.quehacer_ventana.iconify()

            self.veRegistros()

        self.enviaRegistros_btn.config(text='Ver registros', command = ver_registros)
        self.enviaRegistros_btn.pack(padx=10, pady=10)


        self.quehacer_ventana.mainloop()