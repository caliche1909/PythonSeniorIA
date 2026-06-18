"""
Gestor de Usuarios
==================

Aplicación de consola que permite administrar usuarios de forma robusta:
aunque el usuario se equivoque o el archivo tenga problemas, el programa
nunca se rompe; siempre muestra un mensaje amigable.

Funcionalidad:
  - Registrar usuarios (validando la información).
  - Listar usuarios (informando las líneas mal formadas, sin detenerse).
  - Buscar usuarios por nombre.
  - Evitar usuarios duplicados.
  - Validar un archivo al leerlo y mostrar los errores encontrados.
  - Separar los registros buenos y malos en archivos distintos.
  - Registrar la fecha y hora de creación de cada usuario.
  - Extras: contar, eliminar, edad promedio y ordenar usuarios.

Formato de cada línea del archivo principal:
    nombre,edad,fecha_hora

Ejemplo:
    Carlos,25,2026-06-17 18:30:00
"""

import sys
from datetime import datetime

# Aseguramos que la consola pueda mostrar acentos (Windows usa cp1252 por defecto).
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


class Usuario:
    """Representa a un usuario del sistema."""

    def __init__(self, nombre, edad, fecha_hora=None):
        self.nombre = nombre
        self.edad = int(edad)
        # Si no se entrega fecha, se asigna la del momento de creación.
        self.fecha_hora = fecha_hora or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def a_linea(self):
        """Devuelve el usuario en el formato del archivo: nombre,edad,fecha_hora"""
        return f"{self.nombre},{self.edad},{self.fecha_hora}"

    def __str__(self):
        return f"Nombre: {self.nombre}, Edad: {self.edad}, Creado: {self.fecha_hora}"


class GestorUsuarios:
    """Administra el registro, validación y persistencia de usuarios."""

    def __init__(self, archivo="usuarios.txt",
                 archivo_buenos="usuarios_validos.txt",
                 archivo_errores="errores.txt"):
        self.archivo = archivo
        self.archivo_buenos = archivo_buenos
        self.archivo_errores = archivo_errores

    # ------------------------------------------------------------------ #
    # Validación
    # ------------------------------------------------------------------ #
    def validar_datos(self, nombre, edad):
        """
        Valida nombre y edad según el enunciado:
          - El nombre no puede estar vacío.
          - La edad debe ser numérica.
          - La edad no puede ser negativa.
        Devuelve (True, None) si son válidos, o (False, mensaje) si no.
        """
        if nombre is None or nombre.strip() == "":
            return False, "nombre vacío"

        try:
            edad_int = int(edad)
        except (ValueError, TypeError):
            return False, "edad no numérica"

        if edad_int < 0:
            return False, "edad negativa"

        return True, None

    # ------------------------------------------------------------------ #
    # Lectura de usuarios
    # ------------------------------------------------------------------ #
    def _leer_lineas(self):
        """Lee las líneas del archivo principal. Devuelve una lista (vacía si no existe)."""
        try:
            with open(self.archivo, "r", encoding="utf-8") as archivo:
                return archivo.readlines()
        except FileNotFoundError:
            return []

    def cargar_usuarios(self):
        """Devuelve la lista de objetos Usuario válidos del archivo principal."""
        usuarios = []
        for linea in self._leer_lineas():
            linea = linea.strip()
            if not linea:
                continue
            partes = linea.split(",")
            if len(partes) >= 2:
                nombre = partes[0].strip()
                edad = partes[1].strip()
                fecha = partes[2].strip() if len(partes) >= 3 else None
                valido, _ = self.validar_datos(nombre, edad)
                if valido:
                    usuarios.append(Usuario(nombre, edad, fecha))
        return usuarios

    def existe_usuario(self, nombre):
        """Indica si ya existe un usuario con ese nombre (sin distinguir mayúsculas)."""
        nombre = nombre.strip().lower()
        return any(u.nombre.strip().lower() == nombre for u in self.cargar_usuarios())

    # ------------------------------------------------------------------ #
    # Registrar
    # ------------------------------------------------------------------ #
    def registrar_usuario(self):
        """Pide los datos por consola, los valida y guarda el usuario con fecha/hora."""
        try:
            nombre = input("Ingrese el nombre del usuario: ").strip()
            edad = input("Ingrese la edad del usuario: ").strip()

            valido, mensaje = self.validar_datos(nombre, edad)
            if not valido:
                print(f"[!] Dato no válido: {mensaje}.")
                return

            if self.existe_usuario(nombre):
                print(f"[!] El usuario '{nombre}' ya está registrado. No se permiten duplicados.")
                return

            usuario = Usuario(nombre, edad)
            with open(self.archivo, "a", encoding="utf-8") as archivo:
                archivo.write(usuario.a_linea() + "\n")

            print(f"[OK] Usuario registrado exitosamente. ({usuario})")

        except PermissionError:
            print("[ERROR] No se tienen permisos para escribir en el archivo.")
        except Exception as error:
            print(f"[ERROR] Ocurrió un error inesperado: {error}")

    # ------------------------------------------------------------------ #
    # Listar (informando líneas mal formadas sin detenerse)
    # ------------------------------------------------------------------ #
    def mostrar_usuarios(self):
        """Muestra los usuarios válidos y avisa qué líneas del archivo están mal formadas."""
        try:
            lineas = self._leer_lineas()
            if not lineas:
                print("No hay usuarios registrados.")
                return

            validos = []
            errores = []
            for numero, linea in enumerate(lineas, start=1):
                contenido = linea.strip()
                if contenido == "":
                    continue
                partes = contenido.split(",")
                if len(partes) < 2:
                    errores.append((numero, contenido, "faltan campos"))
                    continue
                nombre = partes[0].strip()
                edad = partes[1].strip()
                fecha = partes[2].strip() if len(partes) >= 3 else None
                valido, mensaje = self.validar_datos(nombre, edad)
                if valido:
                    validos.append(Usuario(nombre, edad, fecha))
                else:
                    errores.append((numero, contenido, mensaje))

            if validos:
                print("\n=== Usuarios registrados ===")
                for indice, usuario in enumerate(validos, start=1):
                    print(f"{indice}. {usuario}")
            else:
                print("No hay usuarios válidos para mostrar.")

            if errores:
                print("\n[!] Se encontraron líneas mal formadas (se omitieron):")
                for numero, contenido, motivo in errores:
                    print(f"    Línea {numero}: '{contenido}' ({motivo})")

        except PermissionError:
            print("[ERROR] No se tienen permisos para leer el archivo.")
        except Exception as error:
            print(f"[ERROR] Ocurrió un error inesperado: {error}")

    # ------------------------------------------------------------------ #
    # Buscar
    # ------------------------------------------------------------------ #
    def buscar_usuario(self):
        """Busca usuarios cuyo nombre contenga el texto ingresado."""
        try:
            criterio = input("Ingrese el nombre a buscar: ").strip().lower()
            if criterio == "":
                print("[!] Debe ingresar un texto para buscar.")
                return

            encontrados = [u for u in self.cargar_usuarios()
                           if criterio in u.nombre.lower()]

            if not encontrados:
                print(f"No se encontró ningún usuario que coincida con '{criterio}'.")
                return

            print(f"\n=== Resultados ({len(encontrados)}) ===")
            for usuario in encontrados:
                print(f"  - {usuario}")

        except Exception as error:
            print(f"[ERROR] Ocurrió un error inesperado: {error}")

    # ------------------------------------------------------------------ #
    # Validar un archivo y mostrar errores
    # ------------------------------------------------------------------ #
    def validar_archivo(self, ruta=None):
        """
        Lee un archivo y muestra los errores de cada línea (sin modificar nada).
        Devuelve dos listas: (lineas_buenas, lineas_malas con su motivo).
        """
        if ruta is None:
            ruta = input("Ingrese la ruta del archivo a validar: ").strip()

        buenos = []
        malos = []

        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                lineas = archivo.readlines()
        except FileNotFoundError:
            print(f"[ERROR] No se encontró el archivo '{ruta}'.")
            return buenos, malos
        except PermissionError:
            print(f"[ERROR] No se tienen permisos para leer '{ruta}'.")
            return buenos, malos

        for numero, linea in enumerate(lineas, start=1):
            contenido = linea.strip()
            if contenido == "":
                continue  # Ignoramos líneas en blanco.

            partes = contenido.split(",")
            if len(partes) < 2:
                malos.append((numero, contenido, "faltan campos (se espera 'nombre,edad')"))
                continue

            nombre = partes[0].strip()
            edad = partes[1].strip()

            valido, mensaje = self.validar_datos(nombre, edad)
            if valido:
                buenos.append(contenido)
            else:
                malos.append((numero, contenido, mensaje))

        # Mostrar el reporte de validación.
        print(f"\n=== Reporte de validación de '{ruta}' ===")
        print(f"Líneas válidas:   {len(buenos)}")
        print(f"Líneas con error: {len(malos)}")

        if malos:
            print("\n--- Errores encontrados ---")
            for numero, contenido, motivo in malos:
                print(f"  Línea {numero}: '{contenido}' ({motivo})")
        else:
            print("[OK] El archivo no contiene errores.")

        return buenos, malos

    # ------------------------------------------------------------------ #
    # Separar registros buenos y malos en archivos distintos
    # ------------------------------------------------------------------ #
    def separar_archivo(self, ruta=None):
        """
        Lee un archivo con posibles errores y crea:
          - un archivo con los registros válidos (tal cual venían en la entrada).
          - un archivo con los registros inválidos (incluyendo el motivo).
        """
        if ruta is None:
            ruta = input("Ingrese la ruta del archivo a procesar: ").strip()

        buenos, malos = self.validar_archivo(ruta)

        # Si no se pudo leer la entrada, no generamos archivos vacíos.
        if not buenos and not malos:
            return

        try:
            with open(self.archivo_buenos, "w", encoding="utf-8") as f_buenos:
                for contenido in buenos:
                    # Se conserva el registro tal como venía en el archivo de entrada.
                    f_buenos.write(contenido + "\n")

            with open(self.archivo_errores, "w", encoding="utf-8") as f_malos:
                for _numero, contenido, motivo in malos:
                    f_malos.write(f"{contenido} ({motivo})\n")

            print(f"\n[OK] Proceso terminado.")
            print(f"   Registros válidos guardados en: {self.archivo_buenos} ({len(buenos)})")
            print(f"   Registros con error guardados en: {self.archivo_errores} ({len(malos)})")

        except PermissionError:
            print("[ERROR] No se tienen permisos para escribir los archivos de salida.")
        except Exception as error:
            print(f"[ERROR] Ocurrió un error inesperado: {error}")

    # ------------------------------------------------------------------ #
    # Extras (puntos opcionales)
    # ------------------------------------------------------------------ #
    def contar_usuarios(self):
        """Muestra cuántos usuarios válidos hay registrados."""
        try:
            total = len(self.cargar_usuarios())
            print(f"Hay {total} usuario(s) registrado(s).")
        except Exception as error:
            print(f"[ERROR] Ocurrió un error inesperado: {error}")

    def eliminar_usuario(self):
        """Elimina del archivo el usuario cuyo nombre coincida (sin distinguir mayúsculas)."""
        try:
            objetivo = input("Ingrese el nombre del usuario a eliminar: ").strip().lower()
            if objetivo == "":
                print("[!] Debe ingresar un nombre.")
                return

            usuarios = self.cargar_usuarios()
            quedan = [u for u in usuarios if u.nombre.strip().lower() != objetivo]

            if len(quedan) == len(usuarios):
                print(f"No se encontró el usuario '{objetivo}'.")
                return

            with open(self.archivo, "w", encoding="utf-8") as archivo:
                for usuario in quedan:
                    archivo.write(usuario.a_linea() + "\n")

            eliminados = len(usuarios) - len(quedan)
            print(f"[OK] Se eliminó {eliminados} usuario(s) con el nombre '{objetivo}'.")

        except PermissionError:
            print("[ERROR] No se tienen permisos para escribir en el archivo.")
        except Exception as error:
            print(f"[ERROR] Ocurrió un error inesperado: {error}")

    def edad_promedio(self):
        """Calcula y muestra la edad promedio de los usuarios registrados."""
        try:
            usuarios = self.cargar_usuarios()
            if not usuarios:
                print("No hay usuarios registrados para calcular el promedio.")
                return
            promedio = sum(u.edad for u in usuarios) / len(usuarios)
            print(f"La edad promedio es {promedio:.1f} años ({len(usuarios)} usuarios).")
        except Exception as error:
            print(f"[ERROR] Ocurrió un error inesperado: {error}")

    def ordenar_usuarios(self):
        """Muestra los usuarios ordenados por nombre o por edad."""
        try:
            usuarios = self.cargar_usuarios()
            if not usuarios:
                print("No hay usuarios registrados.")
                return

            criterio = input("Ordenar por (1) nombre o (2) edad: ").strip()
            if criterio == "1":
                usuarios.sort(key=lambda u: u.nombre.lower())
                titulo = "por nombre"
            elif criterio == "2":
                usuarios.sort(key=lambda u: u.edad)
                titulo = "por edad"
            else:
                print("[!] Opción no válida.")
                return

            print(f"\n=== Usuarios ordenados {titulo} ===")
            for indice, usuario in enumerate(usuarios, start=1):
                print(f"{indice}. {usuario}")

        except Exception as error:
            print(f"[ERROR] Ocurrió un error inesperado: {error}")


def menu():
    gestor = GestorUsuarios()
    opcion = ""

    while opcion != "0":
        print("\n ==== GESTOR DE USUARIOS ====")
        print("1. Registrar usuario")
        print("2. Mostrar usuarios")
        print("3. Buscar usuario")
        print("4. Validar un archivo (mostrar errores)")
        print("5. Separar registros buenos y malos en archivos")
        print("6. Contar usuarios")
        print("7. Eliminar usuario")
        print("8. Edad promedio")
        print("9. Ordenar usuarios")
        print("0. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            gestor.registrar_usuario()
        elif opcion == "2":
            gestor.mostrar_usuarios()
        elif opcion == "3":
            gestor.buscar_usuario()
        elif opcion == "4":
            gestor.validar_archivo()
        elif opcion == "5":
            gestor.separar_archivo()
        elif opcion == "6":
            gestor.contar_usuarios()
        elif opcion == "7":
            gestor.eliminar_usuario()
        elif opcion == "8":
            gestor.edad_promedio()
        elif opcion == "9":
            gestor.ordenar_usuarios()
        elif opcion == "0":
            print("Programa finalizado.")
        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    menu()
