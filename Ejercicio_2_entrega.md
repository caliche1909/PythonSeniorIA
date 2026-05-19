Ejercicio grupal: Sistema de gestión de hospital veterinario
Contexto

Una clínica veterinaria quiere desarrollar un sistema orientado a objetos para organizar su funcionamiento diario. El sistema debe permitir gestionar personas, mascotas, consultas, tratamientos, pagos y hospitalizaciones.

Los estudiantes deben analizar el problema, identificar las clases, construir el modelo UML y luego implementar una versión funcional en Python.

Objetivo del ejercicio

Diseñar e implementar un sistema en Python que permita modelar el funcionamiento básico de un hospital veterinario, aplicando correctamente relaciones entre clases y principios de POO.

Lo que debe incluir obligatoriamente
1. Clase abstracta

Debe existir una clase abstracta llamada Persona.

De ella deben heredar otras clases.

Atributos sugeridos:
nombre
documento
Método abstracto obligatorio:
mostrar_rol()


2. Herencia

Desde Persona deben heredar al menos estas clases:

Veterinario
Recepcionista
Cliente

Cada una debe implementar mostrar_rol() de forma diferente.

3. Asociación

Debe existir una relación de asociación entre:

Veterinario y Mascota

porque un veterinario puede atender muchas mascotas y una mascota puede ser atendida por distintos veterinarios en diferentes momentos.

Esa relación puede reflejarse en la clase Consulta, donde se conectan ambas clases.

4. Agregación

Debe existir una relación de agregación entre:

Cliente y Mascota

porque un cliente tiene mascotas, pero la mascota puede seguir existiendo aunque el cliente se elimine del sistema.

El cliente debe tener un atributo como:

mascotas = []

y un método:

agregar_mascota()
5. Composición

Debe existir una relación de composición entre:

Consulta y Tratamiento

porque una consulta crea sus tratamientos como parte de sí misma.

La idea es que el tratamiento nazca dentro de la consulta.

La clase Consulta puede tener:

lista de tratamientos
método crear_tratamiento()
6. Polimorfismo

Debe existir una clase abstracta llamada MetodoPago.

De ella deben heredar:

PagoEfectivo
PagoTarjeta
PagoTransferencia

Cada una debe implementar el método:

procesar_pago(monto)

Luego una clase Factura debe usar cualquier objeto de tipo MetodoPago para cobrar una consulta.

Clases mínimas sugeridas

Los estudiantes deben trabajar, como mínimo, con estas clases:

Persona (abstracta)
Veterinario
Recepcionista
Cliente
Mascota
Consulta
Tratamiento
Factura
MetodoPago (abstracta)
PagoEfectivo
PagoTarjeta
PagoTransferencia
Reglas del sistema
Persona

Clase abstracta.

Atributos:
nombre
documento
Método abstracto:
mostrar_rol()
Veterinario

Hereda de Persona.

Atributos:
especialidad
Métodos:
mostrar_rol()
atender_mascota()
Recepcionista

Hereda de Persona.

Métodos:
mostrar_rol()
registrar_cliente()
Cliente

Hereda de Persona.

Atributos:
telefono
lista de mascotas
Métodos:
mostrar_rol()
agregar_mascota()
mostrar_mascotas()
Mascota
Atributos:
nombre
especie
edad
peso
Métodos:
mostrar_info()
Consulta
Atributos:
mascota
veterinario
motivo
diagnostico
tratamientos
Métodos:
crear_tratamiento()
mostrar_resumen()
calcular_costo_consulta()

Aquí se evidencia:

asociación con Mascota
asociación con Veterinario
composición con Tratamiento
Tratamiento
Atributos:
nombre
costo
duracion_dias
Métodos:
mostrar_tratamiento()
MetodoPago

Clase abstracta.

Método abstracto:
procesar_pago(monto)
PagoEfectivo

Hereda de MetodoPago.

PagoTarjeta

Hereda de MetodoPago.

PagoTransferencia

Hereda de MetodoPago.

Cada una debe implementar procesar_pago() de forma distinta.

Factura
Atributos:
consulta
subtotal
impuesto
total
Métodos:
calcular_total()
pagar(metodo_pago)

Aquí se debe aplicar polimorfismo.