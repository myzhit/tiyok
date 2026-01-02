import os
import requests
import statistics
import time

# --- CONFIGURACIÓN ---
# Tus usuarios a espiar (puedes agregar más)
USUARIOS_A_MONITOREAR = ["domelipa", "khaby.lame", "mrbeast"] 

# ¡MODO FÁCIL! Ponemos 0.1 para que guarde TODO lo que encuentre y veas datos ya.
# Luego lo cambias a 5 cuando quieras solo virales extremos.
MULTIPLICADOR_VIRAL = 0.1  

# --- SECRETOS ---
API_KEY_RAPID = os.environ["RAPIDAPI_KEY"]
URL_DESTINO = os.environ["API_URL"]
LLAVE_HOSTING = os.environ["API_KEY"]

def analizar_usuario(username):
    print(f"\n🔍 Analizando a: {username}...")
    
    # 1. Conectar a RapidAPI (apibox)
    url = "https://tiktok-api23.p.rapidapi.com/api/user/posts"
    querystring = {"unique_id": username, "count": "15"}
    
    headers = {
    	"X-RapidAPI-Key": API_KEY_RAPID,
    	"X-RapidAPI-Host": "tiktok-api23.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        
        # Intentamos leer los videos donde sea que vengan
        videos = data.get("itemList", [])
        if not videos and "data" in data:
            videos = data["data"].get("videos", [])

        if not videos:
            print("❌ No se encontraron videos (Perfil privado o error de API).")
            return

        # 2. Matemáticas
        lista_vistas = []
        for v in videos:
            vistas = v.get("stats", {}).get("playCount", 0)
            lista_vistas.append(vistas)
            
        if not lista_vistas: return

        mediana_vistas = statistics.median(lista_vistas)
        print(f"📊 Mediana de vistas: {mediana_vistas}")

        # 3. Guardar Videos
        for v in videos:
            vistas = v.get("stats", {}).get("playCount", 0)
            
            if vistas >= (mediana_vistas * MULTIPLICADOR_VIRAL):
                ratio = round(vistas / mediana_vistas, 2)
                video_id = v.get("video", {}).get("id", "")
                if not video_id: video_id = v.get("id", "")
                
                video_url = f"https://www.tiktok.com/@{username}/video/{video_id}"
                
                print(f"💎 ENCONTRADO: {video_url} ({ratio}x)")
                enviar_a_boveda(video_url, vistas, mediana_vistas, ratio)

    except Exception as e:
        print(f"❌ Error con {username}: {e}")

def enviar_a_boveda(url, vistas, promedio, ratio):
    payload = {
        "llave": LLAVE_HOSTING,
        "url": url,
        "vistas": vistas,
        "promedio": promedio,
        "ratio": ratio
    }
    try:
        requests.post(URL_DESTINO, data=payload)
    except:
        pass

if __name__ == "__main__":
    print("🤖 INICIANDO PROTOCOLO REAL...") # Si ves esto, es el código nuevo
    for user in USUARIOS_A_MONITOREAR:
        analizar_usuario(user)
        time.sleep(1)
    print("🏁 Fin.")
