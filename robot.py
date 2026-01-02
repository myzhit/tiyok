import os
import requests
import random

# 1. Recuperamos los secretos de la caja fuerte de GitHub
URL_DESTINO = os.environ["API_URL"]
LLAVE_SECRETA = os.environ["API_KEY"]

print("--- INICIANDO ROBOT DE PRUEBA ---")

# 2. Simulamos que encontramos un video viral (Datos falsos para probar)
datos_falsos = {
    "llave": LLAVE_SECRETA,       # La llave para abrir tu puerta
    "url": "https://tiktok.com/@prueba/video/123456789",
    "vistas": random.randint(100000, 5000000),
    "promedio": 50000,
    "ratio": 15.5
}

print(f"Enviando datos a: {URL_DESTINO}...")

# 3. Enviamos los datos a tu hosting
try:
    respuesta = requests.post(URL_DESTINO, data=datos_falsos)
    
    print(f"Código de estado: {respuesta.status_code}")
    print(f"Respuesta del hosting: {respuesta.text}")
    
    if respuesta.status_code == 200 and "Exito" in respuesta.text:
        print("✅ ¡CONEXIÓN EXITOSA! El dato se guardó en tu base de datos.")
    else:
        print("❌ ALGO FALLÓ. Revisa la respuesta del hosting.")

except Exception as e:
    print(f"❌ Error fatal: {e}")
