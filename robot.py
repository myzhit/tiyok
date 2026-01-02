import os
import requests
import json
import statistics
import time

# --- CONFIGURACIÓN ---
# ¡PON AQUÍ TUS USUARIOS OBJETIVO! (Sin @)
USUARIOS_A_MONITOREAR = ["domelipa", "khaby.lame", "mrbeast"] 

# Umbral: ¿Cuántas veces más vistas que el promedio debe tener para ser viral?
MULTIPLICADOR_VIRAL = 5  # Ej: Si el promedio es 10k, busca videos de 50k+

# --- SECRETOS DE LA BÓVEDA ---
API_KEY_RAPID = os.environ["RAPIDAPI_KEY"]
URL_DESTINO = os.environ["API_URL"]
LLAVE_HOSTING = os.environ["API_KEY"]

def analizar_usuario(username):
    print(f"\n🔍 Analizando a: {username}...")
    
    # 1. Conectar a RapidAPI (Usando apibox o similar)
    url = "https://tiktok-api23.p.rapidapi.com/api/user/posts"
    querystring = {"unique_id": username, "count": "15"} # Analizamos los últimos 15 videos
    
    headers = {
    	"X-RapidAPI-Key": API_KEY_RAPID,
    	"X-RapidAPI-Host": "tiktok-api23.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        
        # Verificar si la API respondió bien
        if "userInfo" not in data and "stats" not in data:
             # Intento de compatibilidad con diferentes respuestas de API
             if "data" in data and "videos" in data["data"]:
                 videos = data["data"]["videos"]
             elif "itemList" in data:
                 videos = data["itemList"]
             else:
                 print(f"⚠️ No se pudieron leer videos de {username}. Respuesta extraña de API.")
                 return
        else:
             # Si la estructura es diferente, adaptamos (esto varía según la API exacta que usaste)
             videos = data.get("itemList", [])

        if not videos:
            print("❌ No hay videos recientes o perfil privado.")
            return

        # 2. Calcular el Promedio de Vistas (Matemáticas)
        lista_vistas = []
        for v in videos:
            # Extraer vistas (stats.playCount suele ser el standard)
            vistas = v.get("stats", {}).get("playCount", 0)
            lista_vistas.append(vistas)
            
        if not lista_vistas:
            return

        # Usamos la Mediana porque es más precisa que el promedio simple
        mediana_vistas = statistics.median(lista_vistas)
        print(f"📊 Mediana de vistas de {username}: {mediana_vistas}")

        # 3. Buscar Outliers (Las Joyas)
        for v in videos:
            vistas = v.get("stats", {}).get("playCount", 0)
            
            # LA FÓRMULA DEL ÉXITO
            if vistas >= (mediana_vistas * MULTIPLICADOR_VIRAL):
                ratio = round(vistas / mediana_vistas, 2)
                video_url = f"https://www.tiktok.com/@{username}/video/{v['video']['id']}"
                
                print(f"💎 ¡JOYA ENCONTRADA! {ratio}x más viral de lo normal.")
                print(f"   Link: {video_url}")
                
                # 4. Enviar a tu Hosting
                enviar_a_boveda(video_url, vistas, mediana_vistas, ratio)

    except Exception as e:
        print(f"❌ Error analizando a {username}: {e}")

def enviar_a_boveda(url, vistas, promedio, ratio):
    payload = {
        "llave": LLAVE_HOSTING,
        "url": url,
        "vistas": vistas,
        "promedio": promedio,
        "ratio": ratio
    }
    
    try:
        r = requests.post(URL_DESTINO, data=payload)
        if r.status_code == 200:
            print("✅ Guardado en base de datos.")
        else:
            print(f"⚠️ Error guardando en hosting: {r.text}")
    except:
        print("⚠️ Error de conexión con tu hosting.")

# --- BUCLE PRINCIPAL ---
if __name__ == "__main__":
    print("🤖 INICIANDO PROTOCOLO DE BÚSQUEDA VIRAL...")
    for user in USUARIOS_A_MONITOREAR:
        analizar_usuario(user)
        time.sleep(2) # Pausa pequeña para no saturar
    print("🏁 Fin del ciclo.")
