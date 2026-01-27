import tkinter as tk
from tkinter import ttk
import threading
from textblob import TextBlob
import io
import pygame
from gtts import gTTS
import time
from tkinter import messagebox as ms
from datetime import datetime


if True:
    import B_bases as bd

def voz(texto, lenguaje):
    try:

        with io.BytesIO() as file:
            gTTS(text = texto, lang = lenguaje).write_to_fp(file)
            file.seek(0)
            pygame.mixer.init()
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                continue
    except:
        ms.showerror('Upssssss', 'Culpa nuestra, intenta de nuevo')



def traduc(frase, idioma):
    frase_ = TextBlob(frase)
    traduccion = frase_.translate(to=idioma)
    return traduccion

def detectarIdioma(text):
    idioma = TextBlob(text)
    return idioma.detect_language()


def obtener_fecha():
    FechaExacta = '%d/%m/%Y'
    hoy = datetime.today()
    FechaExacta_f = hoy.strftime(FechaExacta)
    return FechaExacta_f


class enviarAmigos_class:

    def extraerNombreCorreoUsu(self, arg):
        # Bueno este metodo es obvio para que existe

        self.__argumento = arg
        self.__preferencias_i = bd.preferencias_usuario()
        self.__preferencias_valores = self.__preferencias_i.extraer()
        self.__tablaUsuarioApp_i = bd. manejando_bd_sobre_usuarios_del_app()

        if self.__argumento == 'nom':
            self.nombre = self.__tablaUsuarioApp_i.extraer_nombre_por_id(self.__preferencias_valores[4])
            return self.nombre

        if self.__argumento == 'correo':
            self.correo = self.__tablaUsuarioApp_i.extraer_correo_por_id(self.__preferencias_valores[4])
            return self.correo



    def escuchar(self):

        # Este metodo sirve para oir lo que esta en el campo texto
        # realmete solo sirve para hacer el programa mas chevere jaja

        # en estos if analizamos que lenguaje escogio el usuario
        # esto para que lo que vaya a decir suene mas creible
        if self.combo_idiomas.get() == 'Español':
            self.hiloEscuchar = threading.Thread(target = voz, args = (self.zonatext.get('1.0', 'end'), 'es',))
            self.hiloEscuchar.start()


        if self.combo_idiomas.get() == 'Ingles':
            self.hiloEscuchar = threading.Thread(target=voz, args=(self.zonatext.get('1.0', 'end'), 'en',))
            self.hiloEscuchar.start()


        if self.combo_idiomas.get() == 'Ruso':
            self.hiloEscuchar = threading.Thread(target=voz, args=(self.zonatext.get('1.0', 'end'), 'ru',))
            self.hiloEscuchar.start()



    def traduccion(self):
        # Re claro para que sirve el metodo
        # Aca a parte de traducir tambien detectamos el idioma
        # por si no esta escribiendo en español

        # Aca retorna la abreviacion del idioma que esta usando
        # ejemplo:
        # Hi = en
        # Hola = es
        self.__queIdiomaUsa = detectarIdioma(self.zonatext.get('1.0', 'end'))


        # Para español -------------------------------------------------------------------------------------
        if self.__queIdiomaUsa == 'es' and self.combo_idiomas.get() == 'Ingles':
            traduccion_ = traduc(self.zonatext.get('1.0', 'end'), 'en')
            self.zonatext.delete('1.0', 'end')
            time.sleep(0.5)
            self.zonatext.insert('1.0', traduccion_)

        if self.__queIdiomaUsa == 'es' and self.combo_idiomas.get() == 'Ruso':
            traduccion_r = traduc(self.zonatext.get('1.0', 'end'), 'ru')
            self.zonatext.delete('1.0', 'end')
            time.sleep(0.5)
            self.zonatext.insert('1.0', traduccion_r)


        # Para ingles -------------------------------------------------------------------------------------
        if self.__queIdiomaUsa == 'en' and self.combo_idiomas.get() == 'Español':
            traduccion_ = traduc(self.zonatext.get('1.0', 'end'), 'es')
            self.zonatext.delete('1.0', 'end')
            time.sleep(0.5)
            self.zonatext.insert('1.0', traduccion_)

        if self.__queIdiomaUsa == 'en' and self.combo_idiomas.get() == 'Ruso':
            traduccion_r = traduc(self.zonatext.get('1.0', 'end'), 'ru')
            self.zonatext.delete('1.0', 'end')
            time.sleep(0.5)
            self.zonatext.insert('1.0', traduccion_r)


        # Para ruso ---------------------------------------------------------------------------------------
        if self.__queIdiomaUsa == 'ru' and self.combo_idiomas.get() == 'Español':
            traduccion_ = traduc(self.zonatext.get('1.0', 'end'), 'es')
            self.zonatext.delete('1.0', 'end')
            time.sleep(0.5)
            self.zonatext.insert('1.0', traduccion_)

        if self.__queIdiomaUsa == 'ru' and self.combo_idiomas.get() == 'Ingles':
            traduccion_r = traduc(self.zonatext.get('1.0', 'end'), 'en')
            self.zonatext.delete('1.0', 'end')
            time.sleep(0.5)
            self.zonatext.insert('1.0', traduccion_r)


    def enviar(self):

        if self.cuantoEnviar.get() == '' or self.zonatext.get('1.0', 'end') == '':
            ms.showwarning('Home/Enviar a amigos/Alerta', 'No has seleccionado una cifra para enviar')

        else:
            self.__pregunta = ms.askyesno('Home/Enviar a amigos/Alerta', '¿Seguro que quieres enviar {} a {}?'.format(self.cuantoEnviar.get(), self.combo_amigos.get()))
            if self.__pregunta:

                # Sacando total de dinero del usuario, para ver si puede enviar la cifra que quiere
                self.__dineroUsu_i = bd.bd_dinero()
                self.__datosUltimafecha_dinero = self.__dineroUsu_i.sacando_registro_de_la_fecha_mas_reciente()

                if int(self.cuantoEnviar.get()) > self.__datosUltimafecha_dinero[2]:
                    ms.showerror('Home/Enviar a amigos/Alerta', 'No cuentas con la cantidad que quieres enviar.')
                else:

                    # aca restamos lo que se envia al dinero total
                    self.__nuevoDineroTotal = self.__datosUltimafecha_dinero[2] - int(self.cuantoEnviar.get())
                    self.__dineroUsu_i.cambiar_valor_total(self.__nuevoDineroTotal, self.__datosUltimafecha_dinero[0])

                    # añadiendo dinero al campo dinero_para_amigos
                    self.__nuevoValor_dnero_para_amigos = self.__datosUltimafecha_dinero[6] + int(self.cuantoEnviar.get())
                    self.__dineroUsu_i.cambiar_valor_paraMigos(self.__nuevoValor_dnero_para_amigos, self.__datosUltimafecha_dinero[0])


                    # Guardando envio
                    self.guardar_i = bd.historial_de_envio_a_amigos()

                    self.guardar_i.nuevoregistro(self.combo_amigos.get(), self.cuantoEnviar.get(), self.zonatext.get('1.0', 'end'),
                                    obtener_fecha())


                    ms.showinfo('Home/Enviar a amigos/Alerta', 'Se ha enviado correctamente el dinero a tu amigo/a, cuando cierres veras los cambios')





    def __init__(self, ventanaHome, ventanaPregunta, btnEnviar):

        self.ventanaHome = ventanaHome
        self.ventanaPregunta = ventanaPregunta
        self.btn_clic_enviaar = btnEnviar


        self.ventanaEnviarDienro = tk.Tk()
        self.ventanaEnviarDienro.resizable(0,0)
        self.ventanaEnviarDienro.geometry('560x370')
        self.ventanaEnviarDienro.title('Home/Enviar dinero a amigos')

        def cerrar():
            try:
                self.ventanaHome.deiconify()
                self.ventanaPregunta.deiconify()
                self.btn_clic_enviaar['state'] = 'normal'
                self.ventanaEnviarDienro.destroy()
            except:
                self.btn_clic_enviaar['state'] = 'normal'
                self.ventanaEnviarDienro.destroy()

        self.ventanaEnviarDienro.protocol('WM_DELETE_WINDOW', cerrar)


        ttk.Label(self.ventanaEnviarDienro, text = '¿A quien le enviaras dinero?', font = ('consolas', 13)).place(x = 5, y = 5 )

        self.sacar_amigos_i = bd.bd_amigos()
        self.amigos = self.sacar_amigos_i.extraer_amigos()

        self.__amigos_lista = []

        for i in self.amigos:
            for x in i:
                self.__amigos_lista.append(x)

        # Combo de amigos
        tk.Label(self.ventanaEnviarDienro, text = 'Amigo', font = ('consolas', 11)).place(x = 5, y =40)
        self.combo_amigos = ttk.Combobox(self.ventanaEnviarDienro, width = 20, height = 7)
        self.combo_amigos.place(x = 5, y = 65)
        self.combo_amigos['values'] = self.__amigos_lista
        self.combo_amigos['state'] = 'readonly'

        def paraQuien(event):
            self.paraquien['text'] = 'Para: {}'.format(self.combo_amigos.get())

        self.combo_amigos.bind("<<ComboboxSelected>>", paraQuien)
        self.combo_amigos.current(0)


        # Combo de idiomas
        self.idiomaSeleccionado = tk.StringVar()
        tk.Label(self.ventanaEnviarDienro, text='Idioma', font=('consolas', 11)).place(x=170, y=40)
        self.__idiomasDispodibles = ['Español', 'Ingles', 'Ruso']
        self.combo_idiomas = ttk.Combobox(self.ventanaEnviarDienro, width = 18, height = 7)
        self.combo_idiomas['values'] = self.__idiomasDispodibles
        self.combo_idiomas['state'] = 'readonly'
        self.combo_idiomas.current(0)
        self.combo_idiomas.place(x = 170, y = 65)

        def seleccion(event):
            print(self.combo_idiomas.get())
            self.btn_tradu = ttk.Button(self.ventanaEnviarDienro)

            self.btn_tradu.config(text='Traducir a {}'.format(self.combo_idiomas.get()), width = 30)
            self.btn_tradu.place(x=220, y=200)
            self.btn_tradu['command'] = self.traduccion

        self.combo_idiomas.bind("<<ComboboxSelected>>", seleccion)

        # Mensaje para tu amigo
        self.__nombreUsu = self.extraerNombreCorreoUsu('nom')
        tk.Label(self.ventanaEnviarDienro, text='Mensaje:', font=('consolas', 11)).place(x=10, y=110)
        tk.Label(self.ventanaEnviarDienro, text='De: {}'.format(self.__nombreUsu[0])  , font=('helvetica', 7)).place(x=15, y=135)
        self.paraquien = tk.Label(self.ventanaEnviarDienro, font=('helvetica', 7))
        self.paraquien.place(x=15, y=155)

        self.zonatext = tk.Text(self.ventanaEnviarDienro, width=25, height=10, font=('helvetica', 10))
        self.zonatext.place(x = 10, y = 180)
        self.scroll = tk.Scrollbar(self.ventanaEnviarDienro, command=self.zonatext.yview)
        self.scroll.place(x = 190, y = 180)
        self.zonatext.config(yscrollcommand=self.scroll.set)

        # Cuanto se envia
        tk.Label(self.ventanaEnviarDienro, text='Dinero a enviar', font=('consolas', 11)).place(x=340, y=40)
        self.cuntoSepuedeEnviar = [10000, 30000, 50000, 70000, 100000, 300000, 500000, 700000, 1000000]
        self.cuantoEnviar = ttk.Spinbox(self.ventanaEnviarDienro, values=self.cuntoSepuedeEnviar)
        self.cuantoEnviar.place(x=340, y=65)
        self.cuantoEnviar['state'] = 'readonly'


        self.btn_escuchar = ttk.Button(self.ventanaEnviarDienro, text = 'Escuchar', width = 25)
        self.btn_escuchar.place(x = 220, y = 230)
        self.btn_escuchar['command'] = self.escuchar

        self.btn_enviar = ttk.Button(self.ventanaEnviarDienro, text = 'Enviar.', width = 17)
        self.btn_enviar.place(x = 220, y = 260)
        self.btn_enviar['command'] = self.enviar

        self.ventanaEnviarDienro.mainloop()
