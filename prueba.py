import locale
from datetime import datetime

def calcular_tiempo(tiempo):
    # Establecer la configuración regional en español
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

    # Convertir la cadena de fecha y hora a un objeto datetime
    nuevo_tiempo = datetime.strptime(tiempo, "%Y-%m-%d %H:%M:%S")
    
    # Formatear el tiempo para excluir el año
    tiempo_formateado = nuevo_tiempo.strftime("%d de %B %H:%M:%S")
    
    return tiempo_formateado

# Ejemplo de uso:
cadena_tiempo = "2024-05-03 12:05:06"
resultado = calcular_tiempo(cadena_tiempo)
print("Fecha y hora sin año:", resultado)

