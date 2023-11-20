#Proyecto2
#SamuelCarmonaCalvo
#LuciaSomarribasValenzuela

import re

class TablaDeSimbolos:
    def __init__(self):
        self.simbolos = {}

    def insertar(self, nombre, tipo):
        self.simbolos[nombre] = tipo

    def buscar(self, nombre):
        return self.simbolos.get(nombre, None)

    def eliminar(self, nombre):
        if nombre in self.simbolos:
            del self.simbolos[nombre]

class AnalizadorSemantico:
    def __init__(self, tabla_de_simbolos):
        self.tabla_de_simbolos = tabla_de_simbolos
        self.errores = []

    def analizar_codigo(self, codigo_fuente):
        lineas = codigo_fuente.split('\n')
        self.errores = []
        funcion_actual = None

        def reportar_error(mensaje, numero_de_linea):
            self.errores.append(f"Error - Línea {numero_de_linea}: {mensaje}")

        for i, linea in enumerate(lineas, start=1):
            linea = linea.strip()

            # Ignorar líneas vacías
            if not linea:
                continue

            # Verificar declaraciones de variables
            coincidencia = re.match(r'^\s*([a-zA-Z_]\w*)\s*=\s*(.*)$', linea)
            if coincidencia:
                nombre, valor = coincidencia.groups()
                if funcion_actual is None:
                    reportar_error(f"'{nombre}' no está declarado", i)
                else:
                    self.tabla_de_simbolos.insertar(nombre, funcion_actual)
                continue

            # Verificar declaraciones de funciones
            coincidencia = re.match(r'^\s*([a-zA-Z_]\w*)\s+([a-zA-Z_]\w*)\s*\(([^)]*)\)\s*{?$', linea)
            if coincidencia:
                tipo_retorno, nombre_funcion, parametros = coincidencia.groups()
                funcion_actual = nombre_funcion
                continue

            # Verificar sentencias de retorno
            if funcion_actual and linea.startswith("return"):
                if not linea.endswith(';'):
                    reportar_error(f"valor de retorno no coincide con la declaración de '{funcion_actual}'", i)
                continue

            # Verificar sentencias inválidas
            if re.match(r'^\s*(if|while)\s*\(', linea):
                reportar_error(f"Sentencia '{linea.split('(')[0]}' no permitida en este contexto", i)
                continue

            # Verificar sentencias desconocidas
            if re.match(r'^\s*(\w+)\s*\(', linea):
                reportar_error(f"Declaración de función o variable desconocida: {linea.split('(')[0]}", i)
                continue

        return self.errores

def leer_codigo_fuente(ruta_archivo):
    try:
        with open(ruta_archivo, 'r') as archivo:
            codigo_fuente = archivo.read()
        return codigo_fuente
    except FileNotFoundError:
        print(f"El archivo '{ruta_archivo}' no se encontró.")
        return None

if __name__ == "__main__":
    ruta_archivo = "codigo_fuente.txt"  # Reemplaza con la ruta de tu archivo
    codigo_fuente = leer_codigo_fuente(ruta_archivo)

    if codigo_fuente:
        tabla_de_simbolos = TablaDeSimbolos()
        analizador = AnalizadorSemantico(tabla_de_simbolos)
        errores = analizador.analizar_codigo(codigo_fuente)

        if errores:
            for error in errores:
                print(error)
        else:
            print("El código fuente es correcto.")

            
