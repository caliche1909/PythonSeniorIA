from abc import ABC, abstractmethod


# =============================================================
# CLASE ABSTRACTA: Persona
# Concepto POO: Abstracción + Herencia
# =============================================================

class Persona(ABC):
    def __init__(self, nombre, documento):
        self.nombre = nombre
        self.documento = documento

    @abstractmethod
    def mostrar_rol(self):
        pass


# =============================================================
# HERENCIA: Veterinario, Recepcionista, Cliente
# Concepto POO: Herencia + Polimorfismo (mostrar_rol distinto)
# =============================================================
class Veterinario(Persona):
    def __init__(self, nombre, documento, especialidad):
        super().__init__(nombre, documento)
        self.especialidad = especialidad

    def mostrar_rol(self):
        print(f"[Veterinario] {self.nombre} | Documento: {self.documento} | Especialidad: {self.especialidad}")

    def atender_mascota(self, mascota):
        print(f"El Dr. {self.nombre} está atendiendo a {mascota.nombre} ({mascota.especie})")


class Recepcionista(Persona):
    def __init__(self, nombre, documento):
        super().__init__(nombre, documento)

    def mostrar_rol(self):
        print(f"[Recepcionista] {self.nombre} | Documento: {self.documento}")

    def registrar_cliente(self, cliente):
        print(f"Recepcionista {self.nombre} registró al cliente: {cliente.nombre}")


class Cliente(Persona):
    def __init__(self, nombre, documento, telefono):
        super().__init__(nombre, documento)
        self.telefono = telefono
        self.mascotas = []   # Agregación: las mascotas existen independientemente

    def mostrar_rol(self):
        print(f"[Cliente] {self.nombre} | Documento: {self.documento} | Tel: {self.telefono}")

    def agregar_mascota(self, mascota):
        self.mascotas.append(mascota)
        print(f"Mascota '{mascota.nombre}' agregada al cliente {self.nombre}")

    def mostrar_mascotas(self):
        print(f"\nMascotas de {self.nombre}:")
        if not self.mascotas:
            print("  (sin mascotas registradas)")
        for m in self.mascotas:
            m.mostrar_info()


# =============================================================
# CLASE: Mascota
# Concepto POO: Agregación con Cliente
# =============================================================
class Mascota:
    def __init__(self, nombre, especie, edad, peso):
        self.nombre = nombre
        self.especie = especie
        self.edad = edad
        self.peso = peso

    def mostrar_info(self):
        print(f"  - {self.nombre} | Especie: {self.especie} | Edad: {self.edad} años | Peso: {self.peso} kg")


# =============================================================
# CLASE: Tratamiento
# Concepto POO: Composición con Consulta (nace dentro de Consulta)
# =============================================================
class Tratamiento:
    def __init__(self, nombre, costo, duracion_dias):
        self.nombre = nombre
        self.costo = costo
        self.duracion_dias = duracion_dias

    def mostrar_tratamiento(self):
        print(f"    Tratamiento: {self.nombre} | Costo: ${self.costo:,.0f} | Duración: {self.duracion_dias} días")


# =============================================================
# CLASE: Consulta
# Concepto POO:
#   - Asociación con Veterinario y Mascota
#   - Composición con Tratamiento
# =============================================================
class Consulta:
    def __init__(self, mascota, veterinario, motivo):
        self.mascota = mascota
        self.veterinario = veterinario
        self.motivo = motivo
        self.diagnostico = ""
        self.tratamientos = []   # Composición: los tratamientos nacen dentro de la consulta

    def crear_tratamiento(self, nombre, costo, duracion_dias):
        tratamiento = Tratamiento(nombre, costo, duracion_dias)
        self.tratamientos.append(tratamiento)
        print(f"  Tratamiento '{nombre}' creado en la consulta")
        return tratamiento

    def mostrar_resumen(self):
        print(f"\n{'='*50}")
        print(f"  RESUMEN DE CONSULTA")
        print(f"{'='*50}")
        print(f"  Mascota   : {self.mascota.nombre} ({self.mascota.especie})")
        print(f"  Veterinario: Dr. {self.veterinario.nombre}")
        print(f"  Motivo    : {self.motivo}")
        print(f"  Diagnóstico: {self.diagnostico if self.diagnostico else 'Sin diagnóstico'}")
        print(f"  Tratamientos:")
        for t in self.tratamientos:
            t.mostrar_tratamiento()
        print(f"  Costo total: ${self.calcular_costo_consulta():,.0f}")
        print(f"{'='*50}")

    def calcular_costo_consulta(self):
        return sum(t.costo for t in self.tratamientos)


# =============================================================
# CLASE ABSTRACTA: MetodoPago
# Concepto POO: Abstracción + Polimorfismo
# =============================================================
class MetodoPago(ABC):
    @abstractmethod
    def procesar_pago(self, monto):
        pass


class PagoEfectivo(MetodoPago):
    def __init__(self, monto_recibido):
        self.monto_recibido = monto_recibido

    def procesar_pago(self, monto):
        cambio = self.monto_recibido - monto
        print(f"  [Pago en Efectivo] Monto recibido: ${self.monto_recibido:,.0f} | "
              f"Total: ${monto:,.0f} | Cambio: ${cambio:,.0f}")


class PagoTarjeta(MetodoPago):
    def __init__(self, numero_tarjeta):
        self.numero_tarjeta = numero_tarjeta

    def procesar_pago(self, monto):
        print(f"  [Pago con Tarjeta] Tarjeta: **** **** **** {self.numero_tarjeta[-4:]} | "
              f"Cobrado: ${monto:,.0f}")


class PagoTransferencia(MetodoPago):
    def __init__(self, numero_cuenta):
        self.numero_cuenta = numero_cuenta

    def procesar_pago(self, monto):
        print(f"  [Pago por Transferencia] Cuenta destino: {self.numero_cuenta} | "
              f"Valor transferido: ${monto:,.0f}")


# =============================================================
# CLASE: Factura
# Concepto POO: Polimorfismo (acepta cualquier MetodoPago)
# =============================================================
class Factura:
    IMPUESTO = 0.19   # 19% IVA

    def __init__(self, consulta):
        self.consulta = consulta
        self.subtotal = 0.0
        self.impuesto = 0.0
        self.total = 0.0

    def calcular_total(self):
        self.subtotal = self.consulta.calcular_costo_consulta()
        self.impuesto = self.subtotal * self.IMPUESTO
        self.total = self.subtotal + self.impuesto
        print(f"\n  Subtotal : ${self.subtotal:,.0f}")
        print(f"  IVA (19%): ${self.impuesto:,.0f}")
        print(f"  TOTAL    : ${self.total:,.0f}")
        return self.total

    def pagar(self, metodo_pago):
        if self.total == 0:
            self.calcular_total()
        print(f"\n  Procesando pago...")
        metodo_pago.procesar_pago(self.total)   # Polimorfismo: no importa qué método sea
        print(f"  ✔ Pago realizado exitosamente")


# =============================================================
# SISTEMA DE MENÚ INTERACTIVO
# =============================================================
class SistemaVeterinaria:
    def __init__(self):
        self.clientes = []
        self.veterinarios = []
        self.mascotas = []       # todas las mascotas del sistema
        self.consultas = []
        self.facturas = []

    # ---- helpers ----
    def _separador(self):
        print("\n" + "=" * 55)

    def _pausar(self):
        input("\n  Presiona Enter para continuar...")

    def _seleccionar(self, lista, etiqueta):
        """Muestra una lista numerada y retorna el elemento elegido."""
        if not lista:
            print(f"\n  ⚠  No hay {etiqueta} registrados.")
            return None
        print(f"\n  Selecciona {etiqueta}:")
        for i, item in enumerate(lista):
            print(f"  {i + 1}. {item.nombre}")
        while True:
            try:
                idx = int(input("  Opción: ")) - 1
                if 0 <= idx < len(lista):
                    return lista[idx]
                print("  Opción inválida, intenta de nuevo.")
            except ValueError:
                print("  Ingresa un número válido.")

    # ---- opciones del menú ----
    def agregar_cliente(self):
        self._separador()
        print("  AGREGAR CLIENTE")
        self._separador()
        nombre = input("  Nombre completo : ")
        documento = input("  Documento       : ")
        telefono = input("  Teléfono        : ")
        cliente = Cliente(nombre, documento, telefono)
        self.clientes.append(cliente)
        print(f"\n  ✔ Cliente '{nombre}' registrado exitosamente.")
        self._pausar()

    def agregar_veterinario(self):
        self._separador()
        print("  AGREGAR VETERINARIO")
        self._separador()
        nombre = input("  Nombre completo : ")
        documento = input("  Documento       : ")
        especialidad = input("  Especialidad    : ")
        vet = Veterinario(nombre, documento, especialidad)
        self.veterinarios.append(vet)
        print(f"\n  ✔ Veterinario 'Dr. {nombre}' registrado exitosamente.")
        self._pausar()

    def registrar_mascota(self):
        self._separador()
        print("  REGISTRAR MASCOTA")
        self._separador()
        cliente = self._seleccionar(self.clientes, "un cliente")
        if not cliente:
            self._pausar()
            return
        nombre = input("  Nombre de la mascota : ")
        especie = input("  Especie (Perro/Gato/etc.) : ")
        try:
            edad = int(input("  Edad (años) : "))
            peso = float(input("  Peso (kg)   : "))
        except ValueError:
            print("  ⚠  Edad o peso inválido.")
            self._pausar()
            return
        mascota = Mascota(nombre, especie, edad, peso)
        cliente.agregar_mascota(mascota)
        self.mascotas.append(mascota)
        print(f"\n  ✔ Mascota '{nombre}' registrada y asignada a {cliente.nombre}.")
        self._pausar()

    def crear_consulta(self):
        self._separador()
        print("  CREAR CONSULTA")
        self._separador()
        if not self.mascotas:
            print("\n  ⚠  No hay mascotas registradas. Registra una mascota primero.")
            self._pausar()
            return
        if not self.veterinarios:
            print("\n  ⚠  No hay veterinarios registrados.")
            self._pausar()
            return
        mascota = self._seleccionar(self.mascotas, "una mascota")
        if not mascota:
            self._pausar()
            return
        veterinario = self._seleccionar(self.veterinarios, "un veterinario")
        if not veterinario:
            self._pausar()
            return
        motivo = input("  Motivo de la consulta : ")
        diagnostico = input("  Diagnóstico           : ")
        consulta = Consulta(mascota, veterinario, motivo)
        consulta.diagnostico = diagnostico
        veterinario.atender_mascota(mascota)
        self.consultas.append(consulta)
        print(f"\n  ✔ Consulta creada. Consulta N° {len(self.consultas)}")
        self._pausar()

    def agregar_tratamiento(self):
        self._separador()
        print("  AGREGAR TRATAMIENTO A CONSULTA")
        self._separador()
        if not self.consultas:
            print("\n  ⚠  No hay consultas registradas.")
            self._pausar()
            return
        print("\n  Consultas disponibles:")
        for i, c in enumerate(self.consultas):
            print(f"  {i + 1}. Consulta de {c.mascota.nombre} — Dr. {c.veterinario.nombre} — Motivo: {c.motivo}")
        try:
            idx = int(input("  Selecciona consulta: ")) - 1
            if not (0 <= idx < len(self.consultas)):
                print("  Opción inválida.")
                self._pausar()
                return
        except ValueError:
            print("  Ingresa un número válido.")
            self._pausar()
            return
        consulta = self.consultas[idx]
        nombre = input("  Nombre del tratamiento : ")
        try:
            costo = float(input("  Costo ($)              : "))
            duracion = int(input("  Duración (días)        : "))
        except ValueError:
            print("  ⚠  Costo o duración inválidos.")
            self._pausar()
            return
        consulta.crear_tratamiento(nombre, costo, duracion)
        print(f"\n  ✔ Tratamiento '{nombre}' agregado a la consulta.")
        self._pausar()

    def ver_resumen_consulta(self):
        self._separador()
        print("  RESUMEN DE CONSULTA")
        self._separador()
        if not self.consultas:
            print("\n  ⚠  No hay consultas registradas.")
            self._pausar()
            return
        print("\n  Consultas disponibles:")
        for i, c in enumerate(self.consultas):
            print(f"  {i + 1}. {c.mascota.nombre} — Dr. {c.veterinario.nombre}")
        try:
            idx = int(input("  Selecciona consulta: ")) - 1
            if 0 <= idx < len(self.consultas):
                self.consultas[idx].mostrar_resumen()
        except ValueError:
            print("  Número inválido.")
        self._pausar()

    def generar_factura_y_pagar(self):
        self._separador()
        print("  GENERAR FACTURA Y PAGAR")
        self._separador()
        if not self.consultas:
            print("\n  ⚠  No hay consultas registradas.")
            self._pausar()
            return
        print("\n  Consultas disponibles:")
        for i, c in enumerate(self.consultas):
            estado = "✔ Pagada" if any(f.consulta is c for f in self.facturas) else "Pendiente"
            print(f"  {i + 1}. {c.mascota.nombre} — Dr. {c.veterinario.nombre} [{estado}]")
        try:
            idx = int(input("  Selecciona consulta: ")) - 1
            if not (0 <= idx < len(self.consultas)):
                print("  Opción inválida.")
                self._pausar()
                return
        except ValueError:
            print("  Número inválido.")
            self._pausar()
            return
        consulta = self.consultas[idx]
        if not consulta.tratamientos:
            print("\n  ⚠  La consulta no tiene tratamientos. Agrega al menos uno.")
            self._pausar()
            return
        factura = Factura(consulta)
        print("\n  --- Detalle de factura ---")
        factura.calcular_total()
        print("\n  Método de pago:")
        print("  1. Efectivo")
        print("  2. Tarjeta")
        print("  3. Transferencia")
        opcion = input("  Elige método: ").strip()
        if opcion == "1":
            try:
                recibido = float(input("  Monto recibido ($): "))
            except ValueError:
                print("  Monto inválido.")
                self._pausar()
                return
            metodo = PagoEfectivo(recibido)
        elif opcion == "2":
            numero = input("  Número de tarjeta: ")
            metodo = PagoTarjeta(numero)
        elif opcion == "3":
            cuenta = input("  Número de cuenta: ")
            metodo = PagoTransferencia(cuenta)
        else:
            print("  Opción inválida.")
            self._pausar()
            return
        factura.pagar(metodo)
        self.facturas.append(factura)
        self._pausar()

    def ver_clientes(self):
        self._separador()
        print("  CLIENTES REGISTRADOS")
        self._separador()
        if not self.clientes:
            print("\n  (Ningún cliente registrado)")
        for i, c in enumerate(self.clientes):
            print(f"\n  {i + 1}.", end=" ")
            c.mostrar_rol()
            c.mostrar_mascotas()
        self._pausar()

    def ver_veterinarios(self):
        self._separador()
        print("  VETERINARIOS REGISTRADOS")
        self._separador()
        if not self.veterinarios:
            print("\n  (Ningún veterinario registrado)")
        for i, v in enumerate(self.veterinarios):
            print(f"\n  {i + 1}.", end=" ")
            v.mostrar_rol()
        self._pausar()

    def ver_resumen_general(self):
        self._separador()
        print("  RESUMEN GENERAL DEL SISTEMA")
        self._separador()
        total_recaudado = sum(f.total for f in self.facturas)
        print(f"\n  Clientes registrados  : {len(self.clientes)}")
        print(f"  Veterinarios          : {len(self.veterinarios)}")
        print(f"  Mascotas              : {len(self.mascotas)}")
        print(f"  Consultas realizadas  : {len(self.consultas)}")
        print(f"  Facturas generadas    : {len(self.facturas)}")
        print(f"  Total recaudado       : ${total_recaudado:,.0f}")
        self._pausar()

    # ---- menú principal ----
    def mostrar_menu(self):
        print("\n" + "=" * 55)
        print("       BIENVENIDO A MI VETERINARIA 🐾")
        print("=" * 55)
        print("  1.  Agregar cliente")
        print("  2.  Agregar veterinario")
        print("  3.  Registrar mascota (asignar a cliente)")
        print("  4.  Crear consulta (asignar mascota a veterinario)")
        print("  5.  Agregar tratamiento a consulta")
        print("  6.  Ver resumen de consulta")
        print("  7.  Generar factura y pagar")
        print("  8.  Ver clientes y sus mascotas")
        print("  9.  Ver veterinarios")
        print("  10. Ver resumen general")
        print("  0.  Salir")
        print("=" * 55)

    def ejecutar(self):
        opciones = {
            "1": self.agregar_cliente,
            "2": self.agregar_veterinario,
            "3": self.registrar_mascota,
            "4": self.crear_consulta,
            "5": self.agregar_tratamiento,
            "6": self.ver_resumen_consulta,
            "7": self.generar_factura_y_pagar,
            "8": self.ver_clientes,
            "9": self.ver_veterinarios,
            "10": self.ver_resumen_general,
        }
        while True:
            self.mostrar_menu()
            opcion = input("  Selecciona una opción: ").strip()
            if opcion == "0":
                print("\n  ¡Hasta pronto! Gracias por usar el sistema. 🐾\n")
                break
            elif opcion in opciones:
                opciones[opcion]()
            else:
                print("\n  ⚠  Opción no válida. Intenta de nuevo.")


# =============================================================
# PUNTO DE ENTRADA
# =============================================================
if __name__ == "__main__":
    sistema = SistemaVeterinaria()
    sistema.ejecutar()

