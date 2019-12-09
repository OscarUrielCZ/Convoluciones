import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Secuencia:
    def __init__(self, secuencia, origen, tipo):
        self.secuencia = secuencia
        self.origen = origen
        self.tipo = tipo

    def convolusion(self, sec):
        if self.tipo == 'np':
            if sec.tipo == 'np':
                return self.__convolusion_finita(sec)
            else:
                return self.__convolusion_periodica(sec)
        else:
            if sec.tipo == 'np':
                return sec.__convolusion_periodica(self)
            else:
                return self.__convolusion_circular(sec)

    def __convolusion_finita(self, sec):
        todas_sec = []
        for i in sec.secuencia:
            temp_sec = []
            for j in self.secuencia:
                temp_sec.append(i*j)
            todas_sec.append(temp_sec)
        return Secuencia(Secuencia.__suma(Secuencia.__completar_secuencias(todas_sec)), \
            self.origen+sec.origen, sec.tipo)

    def __convolusion_periodica(self, secuencia):           # secuencia es periodica
        conv = self.__convolusion_finita(secuencia)
        secuencia_trozos = Secuencia.separar_trozos(conv.secuencia, len(secuencia.secuencia))
        
        return Secuencia(Secuencia.__suma(secuencia_trozos), \
            (self.origen+secuencia.origen)%len(secuencia.secuencia), 'p')        

    def __convolusion_circular(self, secuencia):
        conv = self.__convolusion_finita(secuencia)
        
        if len(self.secuencia) > len(secuencia.secuencia):  # determinar tamaño de secuencia mayor
            tam_mayor = len(self.secuencia)
        else:
            tam_mayor = len(secuencia.secuencia)
        
        secuencia_trozos = Secuencia.separar_trozos(conv.secuencia, tam_mayor)

        return Secuencia(Secuencia.__suma(secuencia_trozos), \
            (self.origen+secuencia.origen)%len(secuencia.secuencia), 'p')    

    def graficar(self, fig):
        if self.tipo == 'p':
            x = [i for i in range(-25, 26)]
            y = [self.secuencia[(abs(i)-self.origen)%len(self.secuencia)] for i in x]            # lista periodica
        else:
            x = [i for i in range(0-self.origen, len(self.secuencia)-self.origen)]
            y = self.secuencia

        #plt.axhline(0, color='red')
        #plt.axvline(0, color='red')
        #plt.stem(x, y, use_line_collection=True)
        #plt.show()
        # fig.add_subplot(111).stem(x, y, use_line_collection=True)
        fig.clear()
        fig.add_subplot(111).stem(x, y, use_line_collection=True)

    def desplegar_grafica(self):
        if self.tipo == 'p':
            x = [i for i in range(-25, 26)]
            y = [self.secuencia[(abs(i)-(len(self.secuencia)-self.origen))%len(self.secuencia)] for i in x]            # lista periodica
        else:
            x = [i for i in range(0-self.origen, len(self.secuencia)-self.origen)]
            y = self.secuencia
            
        plt.axhline(0, color='red')
        plt.axvline(0, color='red')
        plt.stem(x, y, use_line_collection=True)
        plt.show()

    def resultado(self):
        periodo = ''
        resultado = '{'
        if self.tipo == 'p':
            periodo = '\nperiodo: ' + str(len(self.secuencia))
        for i in range(len(self.secuencia)):
            resultado += str(self.secuencia[i])
            if i != len(self.secuencia)-1:
                resultado += ', '
        resultado += '}'
        origen = f'\nOrigen : {self.origen+1}'
        return resultado + origen + periodo

    @staticmethod
    def __suma(secuencias):
        lista_resultado = []

        for i in range(len(secuencias[0])):
            value = 0
            for lista in secuencias:
                value += lista[i]
            lista_resultado.append(value)

        return lista_resultado

    @staticmethod
    def __completar_secuencias(secuencias):
        inicio = 0
        final = len(secuencias)-1

        for secuencia in secuencias:
            for i in range(inicio):
                secuencia.insert(0, 0)      # agregar en la posición 0 un cero
            for i in range(final):
                secuencia.append(0)         # agregar al final un cero
            inicio += 1
            final -= 1
        return secuencias

    @staticmethod
    def separar_trozos(secuencia, tam_trozo):
        secuencia_trozos = []
        i = 0

        while i < len(secuencia):                   # separar por trozos
            trozo = []
            for j in range(tam_trozo):
                trozo.append(secuencia[i])
                i += 1
                if i >= len(secuencia): 
                    break
            secuencia_trozos.append(trozo)

        len_ocupado = len(secuencia_trozos[-1])     # longitud del último trozo

        for i in range(tam_trozo-len_ocupado):      # llenar con 0's
            secuencia_trozos[-1].append(0)

        return secuencia_trozos