# Sistema de Gestión de Productos
# Autor: Gabriel Carrizo

# Lista principal donde se almacenarán los productos
productos = []

# Función para mostrar el menú
def mostrar_menu():
    print("\n--- MENÚ DE OPCIONES ---")
    print("1. Agregar producto")
    print("2. Mostrar productos")
    print("3. Buscar producto")
    print("4. Eliminar producto")
    print("5. Salir")


# Función para agregar productos
def agregar_producto():
    print("\n--- AGREGAR PRODUCTO ---")

    # Validación del nombre
    while True:
        nombre = input("Ingrese el nombre del producto: ").strip()
        if nombre != "":
            break
        print("Error: El nombre no puede estar vacío.")

    # Validación de categoría
    while True:
        categoria = input("Ingrese la categoría: ").strip()
        if categoria != "":
            break
        print("Error: La categoría no puede estar vacía.")

    # Validación del precio
    while True:
        precio = input("Ingrese el precio (sin centavos): ")

        if precio.isdigit():
            precio = int(precio)
            break
        else:
            print("Error: Debe ingresar solo números enteros.")

    # Guardar producto en la lista
    producto = [nombre, categoria, precio]
    productos.append(producto)

    print("Producto agregado correctamente.")


# Función para mostrar productos
def mostrar_productos():
    print("\n--- LISTA DE PRODUCTOS ---")

    if len(productos) == 0:
        print("No hay productos registrados.")
    else:
        for i, producto in enumerate(productos, start=1):
            print(f"{i}. Nombre: {producto[0]}")
            print(f"   Categoría: {producto[1]}")
            print(f"   Precio: ${producto[2]}")
            print("-------------------------")


# Función para buscar productos
def buscar_producto():
    print("\n--- BUSCAR PRODUCTO ---")

    nombre_buscar = input("Ingrese el nombre del producto: ").strip().lower()

    encontrado = False

    for producto in productos:
        if nombre_buscar in producto[0].lower():
            print("\nProducto encontrado:")
            print(f"Nombre: {producto[0]}")
            print(f"Categoría: {producto[1]}")
            print(f"Precio: ${producto[2]}")
            encontrado = True

    if not encontrado:
        print("No se encontraron productos con ese nombre.")


# Función para eliminar productos
def eliminar_producto():
    print("\n--- ELIMINAR PRODUCTO ---")

    if len(productos) == 0:
        print("No hay productos para eliminar.")
        return

    mostrar_productos()

    while True:
        opcion = input("Ingrese el número del producto a eliminar: ")

        if opcion.isdigit():
            opcion = int(opcion)

            if 1 <= opcion <= len(productos):
                eliminado = productos.pop(opcion - 1)
                print(f"Producto '{eliminado[0]}' eliminado correctamente.")
                break
            else:
                print("Error: Número fuera de rango.")
        else:
            print("Error: Debe ingresar un número válido.")


# Programa principal
while True:
    mostrar_menu()

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        agregar_producto()

    elif opcion == "2":
        mostrar_productos()

    elif opcion == "3":
        buscar_producto()

    elif opcion == "4":
        eliminar_producto()

    elif opcion == "5":
        print("Saliendo del sistema...")
        break

    else:
        print("Opción inválida. Intente nuevamente.")