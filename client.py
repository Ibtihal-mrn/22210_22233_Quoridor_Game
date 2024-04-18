#Dans un premier temps, on se connecte au serveur en envoyant une requête (cf github pour le format)
import socket
import json


host, port = ('127.0.0.1', 3000)
socket_envoie = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #ce socket sert à envoyer des requêtes 
try:
    socket_envoie.connect((host, port))
    print("Client connecté")
# Dans cette partie, on envoie un message au serveur
    data = json.dumps({
   "request": "subscribe",
   "port": 4000, #on précise le port sur lequel le serveur va nous envoyer des requêtes 
   "name": "Ibtihal",
   "matricules": ["22210", "67890"]
    })
    data = data.encode("utf-8")
    socket_envoie.sendall(data) #on envoie notre message sur le port 3000 svia le réseau
    response = socket_envoie.recv(4096)
    json.loads(response.decode())
    print(response)
    socket_envoie.close()


#Partie de code qui permet de recevoir des requetes, on va donc devoir créer un autre socket
    
    socket_reçu = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #cette ligne spécifie le type de socket, TCP communication
    socket_reçu.bind(('0.0.0.0', 4000)) #on lie le socket au port 4000, c'est sur ce port qu'on va recevoir des messages
    while True:
        socket_reçu.listen()
        conn, address = socket_reçu.accept() #
        print("En écoute")


        ping = json.loads(conn.recv(2048).decode()) #conn pour dire que je recois le message 
        print(ping)

        #on s'assure que le type du message est un request
        # if ping.get("type") == "request":
        #     pong = json.dumps({"response":"pong"}).encode("utf-8")
        #     socket_envoie.sendall(pong)
    
        socket_reçu.close()

# except:
#     print("Connexion au serveur échouée!")

except Exception as e:
    print("Connexion au serveur échouée :", e)


   

    