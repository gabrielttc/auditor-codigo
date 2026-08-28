numero_1 = int(input("Ingrese un número: "))
numero_2 = int(input("Ingrese un número: "))
numero_3 = int(input("Ingrese un número: "))

# Todos iguales
if numero_1 == numero_2 and numero_1 == numero_3:
    print("Los tres números son iguales:", numero_1)

# Dos iguales
elif numero_1 == numero_2:
    if numero_1 > numero_3:
        print("El mayor es", numero_1, "y está repetido")
    else:
        print("El mayor es", numero_3)

elif numero_2 == numero_3:
    if numero_2 > numero_1:
        print("El mayor es", numero_2, "y está repetido")
    else:
        print("El mayor es", numero_1)

elif numero_1 == numero_3:
    if numero_1 > numero_2:
        print("El mayor es", numero_1, "y está repetido")
    else:
        print("El mayor es", numero_2)

# Todos distintos
else:
    if numero_1 > numero_2 and numero_1 > numero_3:
        print("El mayor es", numero_1)
    elif numero_2 > numero_1 and numero_2 > numero_3:
        print("El mayor es", numero_2)
    else:
        print("El mayor es", numero_3)

