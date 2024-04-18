#Dans un premier temps, on se connecte au serveur en envoyant une requête (cf github pour le format)
import socket
import json

#variable du message à envoyer au moement de la connexion
data_connection = json.dumps({
   "request": "subscribe",
   "port": 5001, #on précise le port sur lequel le serveur va nous envoyer des requêtes 
   "name": "Mournin",
   "matricules": ["210", "6790"]
    })

#variable du pong 
data_pong = json.dumps({"response":"pong"})


def game_connection(data_connection): #Fonction qui gère la connection du jeu : on envoie la requete et on recoit bien la réponse du serveur
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



def game_ping_pong(data_pong):
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #le socket serveur est le socket qui écoute, il  ne commence pas la conv
    try:
        socket_server.bind(('0.0.0.0', 5001)) #on lie le socket serveur à une adresse et un port sur lequel on sera en écoute
        socket_server.listen() #on se met en écoute
        print('En écoute') #on va printer ça ici afin de s'assurer que le socket est bien en écoute sur le réseau
        while True :
            conn, address = socket_server.accept() #on acccepte les connexions
            ping = json.loads(conn.recv(2048).decode()) #ping est le message qu'on va recevoir en json, on le décode ensuite
            print('message received') 
            if "request" in ping: #si le format du message est bon, on va pouvoir renvoyer une réponse
                if ping['request'] == 'ping':
                    print("Format du message correct")
                    data_pong = data_pong.encode("utf-8")
                    conn.sendall(data_pong) #pour un socket server, c'est avec le conn qu'on doit écouter et envoyer des messages, le socket serveur lui reste à l'écoute des éventuelles connexions
                    print("message envoyé")
                else : 
                    print("Format du message incorrect")
    except Exception as e:
        print("Sent failed", e)


game_connection(data_connection)
game_ping_pong(data_pong)