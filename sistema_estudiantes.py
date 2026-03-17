
"""
Sistema de Gestión Básica de Estudiantes
Autor: Carlos Moran
Fecha: 16 de marzo de 2026
"""

# CLASE ESTUDIANTE
class Estudiante:       
    def __init__(self, nombre, edad, nota1, nota2, nota3):
        self.nombre = nombre
        self.edad = edad
        self.nota1 = nota1
        self.nota2 = nota2
        self.nota3 = nota3
        self.promedio = self.calcular_promedio()
        self.estado = self.evaluar_estado()
    
    def calcular_promedio(self):
        promedio = (self.nota1 + self.nota2 + self.nota3) / 3
        return round(promedio, 2)
    
    def evaluar_estado(self):
        if self.promedio >= 4.0:
            return "Aprobado"
        elif self.promedio >= 3.0:
            return "En recuperación"
        else:
            return "Reprobado"
    
    def obtener_informacion(self):
        return {
            'nombre': self.nombre,
            'edad': self.edad,
            'nota1': self.nota1,
            'nota2': self.nota2,
            'nota3': self.nota3,
            'promedio': self.promedio,
            'estado': self.estado
        }
    
    def mostrar_informacion(self):
        print("\n" + "✅ ESTUDIANTE REGISTRADO EXITOSAMENTE")
        print("-" * 40)
        print(f"Nombre: {self.nombre}")
        print(f"Edad: {self.edad} años")
        print(f"Nota 1: {self.nota1}")
        print(f"Nota 2: {self.nota2}")
        print(f"Nota 3: {self.nota3}")
        print(f"Promedio del estudiante: {self.promedio:.2f}")
        print(f"Estado académico: {self.estado}")
    
    def __str__(self):        
        return f"{self.nombre}: {self.promedio:.2f} - {self.estado}"
    
    def __repr__(self):       
        return f"Estudiante('{self.nombre}', {self.edad}, {self.nota1}, {self.nota2}, {self.nota3})"


# VARIABLES GLOBALES
estudiantes_registrados = []

# REGISTRAR ESTUDIANTE
def registrar_estudiante():    
    print("\n" + "="*50)
    print("         REGISTRO DE NUEVO ESTUDIANTE")
    print("="*50)
    
    # Validar nombre
    while True:
        nombre = input("\nIngrese el nombre del estudiante: ").strip()
        if nombre == "":
            print("Por favor, ingrese un nombre válido.")
            continue
        if nombre.isdigit():
            print("Por favor, ingrese un nombre válido.")
            continue
        break
    
    # Validar edad
    while True:
        try:
            edad_input = input("Ingrese la edad: ").strip()
            edad = int(edad_input)
            if edad <= 0:
                print("Por favor, ingrese una edad válida.")
                continue     
            break
        except ValueError:
            print("Por favor, ingrese solo números.")
    
    # Validar las tres notas
    notas = []
    for i in range(1, 4):
        while True:
            try:
                nota_input = input(f"Ingrese nota {i}: ").strip()
                nota = float(nota_input)
                if nota < 0 or nota > 5:
                    print("Por favor, ingrese una nota entre 0 y 5.")
                    continue
                notas.append(nota)
                break
            except ValueError:
                print("Puede usar decimales (ejemplo: 4.5).")
    
    # Crear objeto estudiante y agregarlo a la lista
    estudiante = Estudiante(nombre, edad, notas[0], notas[1], notas[2])
    estudiante.mostrar_informacion()
    estudiantes_registrados.append(estudiante)
    
    return estudiante


# MOSTRAR MENÚ
def mostrar_menu():
    print("\n" + "="*50)
    print("        SISTEMA DE GESTIÓN DE ESTUDIANTES")
    print("="*50)
    print("1. Registrar estudiante")
    print("2. Mostrar todos los estudiantes.")
    print("3. Salir")
    print("-" * 50)


# VER ESTUDIANTES REGISTRADOS
def mostrar_estudiantes_registrados():
    print("\n" + "="*50)
    print("        ESTUDIANTES REGISTRADOS")
    print("="*50)
    
    if len(estudiantes_registrados) == 0:
        print("\n No hay estudiantes registrados.")
        print("Primero debe registrar estudiantes para poder verlos.")
        print("\nVuelva al menú principal y seleccione la opción 1.")
    else:
        print(f"\nTotal de estudiantes: {len(estudiantes_registrados)}")
        print("\nLISTADO DE ESTUDIANTES:")
        print("-" * 50)
        
        for i, estudiante in enumerate(estudiantes_registrados, 1):
            print(f"{i}. {estudiante.nombre}")
            print(f"   Edad: {estudiante.edad} años")
            print(f"   Promedio: {estudiante.promedio:.2f}")
            print(f"   Estado: {estudiante.estado}")
            print("-" * 30)
    
    print("\n0. Regresar al menú principal")
    print("-" * 50)
    
    while True:
        opcion = input("Seleccione una opción (0): ").strip()
        if opcion == "0":
            break
        else:
            print("Opción inválida. Presione 0 para regresar.")



# MOSTRAR RESUMEN FINAL
def mostrar_resumen_final():
    print("\n" + "="*50)
    print("           RESUMEN FINAL")
    print("="*50)
    
    total_estudiantes = len(estudiantes_registrados)
    print(f"Total de estudiantes registrados: {total_estudiantes}")
    
    if total_estudiantes > 0:
        suma_promedios = sum(estudiante.promedio for estudiante in estudiantes_registrados)
        promedio_general = suma_promedios / total_estudiantes
        print(f"Promedio general del grupo: {promedio_general:.2f}")
        
        aprobados = sum(1 for e in estudiantes_registrados if e.estado == "Aprobado")
        en_recuperacion = sum(1 for e in estudiantes_registrados if e.estado == "En recuperación")
        reprobados = sum(1 for e in estudiantes_registrados if e.estado == "Reprobado")
        
        print(f"\nESTADÍSTICAS ACADÉMICAS:")
        print("-" * 50)
        print(f"Aprobados: {aprobados} ({aprobados/total_estudiantes*100:.1f}%)")
        print(f"En recuperación: {en_recuperacion} ({en_recuperacion/total_estudiantes*100:.1f}%)")
        print(f"Reprobados: {reprobados} ({reprobados/total_estudiantes*100:.1f}%)")
        
        print("\nDETALLE POR ESTUDIANTE:")
        print("-" * 50)
        for i, estudiante in enumerate(estudiantes_registrados, 1):
            print(f"{i}. {estudiante}")
            
    else:
        print("No se registraron estudiantes en esta sesión.")
    
    print("="*50)
    print("¡Gracias por usar el Sistema de Estudiantes!")
    print("="*50)
# FUNCIÓN PRINCIPAL
def main():
    print("¡Bienvenido al Sistema de Gestión de Estudiantes!")
    
    while True:
        mostrar_menu()
        
        try:
            opcion = input("Seleccione una opción (1-3): ").strip()
            
            if opcion == "1":
                registrar_estudiante()
                input("\nPresione ENTER para continuar...")
                
            elif opcion == "2":
                mostrar_estudiantes_registrados()
                input("\nPresione ENTER para continuar...")
            elif opcion == "3":
                print("\nSaliendo del sistema...")
                if len(estudiantes_registrados) > 0:
                    mostrar_resumen_final()
                else:
                    print("\n¡Gracias por usar el Sistema de Estudiantes!")
                break
                
            else:
                print("Opción inválida. Por favor, seleccione 1, 2 o 3.")
                input("Presione ENTER para continuar...")
                
        except KeyboardInterrupt:
            print("\n\nPrograma interrumpido por el usuario.")
            if len(estudiantes_registrados) > 0:
                mostrar_resumen_final()
            break
        except Exception as e:
            print(f"Error inesperado: {e}")
            input("Presione ENTER para continuar...")


if __name__ == "__main__":
    main()