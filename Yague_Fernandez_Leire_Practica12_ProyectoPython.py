import json  # importo la librería json
import os  # importo la librería os para interactuar con el sistema de archivos
import random  # importo random para seleccionar palabras aleatorias
from collections import defaultdict  # importo defaultdict para agrupar palabras por categoría
from googletrans import Translator  # importo Translator para traducción automática

class Palabra:
    def __init__(self, palabra_original, traduccion, categoria, aprendida=False):  
        self.palabra_original = palabra_original  # almaceno la palabra original
        self.traduccion = traduccion  # almaceno la traducción de la palabra
        self.categoria = categoria  # almaceno la categoría de la palabra
        self.aprendida = aprendida  # indico si la palabra ha sido aprendida o no

    def marcar_como_aprendida(self):  
        self.aprendida = True  # cambio el estado de la palabra a aprendida

    def mostrar_datos_palabra(self):  
        return f"{self.palabra_original} - {self.traduccion} ({'Aprendida' if self.aprendida else 'No aprendida'})"  # devuelvo los detalles

class Usuario:
    def __init__(self, nombre):  
        self.nombre = nombre  # guardo el nombre del usuario
        self.vocabulario = []  # inicializo el vocabulario del usuario como una lista vacía
        self.cargar_vocabulario()  # llamo al método para cargar el vocabulario del archivo json

    def cargar_vocabulario(self):  
        try:
            if os.path.exists(f'{self.nombre}_vocabulario.json'):  # verifico si el archivo del usuario existe
                with open(f'{self.nombre}_vocabulario.json', 'r') as fichero_personal_usuario:  # abro el archivo en modo lectura
                    carga_datos = json.load(fichero_personal_usuario)  # cargo los datos del archivo json
                    self.vocabulario = [Palabra(**palabra) for palabra in carga_datos]  # convierto los datos en objetos Palabra
            else:
                print("Usuario no registrado. Se va a crear un nuevo espacio para su práctica de vocabulario.")  # aviso si no existe el archivo
        except (IOError, json.JSONDecodeError) as e:  # manejo posibles errores de entrada/salida o json malformado
            print(f"Error al cargar el vocabulario: {e}")  # imprimo el error

    def guardar_vocabulario(self):  
        try:
            with open(f'{self.nombre}_vocabulario.json', 'w') as f:  # abro el archivo en modo escritura
                json.dump([vars(palabra) for palabra in self.vocabulario], f, indent=3)  # guardo el vocabulario en formato json
        except IOError as e:  # manejo errores de escritura en el archivo
            print(f"Error al guardar el vocabulario: {e}")  # imprimo el error

    def agregar_palabra(self, palabra):  
        # verifico si la palabra ya existe en el vocabulario
        if any(p.palabra_original.lower() == palabra.palabra_original.lower() for p in self.vocabulario):  # compruebo si la palabra ya está en la lista
            print("La palabra ya existe en su vocabulario.")  # aviso si la palabra ya existe
            return  # salgo si la palabra ya está
        else:
            self.vocabulario.append(palabra)  
            self.guardar_vocabulario()  # guardo el vocabulario actualizado

    def listar_vocabulario(self):  
        if not self.vocabulario:  # verifico si el vocabulario está vacío
            print("Todavía no hay palabras en su vocabulario.")  # aviso si no hay palabras
        else:
            for palabra in self.vocabulario:  
                print(palabra.mostrar_datos_palabra())  # muestro los datos de cada palabra

    def borrar_vocabulario(self):  
        self.vocabulario = []  # vacío la lista de vocabulario
        self.guardar_vocabulario()  # guardo el estado vacío en el archivo
        print("Todo el vocabulario ha sido borrado.")  # confirmo que el vocabulario fue borrado

class Vocabulario:
    def __init__(self):  
        self.usuarios = {}  # uso un diccionario para almacenar instancias de Usuario
        self.todas_palabras_usuarios = []  # lista para almacenar todas las palabras de todos los usuarios
        self.palabras_unicas = set()  # set para almacenar palabras únicas
        self.cargar_vocabulario_global()  # cargo el vocabulario global al iniciar
        self.translator = Translator()  # inicializo el traductor

    def cargar_vocabulario_global(self):  
        try:
            if os.path.exists('vocabulario_global.json'):  # verifico si el archivo existe
                with open('vocabulario_global.json', 'r') as f:  # abro el archivo en modo lectura
                    self.todas_palabras_usuarios = json.load(f)  # cargo los datos del archivo json
        except (IOError, json.JSONDecodeError) as e:  # manejo posibles errores de entrada/salida o json malformado
            print(f"Error al cargar el vocabulario: {e}")  # imprimo el error

    def guardar_vocabulario_global(self):  
        try:
            with open('vocabulario_global.json', 'w') as f:  # abro el archivo en modo escritura
                json.dump(self.todas_palabras_usuarios, f, indent=3)  # guardo el vocabulario global en formato json
        except IOError as e:  # manejo posibles errores de escritura
            print(f"Error al guardar el vocabulario global: {e}")  # imprimo el error

    def agregar_usuario(self, usuario):  
        self.usuarios[usuario.nombre] = usuario  # almaceno al usuario en el diccionario usando su nombre como clave

    def agregar_palabra(self, palabra_agregar, traduccion, categoria, usuario):  
        info_palabra = (palabra_agregar.lower(), traduccion, categoria)  # creo una tupla con la información de la palabra

        # verifico si la palabra ya está en el vocabulario del usuario
        if any(p.palabra_original.lower() == palabra_agregar.lower() for p in usuario.vocabulario):  # compruebo si la palabra ya existe
            print("La palabra ya existe en el vocabulario del usuario. Introduzca una nueva.")  # aviso si la palabra ya está
            return  # salgo si la palabra ya está en el vocabulario del usuario

        palabra_nueva = Palabra(palabra_agregar, traduccion, categoria)  # creo una nueva instancia de Palabra
        usuario.agregar_palabra(palabra_nueva)  # intento agregar la palabra al vocabulario del usuario

        if info_palabra not in self.palabras_unicas:  # si la palabra es única, la agrego al vocabulario global
            self.todas_palabras_usuarios.append({  # añado la palabra al listado global
                'palabra_original': palabra_agregar,
                'traduccion': traduccion,
                'categoria': categoria
            })  # agrego la información de la palabra al vocabulario global
            self.palabras_unicas.add(info_palabra)  # agrego la palabra al set de palabras únicas
            self.guardar_vocabulario_global()  # guardo el vocabulario global actualizado

        print("Palabra agregada con éxito.")  # confirmo que la palabra ha sido agregada

    def traducir_palabra(self, palabra): 
        try:
            traduccion = self.translator.translate(palabra, src='es', dest='en')  # uso el traductor para traducir la palabra
            return traduccion.text  # devuelvo la traducción
        except Exception as e:  # manejo posibles errores en la traducción
            print(f"Error al traducir la palabra: {e}")  # imprimo el error
            return None  # devuelvo None si ocurre un error

    def practicar_vocabulario(self, usuario): 
        if usuario.vocabulario:  # verifico si el usuario tiene palabras en su vocabulario
            palabra_random = random.choice(usuario.vocabulario)  # elijo una palabra aleatoria del vocabulario del usuario
            respuesta = input(f"¿Cuál es la traducción de '{palabra_random.palabra_original}'? ")  # pido al usuario que traduzca la palabra
            if respuesta.lower() == palabra_random.traduccion.lower():  # verifico si la respuesta es correcta
                print("¡CORRECTO!")  # confirmo la respuesta correcta
                palabra_random.marcar_como_aprendida()  # marco la palabra como aprendida
                usuario.guardar_vocabulario()  # guardo el vocabulario actualizado
            else:
                print(f"Incorrecto. La respuesta correcta es '{palabra_random.traduccion}'.")  # indico la respuesta correcta si se equivoca
        else:
            print("No hay palabras en el vocabulario para practicar.")  # aviso si el vocabulario está vacío

    def listar_vocabularios_todos(self):  
        if not self.todas_palabras_usuarios:  # si no hay palabras globales
            print("Todavía no hay ninguna palabra almacenada.")  # aviso si no hay palabras
            return  # salgo de la función
        
        for info in self.todas_palabras_usuarios:  # recorro todas las palabras globales
            print(f"{info['palabra_original']} - {info['traduccion']} (Categoría: {info['categoria']})")  # muestro los datos de la palabra

    def listar_vocabulario_por_categoria(self):  
        if not self.todas_palabras_usuarios:  # si no hay palabras en el vocabulario global
            print("No hay palabras almacenadas.")  # aviso si no hay palabras
            return

        vocabulario_por_categoria = defaultdict(list)  # uso defaultdict para agrupar palabras por categoría
        for palabra in self.todas_palabras_usuarios:  # recorro las palabras del vocabulario global
            vocabulario_por_categoria[palabra['categoria']].append(palabra)  # agrupo las palabras por su categoría

        for categoria in sorted(vocabulario_por_categoria.keys()):  # ordeno y muestro las categorías
            print(f"Categoría: {categoria}")  # muestro la categoría
            for palabra in sorted(vocabulario_por_categoria[categoria], key=lambda x: x['palabra_original']):  # ordeno las palabras por su nombre
                print(f"  {palabra['palabra_original']} - {palabra['traduccion']}")  # muestro la palabra y su traducción

    def copiar_vocabulario_global_a_usuario(self, usuario):  
        for info in self.todas_palabras_usuarios:  # recorro las palabras globales
            palabra_nueva = Palabra(info['palabra_original'], info['traduccion'], info['categoria'])  # creo una nueva instancia de Palabra
            if not any(p.palabra_original.lower() == palabra_nueva.palabra_original.lower() for p in usuario.vocabulario):  # verifico si la palabra ya está en el vocabulario del usuario
                usuario.agregar_palabra(palabra_nueva)  # agrego la palabra al vocabulario del usuario
                print(f"Palabra '{palabra_nueva.palabra_original}' copiada al vocabulario de {usuario.nombre}.")  # confirmo la copia de la palabra

def main():  # función principal
    vocabulario = Vocabulario()  # creo una instancia de Vocabulario

    while True:  # bucle principal del programa
        nombre_usuario = input("Ingrese su nombre de usuario (o 'salir' para terminar): ")  # pido al usuario su nombre
        if nombre_usuario.lower() == 'salir':  # si el usuario escribe "salir"
            print("¡Hasta luego!")  # me despido
            break  # salgo del bucle

        if nombre_usuario in vocabulario.usuarios:  # si el usuario ya existe
            usuario = vocabulario.usuarios[nombre_usuario]  # uso la instancia existente del usuario
            print(f"Bienvenido de nuevo, {nombre_usuario}!")  # doy la bienvenida al usuario
        else:
            usuario = Usuario(nombre_usuario)  # creo una nueva instancia de Usuario
            vocabulario.agregar_usuario(usuario)  # agrego el nuevo usuario al vocabulario

        while True:  # bucle del menú principal para el usuario
            opcion = input(f"\n---- Menú Principal para {nombre_usuario}. Seleccione una opción: ---- \n 1. Agregar Palabra \n 2. Listar vocabulario de {nombre_usuario} \n 3. Practicar vocabulario de {nombre_usuario} \n 4. Mostrar un listado de todas las palabras del vocabulario (de todos los usuarios) \n 5. Listar vocabulario global por categoría \n 6. Copiar vocabulario global a mi vocabulario \n 7. Borrar todo el vocabulario de {nombre_usuario} \n 8. Traducir palabra \n 9. Cambiar usuario \n 10. Salir \n")   
            
            if opcion not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:  # verifico si la opción ingresada es válida
                print("Opción no válida. Por favor, seleccione una opción del 1 al 10.")  # aviso si la opción es incorrecta
                continue  # vuelvo a pedir una opción

            match opcion:  # uso un bloque match para manejar las opciones
                case "1":  # opción para agregar una palabra
                    palabra = input("Ingrese la palabra en el idioma original: ")  # pido la palabra
                    traduccion = input("Ingrese la traducción: ")  # pido la traducción
                    categoria = input("Ingrese la categoría: ")  # pido la categoría
                    vocabulario.agregar_palabra(palabra, traduccion, categoria, usuario)  # agrego la palabra al vocabulario del usuario

                case "2":  # opción para listar el vocabulario del usuario
                    print(f"Vocabulario de {usuario.nombre}:")  # muestro el nombre del usuario
                    usuario.listar_vocabulario()  # muestro el vocabulario del usuario

                case "3":  # opción para practicar vocabulario
                    vocabulario.practicar_vocabulario(usuario)  # permito al usuario practicar su vocabulario

                case "4":  # opción para listar todas las palabras del vocabulario global
                    print("Listado de todas las palabras almacenadas:")  # muestro un título
                    vocabulario.listar_vocabularios_todos()  # muestro todas las palabras globales

                case "5":  # opción para listar el vocabulario global por categorías
                    vocabulario.listar_vocabulario_por_categoria()  # muestro el vocabulario global agrupado por categoría

                case "6":  # opción para copiar el vocabulario global al del usuario
                    vocabulario.copiar_vocabulario_global_a_usuario(usuario)  # copio palabras globales al vocabulario del usuario

                case "7":  # opción para borrar el vocabulario del usuario
                    confirmacion = input("¿Está seguro de que quiere borrar todo su vocabulario? (sí/no): ").lower()  # confirmo la acción
                    if confirmacion == "sí":  # si confirma
                        usuario.borrar_vocabulario()  # borro el vocabulario del usuario

                case "8":  # opción para traducir una palabra
                    palabra_a_traducir = input("Ingrese la palabra que desea traducir: ")  # pido la palabra a traducir
                    traduccion = vocabulario.traducir_palabra(palabra_a_traducir)  # llamo al método de traducción
                    if traduccion:  # si la traducción fue exitosa
                        print(f"Traducción: {palabra_a_traducir} -> {traduccion}")  # muestro la traducción

                case "9":  # opción para cambiar de usuario
                    break  # salgo al menú principal para cambiar de usuario

                case "10":  # opción para salir del programa
                    print("¡Adiós!")  # me despido
                    return  # termino el programa
                

main()  # ejecuto la función principal