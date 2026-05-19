import os
from datetime import datetime


#  DATOS INICIALES — INVENTARIO DE VIDEOJUEGOS
inventario = {
    "VG001": {"nombre": "The Legend of Zelda: Breath of the Wild", "plataforma": "Nintendo Switch", "genero": "Aventura",   "precio": 259900, "stock": 5,  "descuento": 0},
    "VG002": {"nombre": "God of War Ragnarök",                      "plataforma": "PlayStation 5",  "genero": "Acción",     "precio": 299900, "stock": 3,  "descuento": 0},
    "VG003": {"nombre": "Elden Ring",                               "plataforma": "PC",             "genero": "RPG",        "precio": 219900, "stock": 7,  "descuento": 0},
    "VG004": {"nombre": "FIFA 24",                                  "plataforma": "PlayStation 5",  "genero": "Deportes",   "precio": 249900, "stock": 10, "descuento": 0},
    "VG005": {"nombre": "Minecraft",                                "plataforma": "PC",             "genero": "Sandbox",    "precio": 119900, "stock": 15, "descuento": 0},
    "VG006": {"nombre": "Super Mario Odyssey",                      "plataforma": "Nintendo Switch", "genero": "Plataformas","precio": 199900, "stock": 4,  "descuento": 0},
    "VG007": {"nombre": "Cyberpunk 2077",                           "plataforma": "PC",             "genero": "RPG",        "precio": 179900, "stock": 6,  "descuento": 0},
    "VG008": {"nombre": "Halo Infinite",                            "plataforma": "Xbox Series X",  "genero": "Shooter",    "precio": 229900, "stock": 5,  "descuento": 0},
    "VG009": {"nombre": "Spider-Man 2",                             "plataforma": "PlayStation 5",  "genero": "Acción",     "precio": 319900, "stock": 2,  "descuento": 0},
    "VG010": {"nombre": "Forza Horizon 5",                          "plataforma": "Xbox Series X",  "genero": "Carreras",   "precio": 209900, "stock": 8,  "descuento": 0},
    "VG011": {"nombre": "Hogwarts Legacy",                          "plataforma": "PC",             "genero": "RPG",        "precio": 239900, "stock": 6,  "descuento": 0},
    "VG012": {"nombre": "Street Fighter 6",                         "plataforma": "PlayStation 5",  "genero": "Pelea",      "precio": 219900, "stock": 4,  "descuento": 0},
}

historial_ventas = []



#  FUNCIONES LAMBDA
precio_final      = lambda juego: round(juego["precio"] * (1 - juego["descuento"] / 100))
hay_stock         = lambda juego: juego["stock"] > 0
total_ventas_fn   = lambda historial: sum(v["total"] for v in historial)
filtrar_plat      = lambda inv, p: {k: v for k, v in inv.items() if v["plataforma"].lower() == p.lower()}
filtrar_genero    = lambda inv, g: {k: v for k, v in inv.items() if v["genero"].lower() == g.lower()}
buscar_nombre     = lambda inv, q: {k: v for k, v in inv.items() if q.lower() in v["nombre"].lower()}
ordenar_precio    = lambda inv, asc=True: sorted(inv.items(), key=lambda x: x[1]["precio"], reverse=not asc)
generar_codigo    = lambda inv: f"VG{(max(int(k[2:]) for k in inv) + 1):03d}" if inv else "VG001"



#  UTILIDADES DE VISUALIZACIÓN
ANCHO = 62

def limpiar():
    os.system("cls" if os.name == "nt" else "clear")

def linea(char="─", ancho=ANCHO):
    print(char * ancho)

def centrar(texto, ancho=ANCHO):
    print(texto.center(ancho))

def pausar():
    print()
    input("  Presiona Enter para continuar...".ljust(ANCHO))

def precio_fmt(valor):
    return f"${valor:,.0f} COP"

def cabecera(subtitulo=""):
    limpiar()
    linea("═")
    centrar("🎮   G A M E S T O R E   P R O   🎮")
    centrar("Sistema de Gestión de Tienda de Videojuegos")
    linea("═")
    if subtitulo:
        print(f"  ▶  {subtitulo}")
        linea()

def mostrar_juego_card(codigo, juego, numero=None):
    pf    = precio_final(juego)
    desc  = f"  🏷  -{juego['descuento']}% DESC" if juego["descuento"] > 0 else ""
    stock = f"📦 Stock: {juego['stock']}" if juego["stock"] > 0 else "⚠  AGOTADO"
    num   = f"[{numero}] " if numero is not None else "    "
    print(f"  {num}{codigo}  │  {juego['nombre'][:38]}")
    print(f"         🖥  {juego['plataforma']:<22} 🎯 {juego['genero']}")
    print(f"         💰 {precio_fmt(pf)}{desc:<20} {stock}")
    linea("·")

def mostrar_inventario_tabla(inv):
    if not inv:
        print("\n  ⚠  No hay videojuegos para mostrar.\n")
        return
    print(f"\n  {'CÓD':<7} {'NOMBRE':<38} {'PLAT':<17} {'PRECIO':>12} {'STK':>5}")
    linea()
    for cod, j in inv.items():
        pf   = precio_final(j)
        nom  = j["nombre"][:37]
        plat = j["plataforma"][:16]
        desc = f"*" if j["descuento"] > 0 else ""
        print(f"  {cod:<7} {nom:<38} {plat:<17} {precio_fmt(pf):>12} {j['stock']:>4}{desc}")
    linea()
    print(f"  * = tiene descuento activo    Total productos: {len(inv)}")




#  1. AGREGAR VIDEOJUEGO
def agregar_videojuego():
    cabecera("AGREGAR VIDEOJUEGO AL INVENTARIO")

    print("  ¿Cómo deseas agregar el videojuego?")
    print()
    print("  [1] Ingresar código manualmente")
    print("  [2] Generar código automático")
    print("  [0] Cancelar")
    linea()
    opc = input("  Opción: ").strip()

    if opc == "0":
        return
    elif opc == "1":
        codigo = input("\n  Código (ej. VG015): ").strip().upper()
        if not codigo:
            print("\n  ⚠  Código inválido.")
            pausar(); return
        if codigo in inventario:
            print(f"\n  ⚠  El código {codigo} ya existe.")
            pausar(); return
    elif opc == "2":
        codigo = generar_codigo(inventario)
        print(f"\n  ✔  Código asignado automáticamente: {codigo}")
    else:
        print("\n  ⚠  Opción inválida.")
        pausar(); return

    print()
    nombre     = input("  Nombre del videojuego : ").strip()
    plataforma = input("  Plataforma            : ").strip()
    genero     = input("  Género                : ").strip()

    try:
        precio = int(input("  Precio (COP, sin puntos): ").strip())
        stock  = int(input("  Stock inicial         : ").strip())
    except ValueError:
        print("\n  ⚠  Precio o stock inválido.")
        pausar(); return

    if not nombre or precio <= 0 or stock < 0:
        print("\n  ⚠  Datos incompletos o inválidos.")
        pausar(); return

    inventario[codigo] = {
        "nombre":     nombre,
        "plataforma": plataforma,
        "genero":     genero,
        "precio":     precio,
        "stock":      stock,
        "descuento":  0,
    }

    print(f"\n  ✅  '{nombre}' agregado con código {codigo}.")
    pausar()



#  2. VENDER VIDEOJUEGO
def vender_videojuego():
    cabecera("VENDER VIDEOJUEGO")

    disponibles = {k: v for k, v in inventario.items() if hay_stock(v)}
    if not disponibles:
        print("\n  ⚠  No hay videojuegos en stock disponibles.\n")
        pausar(); return

    print("  ¿Cómo deseas buscar el videojuego a vender?")
    print()
    print("  [1] Por código")
    print("  [2] Por nombre")
    print("  [3] Ver listado completo")
    print("  [0] Cancelar")
    linea()
    opc = input("  Opción: ").strip()

    codigo = None

    if opc == "0":
        return
    elif opc == "1":
        codigo = input("\n  Ingresa el código: ").strip().upper()
        if codigo not in inventario:
            print(f"\n  ⚠  Código '{codigo}' no encontrado.")
            pausar(); return
    elif opc == "2":
        query = input("\n  Ingresa el nombre (o parte de él): ").strip()
        resultado = buscar_nombre(disponibles, query)
        if not resultado:
            print("\n  ⚠  No se encontraron resultados.")
            pausar(); return
        lista = list(resultado.items())
        print()
        for i, (cod, j) in enumerate(lista, 1):
            mostrar_juego_card(cod, j, numero=i)
        try:
            sel = int(input("  Selecciona el número del juego: ").strip())
            if sel < 1 or sel > len(lista):
                raise ValueError
            codigo = lista[sel - 1][0]
        except ValueError:
            print("\n  ⚠  Selección inválida.")
            pausar(); return
    elif opc == "3":
        lista = list(disponibles.items())
        print()
        for i, (cod, j) in enumerate(lista, 1):
            mostrar_juego_card(cod, j, numero=i)
        try:
            sel = int(input("  Selecciona el número del juego: ").strip())
            if sel < 1 or sel > len(lista):
                raise ValueError
            codigo = lista[sel - 1][0]
        except ValueError:
            print("\n  ⚠  Selección inválida.")
            pausar(); return
    else:
        print("\n  ⚠  Opción inválida.")
        pausar(); return

    juego = inventario[codigo]

    if not hay_stock(juego):
        print(f"\n  ⚠  '{juego['nombre']}' está agotado.")
        pausar(); return

    print()
    linea()
    mostrar_juego_card(codigo, juego)
    try:
        cantidad = int(input("  ¿Cuántas unidades deseas vender? ").strip())
    except ValueError:
        print("\n  ⚠  Cantidad inválida.")
        pausar(); return

    if cantidad <= 0:
        print("\n  ⚠  La cantidad debe ser mayor a 0.")
        pausar(); return
    if cantidad > juego["stock"]:
        print(f"\n  ⚠  Solo hay {juego['stock']} unidad(es) disponibles.")
        pausar(); return

    pf    = precio_final(juego)
    total = pf * cantidad

    print()
    linea("─")
    print(f"  Juego    : {juego['nombre']}")
    print(f"  Cantidad : {cantidad}")
    print(f"  P/unidad : {precio_fmt(pf)}")
    print(f"  TOTAL    : {precio_fmt(total)}")
    linea("─")
    confirmar = input("  ¿Confirmar venta? (s/n): ").strip().lower()

    if confirmar != "s":
        print("\n  ❌  Venta cancelada.")
        pausar(); return

    juego["stock"] -= cantidad
    historial_ventas.append({
        "fecha":    datetime.now().strftime("%d/%m/%Y %H:%M"),
        "codigo":   codigo,
        "nombre":   juego["nombre"],
        "cantidad": cantidad,
        "precio":   pf,
        "total":    total,
    })

    print(f"\n  ✅  Venta registrada. Stock restante: {juego['stock']}")
    if juego["stock"] == 0:
        print("  ⚠  ¡El juego quedó agotado!")
    pausar()




#  3. VER INVENTARIO
def ver_inventario():
    cabecera("INVENTARIO COMPLETO")

    print("  Ordenar / Filtrar por:")
    print()
    print("  [1] Ver todo")
    print("  [2] Filtrar por plataforma")
    print("  [3] Filtrar por género")
    print("  [4] Ordenar por precio (menor a mayor)")
    print("  [5] Ordenar por precio (mayor a menor)")
    print("  [6] Solo con stock disponible")
    print("  [7] Solo agotados")
    print("  [0] Volver")
    linea()
    opc = input("  Opción: ").strip()

    if opc == "0":
        return
    elif opc == "1":
        mostrar_inventario_tabla(inventario)
    elif opc == "2":
        plataformas = list(set(v["plataforma"] for v in inventario.values()))
        print("\n  Plataformas disponibles:")
        for i, p in enumerate(plataformas, 1):
            print(f"    [{i}] {p}")
        plat = input("\n  Escribe la plataforma: ").strip()
        resultado = filtrar_plat(inventario, plat)
        mostrar_inventario_tabla(resultado)
    elif opc == "3":
        generos = list(set(v["genero"] for v in inventario.values()))
        print("\n  Géneros disponibles:")
        for i, g in enumerate(generos, 1):
            print(f"    [{i}] {g}")
        gen = input("\n  Escribe el género: ").strip()
        resultado = filtrar_genero(inventario, gen)
        mostrar_inventario_tabla(resultado)
    elif opc == "4":
        ordenado = dict(ordenar_precio(inventario, asc=True))
        mostrar_inventario_tabla(ordenado)
    elif opc == "5":
        ordenado = dict(ordenar_precio(inventario, asc=False))
        mostrar_inventario_tabla(ordenado)
    elif opc == "6":
        resultado = {k: v for k, v in inventario.items() if hay_stock(v)}
        mostrar_inventario_tabla(resultado)
    elif opc == "7":
        resultado = {k: v for k, v in inventario.items() if not hay_stock(v)}
        mostrar_inventario_tabla(resultado)
    else:
        print("\n  ⚠  Opción inválida.")

    pausar()




#  4. BUSCAR VIDEOJUEGO
def buscar_videojuego():
    cabecera("BUSCAR VIDEOJUEGO")

    print("  [1] Buscar por nombre")
    print("  [2] Buscar por código")
    print("  [0] Volver")
    linea()
    opc = input("  Opción: ").strip()

    if opc == "0":
        return
    elif opc == "1":
        query = input("\n  Ingresa el nombre (o parte de él): ").strip()
        resultado = buscar_nombre(inventario, query)
        if not resultado:
            print("\n  ⚠  No se encontraron resultados.")
        else:
            print(f"\n  Se encontraron {len(resultado)} resultado(s):\n")
            for cod, j in resultado.items():
                mostrar_juego_card(cod, j)
    elif opc == "2":
        codigo = input("\n  Ingresa el código: ").strip().upper()
        if codigo in inventario:
            print()
            mostrar_juego_card(codigo, inventario[codigo])
        else:
            print(f"\n  ⚠  No se encontró el código '{codigo}'.")
    else:
        print("\n  ⚠  Opción inválida.")

    pausar()




#  5. APLICAR DESCUENTO
def aplicar_descuento():
    cabecera("APLICAR / QUITAR DESCUENTO")

    query = input("  Busca el videojuego (nombre o código): ").strip()
    resultado = buscar_nombre(inventario, query) if not query.upper().startswith("VG") else {}

    if query.upper() in inventario:
        resultado = {query.upper(): inventario[query.upper()]}
    elif not resultado:
        resultado = buscar_nombre(inventario, query)

    if not resultado:
        print("\n  ⚠  No se encontraron resultados.")
        pausar(); return

    lista = list(resultado.items())
    print()
    for i, (cod, j) in enumerate(lista, 1):
        mostrar_juego_card(cod, j, numero=i)

    if len(lista) > 1:
        try:
            sel = int(input("  Selecciona el número del juego: ").strip())
            if sel < 1 or sel > len(lista):
                raise ValueError
        except ValueError:
            print("\n  ⚠  Selección inválida.")
            pausar(); return
        codigo = lista[sel - 1][0]
    else:
        codigo = lista[0][0]

    juego = inventario[codigo]
    print(f"\n  Descuento actual: {juego['descuento']}%")
    print("  Ingresa 0 para quitar el descuento.")

    try:
        nuevo_desc = int(input("  Nuevo descuento (%): ").strip())
        if nuevo_desc < 0 or nuevo_desc >= 100:
            raise ValueError
    except ValueError:
        print("\n  ⚠  Descuento inválido (debe ser entre 0 y 99).")
        pausar(); return

    precio_antes = precio_final(juego)
    juego["descuento"] = nuevo_desc
    precio_despues = precio_final(juego)

    print(f"\n  ✅  Descuento actualizado a {nuevo_desc}%")
    print(f"     Precio antes : {precio_fmt(precio_antes)}")
    print(f"     Precio ahora : {precio_fmt(precio_despues)}")
    pausar()




#  6. EDITAR VIDEOJUEGO
def editar_videojuego():
    cabecera("EDITAR VIDEOJUEGO")

    codigo = input("  Ingresa el código del juego a editar: ").strip().upper()
    if codigo not in inventario:
        print(f"\n  ⚠  Código '{codigo}' no encontrado.")
        pausar(); return

    juego = inventario[codigo]
    mostrar_juego_card(codigo, juego)

    print("  ¿Qué deseas editar?")
    print()
    print("  [1] Nombre")
    print("  [2] Plataforma")
    print("  [3] Género")
    print("  [4] Precio")
    print("  [5] Stock")
    print("  [0] Cancelar")
    linea()
    opc = input("  Opción: ").strip()

    if opc == "0":
        return
    elif opc == "1":
        nuevo = input(f"  Nombre actual: {juego['nombre']}\n  Nuevo nombre : ").strip()
        if nuevo:
            juego["nombre"] = nuevo
    elif opc == "2":
        nuevo = input(f"  Plataforma actual: {juego['plataforma']}\n  Nueva plataforma : ").strip()
        if nuevo:
            juego["plataforma"] = nuevo
    elif opc == "3":
        nuevo = input(f"  Género actual: {juego['genero']}\n  Nuevo género : ").strip()
        if nuevo:
            juego["genero"] = nuevo
    elif opc == "4":
        try:
            nuevo = int(input(f"  Precio actual: {precio_fmt(juego['precio'])}\n  Nuevo precio : ").strip())
            if nuevo > 0:
                juego["precio"] = nuevo
            else:
                print("\n  ⚠  El precio debe ser mayor a 0.")
                pausar(); return
        except ValueError:
            print("\n  ⚠  Valor inválido.")
            pausar(); return
    elif opc == "5":
        try:
            nuevo = int(input(f"  Stock actual: {juego['stock']}\n  Nuevo stock : ").strip())
            if nuevo >= 0:
                juego["stock"] = nuevo
            else:
                print("\n  ⚠  El stock no puede ser negativo.")
                pausar(); return
        except ValueError:
            print("\n  ⚠  Valor inválido.")
            pausar(); return
    else:
        print("\n  ⚠  Opción inválida.")
        pausar(); return

    print(f"\n  ✅  Videojuego '{juego['nombre']}' actualizado correctamente.")
    pausar()




#  7. ELIMINAR VIDEOJUEGO
def eliminar_videojuego():
    cabecera("ELIMINAR VIDEOJUEGO")

    codigo = input("  Ingresa el código del juego a eliminar: ").strip().upper()
    if codigo not in inventario:
        print(f"\n  ⚠  Código '{codigo}' no encontrado.")
        pausar(); return

    juego = inventario[codigo]
    mostrar_juego_card(codigo, juego)

    confirmar = input(f"  ¿Seguro que deseas eliminar '{juego['nombre']}'? (s/n): ").strip().lower()
    if confirmar == "s":
        del inventario[codigo]
        print(f"\n  ✅  '{juego['nombre']}' eliminado del inventario.")
    else:
        print("\n  ❌  Eliminación cancelada.")
    pausar()




#  8. REBASTECER STOCK
def reabastecer_stock():
    cabecera("REABASTECER STOCK")

    codigo = input("  Ingresa el código del juego: ").strip().upper()
    if codigo not in inventario:
        print(f"\n  ⚠  Código '{codigo}' no encontrado.")
        pausar(); return

    juego = inventario[codigo]
    mostrar_juego_card(codigo, juego)

    try:
        cantidad = int(input("  ¿Cuántas unidades deseas agregar? ").strip())
        if cantidad <= 0:
            raise ValueError
    except ValueError:
        print("\n  ⚠  Cantidad inválida.")
        pausar(); return

    juego["stock"] += cantidad
    print(f"\n  ✅  Stock actualizado. Nuevo stock: {juego['stock']} unidades.")
    pausar()




#  9. VER TOTAL DE VENTAS E HISTORIAL
def ver_ventas():
    cabecera("REPORTE DE VENTAS")

    if not historial_ventas:
        print("\n  ⚠  No se han registrado ventas aún.\n")
        pausar(); return

    total = total_ventas_fn(historial_ventas)
    unidades = sum(v["cantidad"] for v in historial_ventas)

    print(f"  Total de transacciones : {len(historial_ventas)}")
    print(f"  Total de unidades      : {unidades}")
    print(f"  Total recaudado        : {precio_fmt(total)}")
    linea()

    print(f"\n  {'#':<4} {'FECHA':<18} {'NOMBRE':<36} {'UND':>4} {'TOTAL':>14}")
    linea()
    for i, v in enumerate(historial_ventas, 1):
        nom = v["nombre"][:35]
        print(f"  {i:<4} {v['fecha']:<18} {nom:<36} {v['cantidad']:>4} {precio_fmt(v['total']):>14}")
    linea()
    print(f"  {'':59} {precio_fmt(total):>14}")
    print()

    # Top 3 más vendidos
    conteo = {}
    for v in historial_ventas:
        conteo[v["nombre"]] = conteo.get(v["nombre"], 0) + v["cantidad"]
    top3 = sorted(conteo.items(), key=lambda x: x[1], reverse=True)[:3]

    print("  🏆 Top 3 más vendidos:")
    for i, (nom, cant) in enumerate(top3, 1):
        print(f"     {i}. {nom[:45]} — {cant} und.")

    pausar()




#  MENÚ PRINCIPAL
def menu_principal():
    while True:
        cabecera()
        total_juegos   = len(inventario)
        juegos_stock   = sum(1 for v in inventario.values() if hay_stock(v))
        total_recaudado = total_ventas_fn(historial_ventas)

        print(f"  📦 Productos en inventario : {total_juegos}  ({juegos_stock} con stock)")
        print(f"  💵 Total recaudado         : {precio_fmt(total_recaudado)}")
        linea()
        print()
        print("   1  ➤  Agregar videojuego")
        print("   2  ➤  Vender videojuego")
        print("   3  ➤  Ver inventario")
        print("   4  ➤  Buscar videojuego")
        print("   5  ➤  Aplicar / Quitar descuento")
        print("   6  ➤  Editar videojuego")
        print("   7  ➤  Reabastecer stock")
        print("   8  ➤  Ver ventas y reporte")
        print("   9  ➤  Eliminar videojuego")
        print("   0  ➤  Salir")
        print()
        linea()
        opc = input("  Selecciona una opción: ").strip()

        acciones = {
            "1": agregar_videojuego,
            "2": vender_videojuego,
            "3": ver_inventario,
            "4": buscar_videojuego,
            "5": aplicar_descuento,
            "6": editar_videojuego,
            "7": reabastecer_stock,
            "8": ver_ventas,
            "9": eliminar_videojuego,
        }

        if opc == "0":
            cabecera()
            centrar("¡Hasta luego! Gracias por usar GameStore Pro 🎮")
            print()
            break
        elif opc in acciones:
            acciones[opc]()
        else:
            print("\n  ⚠  Opción inválida. Intenta de nuevo.")
            pausar()




#  PUNTO DE ENTRADA
if __name__ == "__main__":
    menu_principal()
