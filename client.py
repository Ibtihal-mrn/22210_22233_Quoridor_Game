import socket
import json
import random
from turtle import position

# Variables globales
data_connection = json.dumps({
    "request": "subscribe",
    "port": 8790,
    "name": "Ibtihal",
    "matricules": ["22210"]
})

data_pong = json.dumps({"response":"pong"})

# Fonctions de connexion et de jeu
def game_connection(data_connection):
    host, port = ('127.0.0.1', 3000)
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        socket_client.connect((host, port))
        print("Joueur connecté")
        data_connection = data_connection.encode("utf-8")
        socket_client.sendall(data_connection)
        print("message sent")
        response = socket_client.recv(4096)
        json.loads(response.decode())
        print(response)
        socket_client.close()
    except Exception:
        print("Connection Failed")

def actual_postion(server_json):
    board = server_json['state']['board']
    player = server_json['state']['current']
    for i, elem in enumerate(board):
        if player in elem:
            position_in_list = elem.index(player)
            return [i, position_in_list]

def move_right(server_json, actual_position):
    pawn = 0
    if server_json["state"]["players"][1] == "Mournin":
        pawn = 1
    # On vérifie que si j'avance de 2 vers la droite, je ne sors pas du terrain
    if actual_position[1] + 2 < len(server_json["state"]["board"][0]): 
        # si je me trouve sur une case 2 = case dispo pour un joueur, et que juste à côté de moi, il y'a pas de 4 = mur donc on vérifie que je peux me déplacer sans sauter par dessus un mur
        if server_json["state"]["board"][actual_position[0]][actual_position[1] + 2] == 2 and server_json["state"]["board"][actual_position[0]][actual_position[1] + 1] != 4:
            # Je return le bon type de move qui ira dans le json response
            return {"type" : "pawn", "position" : [[actual_position[0], actual_position[1] + 2]]}
        # Si la case sur laquelle je veux me déplacer == 1 ou 0 == case du joueur et que la position actuel + 4 car on passe au dessus du joueur ne sort pas du terrain et que que la case + 4 après le joueur vaut 2 = case dispo:
        elif server_json["state"]["board"][actual_position[0]][actual_position[1] + 2] == 1 - pawn and actual_position[1] + 4 < len(server_json["state"]["board"][0]) and server_json["state"]["board"][actual_position[0]][actual_position[1] + 4] == 2:
            # Si la position juste à côté de ma position actuelle n'est pas un mur et pareil dans le cas où je dépasse un joueur d'où le +3:
            if server_json["state"]["board"][actual_position[0]][actual_position[1] + 1] != 4 and server_json["state"]["board"][actual_position[0]][actual_position[1] + 3] != 4:
                # Je return le bon type de move qui ira dans response
                return {"type" : "pawn", "position" : [[actual_position[0], actual_position[1] + 4]]}
    return False

#Pour les autres fonctions (left, top, bottom), on suit la même logique

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

def move_top(server_json, actual_position):
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

def move_bottom(server_json, actual_position):
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
    if move_bottom(server_json, current_position):
        possible_moves.append("bottom")
    if move_right(server_json, current_position):
        possible_moves.append("right")
    if move_left(server_json, current_position):
        possible_moves.append("left")
    chosen_direction = random.choice(possible_moves)
    print(f"Chosen direction: {chosen_direction}")  # Add this line
    if chosen_direction == "top":
        return move_top(server_json, current_position)
    if chosen_direction == "bottom":
        return move_bottom(server_json, current_position)
    if chosen_direction == "left":
        return move_left(server_json, current_position)
    if chosen_direction == "right":
        return move_right(server_json, current_position)

#Créer la méthode qui permet d'ajouter des murs
# Pour ajouter des murs, on doit renvoyer une liste de deux listes car le mur se place sur deux coordonées

# Stratégie : je vais essayer de faire en sorte de placer des murs aux alentours de l'adversaire chaque fois que c'est possible, du coup, je dois pouvoir être en mesure 
# De connaître la position de mon adversaire après chaque tour 

def add_blocker(server_json):
    #Commencer par déterminer si je suis le 1 ou le 0
    board = server_json['state']['board']
    pawn = 1
    #position_player_2=None
    if server_json["state"]["players"][1] == "Mournin":
        pawn = 0
        
        for i, elem in enumerate(board):
            if pawn in elem:
                position_in_list = elem.index(pawn)
                position_player_2=[i, position_in_list]
        print("La position de mon adversaire est", position_player_2)
        if position_player_2[0] + 1 < len(server_json["state"]["board"]) and position_player_2[1]+2 < len(server_json["state"]["board"]) or position_player_2[2]-2 > 0:
        #je vais vérifier si les deux coordonnées où je veux mettre un mur sont dispo dispo pour un mur car 3 représente une case pour un mur où il n'y en a pas encore
            if server_json["state"]["board"][position_player_2[0]+1][position_player_2[1]] == 3 and server_json["state"]["board"][position_player_2[0]+1][position_player_2[1]+2] == 3:
                return{"type" : "blocker", "position" : [[position_player_2[0]+1, position_player_2[1]], [position_player_2[0]+1, position_player_2[1]+2]]}
    else : 
        for i, elem in enumerate(board):
            if pawn in elem:
                position_in_list = elem.index(pawn)
                position_player_2 = [i, position_in_list]
        print("position player 2", position_player_2)
        if position_player_2[0]-1 > 0 and position_player_2[1]+2 < len(server_json["state"]["board"]) or position_player_2[1]-2 >0:
            if server_json["state"]["board"][position_player_2[0]-1][position_player_2[1]] == 3 and server_json["state"]["board"][position_player_2[0]-1][position_player_2[1]+2] == 3:
                return {"type" : "blocker", "position" : [position_player_2[0]-1, position_player_2[1], [position_player_2[0]-1, position_player_2[1]+2]]}


def play(data_pong):
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        socket_server.bind(('0.0.0.0', 8790))
        socket_server.listen()
        print('En écoute')
        while True:
            conn, address = socket_server.accept()
            server_json = json.loads(conn.recv(10000).decode())
            print("Message reçu:", server_json)
            if "request" in server_json:
                if server_json['request'] == 'ping':
                    pong = data_pong.encode("utf-8")
                    conn.sendall(pong)
                    print("réponse envoyé:", pong)
                # elif server_json['request'] == 'play':
                #     move = decide_move(server_json)
                #     print(f"Move: {move}")  # Add this line
                #     response = json.dumps({
                #         "response": "move",
                #         "move": move,
                #         "message": "Fun message"
                #     })
                #     response_encode = response.encode("utf-8")
                #     print("réponse envoyé:", response_encode)
                #     conn.sendall(response_encode)
                elif server_json['request'] == 'play':
                    block = add_blocker(server_json)
                    response = json.dumps({
                        "response": "move",
                        "move": block,
                        "message": "fun message"
                    })
                    response_encode = response.encode("utf-8")
                    print("réponse envoyé:", response_encode)
                    conn.sendall(response_encode)
                    

    except OSError as e:
        print("Sent failed", e)

# Appel des fonctions
game_connection(data_connection)
play(data_pong)



   

    