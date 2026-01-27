import re


class class_validar_nombre():

    def __init__(self, nombre):
        self.nombre = [nombre]
        self.nombre_v_f = None

        for i in self.nombre:
            if re.findall('[0-9]$', i) and re.findall('^[a-zA-Z_-]+', i) and re.findall('[^@|.|!|°|¡|¿|?|#|$|%|&]', i) and len(self.nombre[0]) >= 6:
                self.nombre_v_f = True
            else:
                self.nombre_v_f = False

    def retorno(self):
        return self.nombre_v_f


class class_validar_correo():

    def __init__(self, correo):
        self.correo = [correo]
        self.correo_simple = correo
        self.correo_v_f = True
        self.extension = False
        self.vecesArroba = 0

        # diegopatinom@outlook.com
        # carlos.__12_.Bs@gmail.com

        for x in self.correo:
            if re.findall('^[a-zA-Z_-]', x) and re.findall('^(1-9)?', x) and re.findall('[@]', x) and re.findall('[a-z]', x) and re.findall('[^@|.|!|°|¡|¿|?|#|$|%|&]', x):
                self.correo_v_f = True

            if re.findall('.com$', x) or re.findall('.as$', x) or re.findall('.co$', x):
                self.extension = True


        for arrobas in self.correo_simple:
            if arrobas == '@':
                self.vecesArroba+=1

    def retorno(self):
        if self.correo_v_f and self.extension and len(self.correo[0]) >= 12 and self.vecesArroba == 1:
            return True
        else:
            return False


class class_validar_contra():

    def __init__(self, contra):
        self.contrasegna = [contra]
        self.contrasegna_simple = contra

    def contra_alfanumerica_y_retorno(self):
        for i in self.contrasegna:
            if len(self.contrasegna[0]) >= 10 and re.findall('[0-9]', i) and re.findall('[a-z]', i) and re.findall('[A-Z]', i):
                return True
            else:
                return False

    def contra_numeros_y_retorno(self):
        if len(self.contrasegna_simple) >= 10 and self.contrasegna_simple.isdigit():
            return True
        else:
            return False


class class_validaor_prefijo_y_numero():

    def __init__(self, codigo, numero):
        self.prefijo = codigo
        self.numero = numero

    def retorno_prefijo(self):

        if self.prefijo == '+57':
            return 'Colombia'

        elif self.prefijo == '+58':
            return 'Venezuela'

        elif self.prefijo == '+506':
            return 'Costa Rica'

        elif self.prefijo == '+54':
            return 'Argentina'

        elif self.prefijo == '+51':
            return 'Peru'

        elif self.prefijo == '+1':
            return 'Estados Unidos'

        elif self.prefijo == '+58':
            return 'Rusa'


    def validando_numero_y_retorno(self):
        if len(self.numero) == 10 and self.numero.isdigit():
            return True
        else:
            return False