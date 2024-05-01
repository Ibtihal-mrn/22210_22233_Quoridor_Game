#Dans un premier temps, on se connecte au serveur en envoyant une requête (cf github pour le format)
from http import server
import socket
import json
import random

#variable du message à envoyer au mement de la connexion
data_connection = json.dumps({
   "request": "subscribe",
   "port": 5099, #on précise le port sur lequel le serveur va nous envoyer des requêtes 
   "name": "Mournin",
   "matricules": ["22210"]
    })

#variable du pong 
data_pong = json.dumps({"response":"pong"})

#Se connecter au serveur
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


#Il faut commencer par implémenter toutes les méthodes qui permettent de se déplacer
# Déplacement possible : Gauche, droite, haut, bas
# Dans chaque fonction pour aller à gauche droite, etc on va donner une limite
# Dans la disposition du plateau, pour avancer de 1 case je dois faire un bon de deux (cf listes sur github)
#demander à othmane quel est l'intérêt de son return en dictionnaire

# Pour me déplacer, on va faire varier la postion dans la matrice 17x17 en faisant varier l'indice de la ligne ou de la colonne. Le premier indice est celui de la 
# ligne, et le second est celui de la colonne. Ainsi, on va facilement pouvoir vérifier les positions limites aussi  
# Dans chaque méthode, je vais prendre en paramètre ma position actuelle et la mettre à jour. 
# Attention, on avance bien de deux à chaque fois car on doit passer la case du mur. 

#Je vais aussi devoir changer les return False et plutot mettre un message d'erreur

# GERER LES BADS MOVE !!!!! Une fois que j'aurai réussi à faire déplacer convenablement mon pion, je vais ajouter la détetection des murs pour qu'ils ne puissent pas 
# avancer dans ce cas  

def actual_postion(server_json):
    board = server_json['state']['board']
    player = server_json['state']['current'] #current est un paramètre du serveur json 
    for i, elem in enumerate(board): #on parcourt ce qu'il y a dans chaque liste avant de passer à la suivante 
        if  player in elem:
            position_in_list = elem.index(player) #on récupère la position de joueur car le pion est représenté par le 0
            return [i, position_in_list] #on renvoie numéro de la liste où se trouve le joueur et sa position
        
def move_right(actual_position, server_json): 
    pawn = 0
    if server_json["state"]["players"][1] == "Mournin":
        pawn = 1
    if actual_position[1] + 2 < len(server_json["state"]["board"][0]):
        if server_json["state"]["board"][actual_position[0]][actual_position[1] + 2] == 2 and server_json["state"]["board"][actual_position[0]][actual_position[1] + 1] != 4:
            return {"type" : "pawn", "position" : [[actual_position[0], actual_position[1] + 2]]}
        elif server_json["state"]["board"][actual_position[0]][actual_position[1] + 2] == 1 - pawn and actual_position[1] + 4 < len(server_json["state"]["board"][0]) and server_json["state"]["board"][actual_position[0]][actual_position[1] + 4] == 2:
            if server_json["state"]["board"][actual_position[0]][actual_position[1] + 1] != 4 and server_json["state"]["board"][actual_position[0]][actual_position[1] + 3] != 4:
                return {"type" : "pawn", "position" : [[actual_position[0], actual_position[1] + 4]]}
    return False
    

def move_left(server_json, actual_position):
    pawn = 0
    if server_json["state"]["players"][1] == "Mournin":
        pawn = 1
    if actual_position[1] - 2 >= 0:
        if server_json["state"]["board"][actual_position[0]][actual_position[1] - 2] == 2 and server_json["state"]["board"][actual_position[0]][actual_position[1] - 1] != 4:
            return {"type" : "pawn", "position" : [[actual_position[0], actual_position[1] - 2]]}
        elif server_json["state"]["board"][actual_position[0]][actual_position[1] - 2] == 1 - pawn and actual_position[1] - 4 >= 0 and server_json["state"]["board"][actual_position[0]][actual_position[1] - 4] == 2:
            if server_json["state"]["board"][actual_position[0]][actual_position[1] - 1] != 4 and server_json["state"]["board"][actual_position[0]][actual_position[1] - 3] != 4:
                return {"type" : "pawn", "position" : [[actual_position[0], actual_position[1] - 4]]}
    return False
   


def move_top(actual_position, server_json):
    pawn = 0
    if server_json["state"]["players"][1] == "Mournin":
        pawn = 1
    if actual_position[0] - 2 >= 0:
        if server_json["state"]["board"][actual_position[0] - 2][actual_position[1]] == 2 and server_json["state"]["board"][actual_position[0] - 1][actual_position[1]] != 4:
            return {"type" : "pawn", "position" : [[actual_position[0] - 2, actual_position[1]]]}
        elif server_json["state"]["board"][actual_position[0] - 2][actual_position[1]] == 1 - pawn and actual_position[0] - 4 >= 0 and server_json["state"]["board"][actual_position[0] - 4][actual_position[1]] == 2:
            if server_json["state"]["board"][actual_position[0] - 1][actual_position[1]] != 4 and server_json["state"]["board"][actual_position[0] - 3][actual_position[1]] != 4:
                return {"type" : "pawn", "position" : [[actual_position[0] - 4, actual_position[1]]]}
    return False


def move_bottom(actual_position, server_json):
    pawn = 0
    if server_json["state"]["players"][1] == "Mournin":
        pawn = 1
    if actual_position[0] + 2 < len(server_json["state"]["board"]):
        if server_json["state"]["board"][actual_position[0] + 2][actual_position[1]] == 2 and server_json["state"]["board"][actual_position[0] + 1][actual_position[1]] != 4:
            return {"type" : "pawn", "position" : [[actual_position[0] + 2, actual_position[1]]]}
        elif server_json["state"]["board"][actual_position[0] + 2][actual_position[1]] == 1 - pawn and actual_position[0] + 4 < len(server_json["state"]["board"]) and server_json["state"]["board"][actual_position[0] + 4][actual_position[1]] == 2:
            if server_json["state"]["board"][actual_position[0] + 1][actual_position[1]] != 4 and server_json["state"]["board"][actual_position[0] + 3][actual_position[1]] != 4:
                return {"type" : "pawn", "position" : [[actual_position[0] + 4, actual_position[1]]]}
    return False

def decide_move(server_json):
    current_position = actual_postion(server_json)
    possible_moves = []
    if move_top(server_json, current_position):
        possible_moves.append("top")
    if move_bottom(current_position, server_json):
        possible_moves.append("bottom")
    if move_right(current_position, server_json):
        possible_moves.append("right")
    if move_left(current_position, server_json):
        possible_moves.append("left")
    chosen_direction = random.choice(possible_moves)
    #il faut return la nouvelle position plûtot que la direction choisie
    if chosen_direction == "top":
        return move_top(current_position, server_json)
    if chosen_direction == "bottom":
        return move_bottom(current_position, server_json)
    if chosen_direction == "left":
        return move_left(current_position, server_json)
    if chosen_direction == "right":
        return move_right(current_position, server_json)
   

#on va faire appel à la fonction move dans la fonction move player une fois que la direction a été choisi
# def move(server_json, direction):
#     current_position = actual_postion(server_json)
#     if direction == "top":
#         return move_top(current_position)
#     if direction == "bottom":
#         return move_bottom(current_position)
#     if direction == "right":
#         return move_right(current_position)
#     if direction == "left":
#         return move_left(current_position)



# def move_player(server_json): #dans cette fonction on va apprendre à notre ia à se déplacer 
#     while True:
#         direction = decide_move(server_json)
#         if direction is None :
#             print("Aucune direction possible")
#             break #on sort de la boucle
#         else : 
#             new_position = move(server_json, direction)
#             if new_position:
#                 print("Nouvelle position:", new_position )
#             else:
#                 print("déplacement dans la direction", direction, "non autorisé")


#Répondre au Pong
def play(data_pong):
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #le socket serveur est le socket qui écoute, il  ne commence pas la conv
    try:
        socket_server.bind(('0.0.0.0', 5099)) #on lie le socket serveur à une adresse et un port sur lequel on sera en écoute
        socket_server.listen() #on se met en écoute
        print('En écoute') #on va printer ça ici afin de s'assurer que le socket est bien en écoute sur le réseau
        #Entrer dans une boucle infinie pour répondre à des requêtes tants que c'est possible
        while True :
            conn, address = socket_server.accept() #on acccepte les connexions
            server_json = json.loads(conn.recv(10000).decode()) #ping est le message qu'on va recevoir en json, on le décode ensuite
            print("Message reçu:", server_json) 

            #Vérifier qu'il s'agit bien d'une requête
            if "request" in server_json: 
                if server_json['request'] == 'ping':
                    pong = data_pong.encode("utf-8") 
                    conn.sendall(pong) #pour un socket server, c'est avec le conn qu'on doit écouter et envoyer des messages, le socket serveur lui reste à l'écoute des éventuelles connexions
                    print("réponse envoyé:", pong)

                elif server_json['request'] == 'play':
                    move = decide_move(server_json)
                    print(f"Move:{move}")
                    response = json.dumps({ "response": "move", 
                                "move": move, #je comprends pas pourquoi ça marche pas
                                "message": "Fun message"})
                    response_encode = response.encode("utf-8")
                    print("réponse envoyé:", response_encode)
                    conn.sendall(response_encode)
                    print("réponse envoyé:", response_encode)    
                
    except Exception as e:
        print("Sent failed", e)





game_connection(data_connection)
play(data_pong)



   

    