print("---INICIANDO SISTEMA DE DETENCION DE SPAM ---")
correo = ("¡Ganaste un precio gratis!")
palabra_sospechosa = "premio"
if palabra_sospechosa in correo.lower():
    print("alerta: Este correo parece SPAM.")
else : 
    print ("Correo seguro.Enviado a la bandeja de entrada.")     

