import sqlite3


class manejando_bd_sobre_usuarios_del_app():

    def __init__(self):
        self.conexion = sqlite3.connect('F_UsuariosDelApp.db')
        self.cursor = self.conexion.cursor()

    def extraer_nombre_por_id(self, queId):
        self.id = queId
        self.consuta = 'SELECT Nombre FROM usuarosdeAPP WHERE id = {}'.format(self.id)
        self.cursor.execute(self.consuta)
        self.Darvalor = self.cursor.fetchall()
        self.conexion.commit()
        return self.Darvalor[0]

    def extraer_correo_por_id(self, queId):
        self.id = queId
        self.consu = 'SELECT Correo FROM usuarosdeAPP WHERE id = {}'.format(self.id)
        self.cursor.execute(self.consu)
        self.Darvalor = self.cursor.fetchall()
        self.conexion.commit()
        return self.Darvalor[0]

    def extraer_contra_por_id(self, queid):
        self.id = queid
        self.consut = 'SELECT Contra FROM usuarosdeAPP WHERE id = {}'.format(self.id)
        self.cursor.execute(self.consut)
        self.Darvalor = self.cursor.fetchall()
        self.conexion.commit()
        return self.Darvalor[0]

    def extraer_numero_por_id(self, queid):
        self.id = queid
        self.consuta = 'SELECT Numero FROM usuarosdeAPP WHERE id = {}'.format(self.id)
        self.cursor.execute(self.consuta)
        self.Darvalor = self.cursor.fetchall()
        self.conexion.commit()
        return self.Darvalor[0]

    def extraer_nombres_de_usuarios(self):
        self.consulta = 'SELECT Nombre FROM usuarosdeAPP'
        self.cursor.execute(self.consulta)
        self.recojerDatos = self.cursor.fetchall()
        self.conexion.commit()
        return list(self.recojerDatos)




    def extraer_ultimo_usuario(self):
        # este metodo sirve para saber que id tendra el nuevo usuario
        # ya que retornara el id del ultimo registro.
        self.cursor.execute(' SELECT * FROM usuarosdeAPP ORDER BY id DESC LIMIT 1')
        self.resultado = self.cursor.fetchall()
        self.conexion.commit()
        return self.resultado[0]


    def ingresar_nuevo_usu(self, nombre, contra, correo, pais, numero):
        self.values = [nombre, contra, correo, pais, numero]
        self.cursor.execute('INSERT INTO usuarosdeAPP VALUES(NULL, ?, ?, ?, ?, ?)', (self.values))
        self.conexion.commit()


    def editar_capo_contra_por_id(self, queid, Nvalor):
        self.id = queid
        self.valor = Nvalor
        self.cursor.execute("UPDATE usuarosdeAPP SET Contra='" + self.valor + "'WHERE id=" + str(self.id))
        self.conexion.commit()


    def editar_capo_Nombre_por_id(self, queid, Newvalor):
        self.id = queid
        self.valor_nombre = Newvalor
        self.cursor.execute("UPDATE usuarosdeAPP SET Nombre='" + self.valor_nombre + "'WHERE id=" + str(self.id))
        self.conexion.commit()


    def editar_capo_correo_por_id(self, queid, Nuevovalor):
        self.id = queid
        self.valor_correo = Nuevovalor
        self.cursor.execute("UPDATE usuarosdeAPP SET Correo='" + self.valor_correo + "'WHERE id=" + str(self.id))
        self.conexion.commit()


    def editar_capo_numero_por_id(self, queid, Nuevo_valor):
        self.id = queid
        self.valor_numero = Nuevo_valor
        self.cursor.execute("UPDATE usuarosdeAPP SET Numero='" + self.valor_numero + "'WHERE id=" + str(self.id))
        self.conexion.commit()


    def extraerTodosValores_porId(self, id):
        # Sí... Ya se con este metodo hubiera podido extraer todo_ por un id
        # en vez de ir en uno un uno, de igual modo ya casi acabo el programa
        # entonces lo dejare asi
        self.id = id
        self.cursor.execute('SELECT * FROM usuarosdeAPP WHERE id={}'.format(self.id))
        self.__valores = self.cursor.fetchall()
        self.conexion.commit()
        return self.__valores

#a = manejando_bd_sobre_usuarios_del_app()
#print(a.extraerTodosValores_porId(1))



class preferencias_usuario():

    def __init__(self):
        self.conexion = sqlite3.connect('E_BaseDatos')
        self.cursor = self.conexion.cursor()

    def crearTabla(self):
        try:
            self.cursor.execute('''CREATE TABLE preferencias_usuario(
                id INTEGER PRIMARY KEY,
                creo_cuenta INTEGEER,
                mensajes_ayuda INTEGER,
                enviarme_correos INTEGER,
                miIde INTEGER,
                Notificacion INTEGER
            )''')

            self.valores = [0, 0, 0, 0, 0]
            self.cursor.execute('INSERT INTO preferencias_usuario VALUES(NULL, ?, ?, ?, ?, ?)', (self.valores))
            self.conexion.commit()
        except:
            pass

    def extraer(self):
        self.cursor.execute('SELECT * FROM preferencias_usuario')
        self.valores_extraidos = self.cursor.fetchall()

        for i in self.valores_extraidos:
            valores_en_lista = i

        self.conexion.commit()
        return valores_en_lista


    def cambiar_valor_creo_cuenta(self):
        self.cursor.execute('UPDATE preferencias_usuario SET creo_cuenta = 1')
        self.conexion.commit()

    def cambiar_valor_mensajes_ayuda(self):
        self.cursor.execute('UPDATE preferencias_usuario SET mensajes_ayuda = 1')
        self.conexion.commit()

    def cambiar_valor_enviarme_correos(self):
        self.cursor.execute('UPDATE preferencias_usuario SET enviarme_correos = 1')
        self.conexion.commit()

    def cambiar_valor_id(self, id):
        self.id = id
        self.consulta = 'UPDATE preferencias_usuario SET miIde = {}'.format(self.id)
        self.cursor.execute(self.consulta)
        self.conexion.commit()

    def cambiar_N_notificaciones(self, numero):
        self.numero = numero
        self.consulta = 'UPDATE preferencias_usuario SET Notificacion = {}'.format(self.numero)
        self.cursor.execute(self.consulta)
        self.conexion.commit()

    def borrar_base(self):
        # este metodo sirve para cuando el usuario borre su cuenta
        self.cursor.execute('DELETE FROM preferencias_usuario')
        self.valores = [0, 0, 0, 0]
        self.cursor.execute('INSERT INTO preferencias_usuario VALUES(NULL, ?, ?, ?, ?)', (self.valores))
        self.conexion.commit()







class bd_dinero():
    def __init__(self):
        self.conexion = sqlite3.connect('E_BaseDatos')
        self.cursor = self.conexion.cursor()

    def crear_tabla_dinero(self, fechaDecreacion):
        self.fechauno = fechaDecreacion
        self.cursor.execute('''CREATE TABLE dinero(
            id INTEGER PRIMARY KEY,
            Fecha VARCHAR(50) UNIQUE,
            Dinero_total FLOAT,
            Dinero_ingreado FLOAT,
            Dinero_retirado FLOAT,
            Dinero_de_amigos FLOAT,
            Dinero_para_amigos FLOAT,
            Dinero_a_fundaciones FLOAT)
        ''')

        self.valor = [self.fechauno, 0, 0, 0, 0, 0, 0]
        self.cursor.execute('INSERT INTO dinero VALUES(NULL,?,?,?,?,?,?,?)', (self.valor))
        self.conexion.commit()


    def sacando_registro_de_la_fecha_mas_reciente(self):
        self.cursor.execute('SELECT * FROM dinero ORDER BY id ASC')
        self.resultado = self.cursor.fetchall()
        self.conexion.commit()
        for i in self.resultado:
            valores = i
        return valores



    def buscar_registro_por_id(self, id):
        try:
            self.idBuscar = id
            print(self.idBuscar)
            self.cursor.execute("SELECT * FROM dinero WHERE id={}".format(self.idBuscar))
            self.resultado_ = self.cursor.fetchall()
            self.conexion.commit()

            for i in self.resultado_:
                valores = i
            return valores
        except:
            return False

    def hacer_registro(self, datos = [None, None, None, None, None, None, None]):
        # los valores que se piden en la tupla son los mismos que solicita la tabla
        # si no sabes que tabla mira el metodo "crear_tabla_dinero" de esta clase
        self.valores_a_ingresar = datos
        self.cursor.execute('INSERT INTO dinero VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)', (self.valores_a_ingresar))
        self.conexion.commit()


    def borrar_registros(self):
        self.cursor.execute('DELETE FROM dinero')
        self.conexion.commit()


    def extraer_todas_fechas(self):
        self.cursor.execute('SELECT Fecha FROM dinero')
        self.F_i = self.cursor.fetchall()
        self.conexion.commit()
        return self.F_i

    def extraer_todos_id(self):
        self.cursor.execute('SELECT id FROM dinero')
        self.ide_i = self.cursor.fetchall()
        self.conexion.commit()
        return self.ide_i

    def ingresar_dinero(self, Nuevovalor, id):
        self.__nuevo = Nuevovalor
        self.__queId = id
        self.cursor.execute('UPDATE dinero SET Dinero_ingreado={} WHERE id = {}'.format(self.__nuevo, self.__queId))
        self.conexion.commit()

    def retirar_dinero(self, new, ide):
        self.new = new
        self.ide = ide
        self.cursor.execute('UPDATE dinero SET Dinero_retirado={} WHERE id = {}'.format(self.new, self.ide))
        self.conexion.commit()

    def cambiar_valor_total(self, actualizacion, id):
        self.__actu = actualizacion
        self.__id = id
        self.cursor.execute('UPDATE dinero SET Dinero_total={} WHERE id={}'.format(self.__actu, self.__id))
        self.conexion.commit()

    def cambiar_valor_paraMigos(self, actuaizacionn, idee):
        self.actuali = actuaizacionn
        self.idee = idee
        self.cursor.execute('UPDATE dinero SET Dinero_para_amigos={} WHERE id={}'.format(self.actuali, self.idee))
        self.conexion.commit()

    def cambiar_valor_deAmigos(self, actuaizacionn, idee):
        self.actuali_ = actuaizacionn
        self.idee_ = idee
        self.cursor.execute('UPDATE dinero SET Dinero_de_amigos={} WHERE id={}'.format(self.actuali_, self.idee_))
        self.conexion.commit()





class repositorio_bd_dinero():

    def __init__(self):
        self.conexion_r = sqlite3.connect('E_BaseDatos')
        self.cursor_r = self.conexion_r.cursor()


    def crearTabla(self):
        try:
            self.cursor_r.execute('''CREATE TABLE repodinero(
                        id INTEGER PRIMARY KEY,
                        Fecha VARCHAR(50),
                        Dinero_total FLOAT,
                        Dinero_ingreado FLOAT,
                        Dinero_retirado FLOAT,
                        Dinero_de_amigos FLOAT,
                        Dinero_para_amigos FLOAT,
                        Dinero_a_fundaciones FLOAT)
                    ''')
            self.conexion_r.commit()
            print('exito bdbdbdbdbdb')
        except:
            print('ya esta creada')


    def hacer_registro(self, valores = (None, None, None, None, None, None, None)):
        self.datos = valores
        self.cursor_r.execute('INSERT INTO repodinero VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)', (self.datos))
        self.conexion_r.commit()

    def borrar_registros(self):
        self.cursor_r.execute('DELETE FROM repodinero')
        self.conexion_r.commit()

    def extraerRegistro(self):
        self.cursor_r.execute('SELECT * FROM repodinero')
        self.conexion_r.commit()

        for i in self.cursor_r.fetchall():
            values = i
        return values





class bd_amigos:

    def __init__(self):
        self.conexion = sqlite3.connect('E_BaseDatos')
        self.cursor = self.conexion.cursor()

    def crear_tabla_amigos(self):
        self.cursor.execute('''CREATE TABLE amigos(
            id INTEGER PRIMARY KEY,
            Amigos VARCHAR(50) UNIQUE,
            Fecha_que_se_agrego VARCHAR(50)
        )''')

        self.conexion.commit()

    def agregar_nuevo_amigo(self, nombre, fecha):

        self.values = [nombre, fecha]
        self.cursor.execute('INSERT INTO amigos VALUES(NULL, ?, ?)', (self.values))
        self.conexion.commit()

    def extraer_amigos(self):
        self.cursor.execute('SELECT Amigos FROM amigos')
        self.__resiltado = self.cursor.fetchall()
        self.conexion.commit()
        return self.__resiltado

    def extraer_fecha(self):
        self.cursor.execute('SELECT Fecha_que_se_agrego FROM amigos')
        self.__resiltado_ = self.cursor.fetchall()
        self.conexion.commit()
        return self.__resiltado_



class historial_de_envio_a_amigos():

    def __init__(self):
        self.conexion = sqlite3.connect('E_BaseDatos')
        self.cursor = self.conexion.cursor()

    def crearBase(self):
        self.cursor.execute('''CREATE TABLE historialEnvios(
            id INTEGER PRIMARY KEY,
            ParaQuien VARCHAR(50),
            DineroEnviado FLOAT,
            Descripcion VARCHAR(1000),
            Fecha VARCHAR(10)
        )''')

        self.conexion.commit()


    def nuevoregistro(self, amigo, dinero, descrip,fecha):
        self.values = [amigo, dinero, descrip, fecha]
        self.cursor.execute('INSERT INTO historialEnvios VALUES(NULL, ?,?,?,?)', (self.values))
        self.conexion.commit()


    def extraerDatos_paraQuien(self):
        self.cursor.execute('SELECT ParaQuien FROM historialEnvios')
        self.valores = self.cursor.fetchall()
        self.conexion.commit()
        return self.valores


    def extraerDatos_DineroEnviado(self):
        self.cursor.execute('SELECT DineroEnviado FROM historialEnvios')
        self.valores = self.cursor.fetchall()
        self.conexion.commit()
        return self.valores

    def extraerDatos_Descripcion(self):
        self.cursor.execute('SELECT Descripcion FROM historialEnvios')
        self.valores = self.cursor.fetchall()
        self.conexion.commit()
        return self.valores

    def extraerDatos_Fecha(self):
        self.cursor.execute('SELECT Fecha FROM historialEnvios')
        self.valores = self.cursor.fetchall()
        self.conexion.commit()
        return self.valores




class bd_notificaciones:

    def __init__(self):
        self.conexion_n = sqlite3.connect('NotificacionesUsu')
        self.cursor_n = self.conexion_n.cursor()


    def crearTabla_noti(self):
        self.cursor_n.execute('''CREATE TABLE notificaciones(
            id INTEGER PRIMARY KEY,
            Notificacion VARCHAR(1000),
            Fecha VARCHAR(10)
        )''')
        self.conexion_n.commit()


    def agnadir(self, Notificacion, fecha):
        self.__valores = [Notificacion, fecha]
        self.cursor_n.execute('INSERT INTO notificaciones VALUES(NULL, ?, ?)', (self.__valores))
        self.conexion_n.commit()


    def extraer_notificacion_es(self):
        self.cursor_n.execute('SELECT Notificacion FROM notificaciones')
        self.valores = self.cursor_n.fetchall()
        self.conexion_n.commit()
        return self.valores


    def extraer_fecha_s(self):
        self.cursor_n.execute('SELECT Fecha FROM notificaciones')
        self.valores_ = self.cursor_n.fetchall()
        self.conexion_n.commit()
        return self.valores_