import socket
import json

#variable du message à envoyer au moement de la connexion
data_connection = json.dumps({
   "request": "subscribe",
   "port": 5000, #on précise le port sur lequel le serveur va nous envoyer des requêtes 
   "name": "Ibt",
   "matricules": ["2210", "6780"]
    })

def game_connection(data_connection):
    host, port = ('127.0.0.1', 3000) #On va devoir se connecter sur le port 3000 pour une adresse quelconque
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #le socket client est celui qui commence la communication
    try:
        socket_client.connect((host, port)) #avec le socket client, on essaye de se connecter au serveur
        print("Joueur connecté")
        data_connection = data_connection.encode("utf-8") #on encode en ut8 le message json a envoyer
        socket_client.sendall(data_connection) #on envoie notre message sur le port 3000 via le réseau
        print("message sent")
        response = socket_client.recv(4096) #si le message est bien envoyé, on recoit la réponse de retour 
        json.loads(response.decode()) #on utilise le load pour recevoir du json et le convertir en python
        print(response)
        socket_client.close()
    except Exception:
        print("Connection Failed")

game_connection(data_connection)