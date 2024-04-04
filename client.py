#Dans un premier temps, on se connecte au serveur en envoyant une requête (cf github pour le format)
import socket
import json

host, port = ('127.0.0.1', 3000)

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    socket.connect((host, port))
    print("Client connecté")

    
    data = json.dumps({
   "request": "subscribe",
   "port": 3000,
   "name": "Ibtihal",
   "matricules": ["22210", "67890"]
    })
    data = data.encode("utf-8")
    socket.sendall(data) #on envoie notre message sur le port 3000 svia le réseau
    response = json.loads(socket.recv(2048).decode())
    print(response)

except:
    print("Connexion au serveur échouée!")
finally: #on demande de fermer le socket dans tous les cas
    socket.close()

    