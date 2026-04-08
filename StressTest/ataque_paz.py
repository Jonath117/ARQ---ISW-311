import threading
import requests

# Configuración
URL = "http://10.80.114.112:5001/sumar?a=75&b=25"
HILOS = 50  

def enviar_peticiones():
    while True:
        try:
            response = requests.get(URL)
            print(f"Estado: {response.status_code}")
        except:
            print("El servidor no responde")

for i in range(HILOS):
    threading.Thread(target=enviar_peticiones, daemon=True).start()

while True:
    pass