import socket

import json

import random

from simpleai.search import SearchProblem, astar
 
import math as m
# Variables globales

data_connection = json.dumps({

    "request": "subscribe",

    "port": 8791,

    "name": "Ibtihal",

    "matricules": ["22233"]

})

Nom = "Pierrot"

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

        response_json = json.loads(response.decode())  # Reprends les réponses du serveur dans une variable

        print(response_json)  # Affiche ces réponses

        socket_client.close()

    except Exception as e:
        print("Connection Failed:")

 

def actual_postion(server_json):

    board = server_json['state']['board']

    player = server_json['state']['current']

    for i, elem in enumerate(board):

        if player in elem:

            position_in_list = elem.index(player)

            return [i, position_in_list]

 

def move_right(server_json, actual_position):

    pawn = 0

    if server_json["state"]["players"][1] == "Ibtihal":

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

    if server_json["state"]["players"][1] == "Ibtihal":

        pawn = 1

    if -1 < actual_position[1] - 2 < len(server_json["state"]["board"][0]):

        if server_json["state"]["board"][actual_position[0]][actual_position[1] - 2] == 2 and server_json["state"]["board"][actual_position[0]][actual_position[1] - 1] != 4:

            return {"type" : "pawn", "position" : [[actual_position[0], actual_position[1] - 2]]}

        elif server_json["state"]["board"][actual_position[0]][actual_position[1] - 2] == 1 - pawn and actual_position[1] - 4 >= 0 and server_json["state"]["board"][actual_position[0]][actual_position[1] - 4] == 2:

            if server_json["state"]["board"][actual_position[0]][actual_position[1] - 1] != 4 and server_json["state"]["board"][actual_position[0]][actual_position[1] - 3] != 4:

                return {"type" : "pawn", "position" : [[actual_position[0], actual_position[1] - 4]]}

    return False

 

def move_top(server_json, actual_position):

    pawn = 0

    if server_json["state"]["players"][1] == "Ibtihal":

        pawn = 1

    if actual_position[0] + 2 < len(server_json["state"]["board"]):

        if server_json["state"]["board"][actual_position[0] + 2][actual_position[1]] == 2 and server_json["state"]["board"][actual_position[0] + 1][actual_position[1]] != 4:
            print(actual_position[0]+2)
            return {"type" : "pawn", "position" : [[actual_position[0] + 2, actual_position[1]]]}

        elif server_json["state"]["board"][actual_position[0] - 2][actual_position[1]] == 1 - pawn and actual_position[0] - 4 >= 0 and server_json["state"]["board"][actual_position[0] - 4][actual_position[1]] == 2:

            if server_json["state"]["board"][actual_position[0] - 1][actual_position[1]] != 4 and server_json["state"]["board"][actual_position[0] - 3][actual_position[1]] != 4:

                return {"type" : "pawn", "position" : [[actual_position[0] - 4, actual_position[1]]]}
            
    return False

 

def move_bottom(server_json, actual_position):

    pawn = 0

    if server_json["state"]["players"][1] == "Ibtihal":

        pawn = 1

    if actual_position[0] - 2 > -1:

        if server_json["state"]["board"][actual_position[0] - 2][actual_position[1]] == 2 and server_json["state"]["board"][actual_position[0] - 1][actual_position[1]] != 4:

            return {"type" : "pawn", "position" : [[actual_position[0] - 2, actual_position[1]]]}

        elif server_json["state"]["board"][actual_position[0] + 2][actual_position[1]] == 1 - pawn and actual_position[0] + 4 < len(server_json["state"]["board"]) and server_json["state"]["board"][actual_position[0] + 4][actual_position[1]] == 2:

            if server_json["state"]["board"][actual_position[0] + 1][actual_position[1]] != 4 and server_json["state"]["board"][actual_position[0] + 3][actual_position[1]] != 4:

                return {"type" : "pawn", "position" : [[actual_position[0] + 4, actual_position[1]]]}

    return False


class MoveChoice_0(SearchProblem):
    def heuristic(self, server_json, actual_position):
        board = server_json["state"]["board"]  # Récupérer la liste représentant le plateau de jeu
    
        max_distance = 1 # Initialiser la distance maximale à -1

    
        for col_index, cell_value in enumerate(board[16]):  # Parcourir toutes les colonnes de la ligne opposée
        
            distance_to_goal = abs(actual_position[0] + col_index)  # Calculer la distance à cette cellule
        
            max_distance = max(max_distance, distance_to_goal)  # Mettre à jour la distance maximale

        print('Distance_0:', max_distance)
        return max_distance  # Retourner la distance maximale


    def best_first_search(self, server_json, actual_position, moves):
        sorted_moves = sorted(moves, key=lambda move: self.heuristic(server_json, actual_position))

        print('Mouvements triés: ', sorted_moves)

        if move_bottom in sorted_moves:

            sorted_moves.remove(move_bottom)

        best_move = sorted_moves[0]

        return best_move

    def make_move(self, server_json, moves):
        current_position = actual_postion(server_json)
        print(current_position)
        best_move = self.best_first_search(server_json, current_position, moves)
        return best_move

class MoveChoice_1(SearchProblem):
    def heuristic(self, server_json, actual_position):
        board = server_json["state"]["board"] # Récupérer la liste représentant le plateau de jeu
    
        min_distance = float('inf') # Initialiser la distance minimale à l'infini
    
        for col_index, cell_value in enumerate(board[0]): # Parcourir toutes les colonnes et cellules de la ligne opposée
        
            if cell_value != 0: # Si la cellule est bloquée, passer à la suivante
                continue
        
            distance_to_goal = abs(actual_position[0] - col_index) # Calculer la distance à cette cellule
            print('Col_indes:' , col_index)
            print('Position actuelle: ', actual_position)
            print('Distance to goal: ', distance_to_goal)
        
            min_distance = min(min_distance, distance_to_goal) # Mettre à jour la distance minimale
            print('Min distance: ', min_distance)
    
        return min_distance  # Retourner la distance minimale


    def best_first_search(self, server_json, actual_position, moves):
        sorted_moves = sorted(moves, key=lambda move: self.heuristic(server_json, actual_position))

        print('Mouvements triés: ', sorted_moves)

        if move_top in sorted_moves:

            sorted_moves.remove(move_top)

        best_move = sorted_moves[0]       

        return best_move

    def make_move(self, server_json, moves):
        current_position = actual_postion(server_json)

        print(current_position)
        
        best_move = self.best_first_search(server_json, current_position, moves)
        return best_move

M0 = MoveChoice_0()
M1 = MoveChoice_1()

def decide_move0(server_json):
    current_position = actual_postion(server_json)
    possible_moves = []

    if move_top(server_json, current_position):
        possible_moves.append(move_top)

    if move_bottom(server_json, current_position):
        possible_moves.append(move_bottom)

    if move_right(server_json, current_position):
        possible_moves.append(move_right)

    if move_left(server_json, current_position):
        possible_moves.append(move_left)
    
    print ("Indice du joueur: 0")
    print("Possible moves:", possible_moves)

    if possible_moves:
        print('Liste de mouvements crée')
        possible_moves.append(move_top)
        chosen_direction = M0.make_move(server_json, possible_moves)
        print(f"Direction calculée: {chosen_direction.__name__}")
        if chosen_direction:
            return chosen_direction(server_json, current_position)
    else:
        # Si aucun mouvement possible, choisir un mouvement aléatoire
        chosen_direction = random.choice(["top", "bottom", "left", "right"])
        print(f"Direction aléatoire: {chosen_direction.__name__}")
        if chosen_direction == "top":
            return move_top(server_json, current_position)
        elif chosen_direction == "bottom":
            return move_bottom(server_json, current_position)
        elif chosen_direction == "left":
            return move_left(server_json, current_position)
        elif chosen_direction == "right":
            return move_right(server_json, current_position)
        else:
            print('Aucun mouvement fait')

def decide_move1(server_json):
    current_position = actual_postion(server_json)
    possible_moves = []
    print()

    if move_top(server_json, current_position):
        possible_moves.append(move_top)

    if move_bottom(server_json, current_position):
        possible_moves.append(move_bottom)

    if move_right(server_json, current_position):
        possible_moves.append(move_right)

    if move_left(server_json, current_position):
        possible_moves.append(move_left)

    print ("Indice du joueur: 1")
    print("Possible moves:", possible_moves)

    if possible_moves:
        print('Liste de mouvements crée')
        chosen_direction = M1.make_move(server_json, possible_moves)
        print(f"Direction calculée: {chosen_direction.__name__}")
        if chosen_direction:
            return chosen_direction(server_json, current_position)
    else:
        # Si aucun mouvement possible, choisir un mouvement aléatoire
        chosen_direction = random.choice(["top", "bottom", "left", "right"])
        print(f"Direction aléatoire: {chosen_direction.__name__}")
        if chosen_direction == "top":
            return move_top(server_json, current_position)
        elif chosen_direction == "bottom":
            return move_bottom(server_json, current_position)
        elif chosen_direction == "left":
            return move_left(server_json, current_position)
        elif chosen_direction == "right":
            return move_right(server_json, current_position)
        else:
            print('Aucun mouvement fait')

    

def play(data_pong):

    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:

        socket_server.bind(('0.0.0.0', 8791))

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

                elif server_json['request'] == 'play':
                    current_player = server_json['state']['current']

                    if current_player == 0: 
                        move = decide_move0(server_json)

                        print(f"Move: {move}")  # Add this line

                        response = json.dumps({

                            "response": "move",

                            "move": move,

                            "message": "Joue mieux que ca"

                        })

                        response_encode = response.encode("utf-8")

                        print("réponse envoyé:", response_encode)

                        conn.sendall(response_encode)

                    if current_player == 1: 
                        print('OK')
                        move = decide_move1(server_json)

                        print(f"Move: {move}")  # Add this line

                        response = json.dumps({

                            "response": "move",

                            "move": move,

                            "message": "Joue mieux que ca"

                        })

                        response_encode = response.encode("utf-8")

                        print("réponse envoyé:", response_encode)

                        conn.sendall(response_encode)

    except Exception as e:

        print("Sent failed", e) 
# Appel des fonctions

game_connection(data_connection)

play(data_pong)

