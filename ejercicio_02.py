#Solicite al cliente su nombre, apellido, edad y correo electrónico.
#Almacene estos datos en variables.
#Los muestre organizados en forma de una tarjeta de presentación en la pantalla.
#¡Espero ver el resultado de tu trabajo pronto!
#Saludos, Mariana
#apellido = input("ingrese su  apellido: ")
#nombre = input("ingrese su nombre: ")
#edad = input(" ingrese su edad: ")
#correo = input(" ingrese su correo: ")

#print("----- TARJETA -----")
#print(f"Apellido: {apellido}")
#print(f"Nombre: {nombre}")
#print(f"Edad: {edad}")
#print(f"Correo: {correo}")
#print("-------------------")



numeros = []
mostrados = []

# cargar números
for i in range(5):
    n = int(input("Ingrese un número: "))
    numeros.append(n)

mayor_cantidad = 0
numero_mas_repetido = 0

for i in range(len(numeros)):
    valor = numeros[i]
    
    if valor not in mostrados:
        cantidad = numeros.count(valor)
        
        if cantidad > mayor_cantidad:
            mayor_cantidad = cantidad
            numero_mas_repetido = valor
        
        mostrados.append(valor)

# resultado
if mayor_cantidad > 1:
    print("El número que más se repite es", numero_mas_repetido, "(", mayor_cantidad, "veces )")
else:
    print("No hay números repetidos")
