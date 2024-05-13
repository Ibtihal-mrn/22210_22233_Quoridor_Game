import socket
import json
import random
from simpleai.search import SearchProblem, astar 
 
# Variables globales
data_connection = json.dumps({
    "request": "subscribe",
    "port": 8793,
    "name": "Ibtihal",
    "matricules": ["22210"]
})
data_pong = json.dumps({"response":"pong"})
Random_1 = random.choice([1, -1])
Random_2 = random.choice([2, -2])

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
 
def actual_position(server_json):
    board = server_json['state']['board']
    player = server_json['state']['current']
    for i, elem in enumerate(board):
        if player in elem:
            position_in_list = elem.index(player)
            return [i, position_in_list]

# Créer des fonctions qui calcule la distantce qui me sépare du bord du plateau 
def distance_to_win(server_json, actual_position):
    board = server_json['state']['board']
    if server_json['state']['current'] == 0 : 
        print('Indice de mon pion:', server_json['state']['current'])
        a = len(board) - actual_position[0] - 1
        print('Ma distance calculée:',a)
        return a    
    elif  server_json['state']['current'] == 1 :            
            print('Indice de mon pion:', server_json['state']['current'])        
            print('Longueur du plateau:', len(board)) 
            board_length = len(board)
            Distance_1 = 17 - actual_position[0] 
            a = board_length - Distance_1
            print('Ma distance calculée:',a)
            return a

# Créer des fonctions qui calcule la distantce qui sépare le joueur 2 du bord du plateau          
def distance_player2_to_win(server_json):
    board = server_json['state']['board']
    board_length = len(board)
    pawn = 0
    if server_json["state"]["players"][1] == "Ibtihal" :       
        pawn_2 = 0
        for i, elem in enumerate(board):
            if pawn_2 in elem:
                position_player_2 = i
        return board_length - position_player_2
    else :
        pawn_2 = 1
        for i, elem in enumerate(board):
            position_player_2 = i
        Distance = board_length - position_player_2
        a = board_length - Distance 
        return a

# Création des fonctions de mouvements
def move_right(server_json, actual_position): # Se déplacer à droite
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

def move_left(server_json, actual_position): # Se déplacer à gauche
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

def move_top(server_json, actual_position): # Se déplacer vers le haut
    pawn_2 = float(1)
    if server_json["state"]["players"][1] == "Ibtihal":
        pawn_2 = float (0)
    if actual_position[0] + 2 < len(server_json["state"]["board"]):
        board = server_json["state"]["board"]

        # Condition: Est est possible de monter?
        if server_json["state"]["board"][actual_position[0] + 2][actual_position[1]] == 2 and server_json["state"]["board"][actual_position[0] + 1][actual_position[1]] != 4:
            return {"type" : "pawn", "position" : [[actual_position[0] + 2, actual_position[1]]]}
        
        # Condition: Est est possible de monter si le joueur est dans la case suivante ?
        elif server_json["state"]["board"][actual_position[0] + 2][actual_position[1]] == pawn_2 and server_json["state"]["board"][actual_position[0] + 2][actual_position[1]] < len(board):
            if server_json["state"]["board"][actual_position[0] + 1][actual_position[1]] != 4:   # si il n'y a pas de mur entre les 2 joueurs
                return {"type" : "pawn", "position" : [[actual_position[0] + 4, actual_position[1]]]}           
            if server_json["state"]["board"][actual_position[0] + 1][actual_position[1]] == 4:
                return False      
                  
        # Condition: Est est possible de monter si il y a un mur ?
        elif server_json["state"]["board"][actual_position[0] + 1][actual_position[1]] == 4 :
            return False
        # Condition: Est est possible de monter si il y a un mur et derrière se trouve un joueur
        elif server_json["state"]["board"][actual_position[0] + 1][actual_position[1]] == 4 and server_json["state"]["board"][actual_position[0] + 2][actual_position[1]] == pawn_2 :
            return False

def move_bottom(server_json, actual_position): # Se déplacer vers le bas
    pawn_2 = float(1)
    if server_json["state"]["players"][1] == "Ibtihal":
        pawn_2 = float (0)
    if actual_position[0] - 2 > -1:
    # Condition: Est est possible de descendre ?
        if server_json["state"]["board"][actual_position[0] - 2][actual_position[1]] == 2 and server_json["state"]["board"][actual_position[0] - 1][actual_position[1]] != 4:
            return {"type" : "pawn", "position" : [[actual_position[0] - 2, actual_position[1]]]}
           
    # Condition: Est est possible de descendre si le joueur est dans la case suivante ?
        elif server_json["state"]["board"][actual_position[0] - 2][actual_position[1]] == pawn_2:
            if server_json["state"]["board"][actual_position[0] - 1][actual_position[1]] != 4 and server_json["state"]["board"][actual_position[0] - 1][actual_position[1]]  > -1 :   # si il n'y a pas de mur entre les 2 joueurs
                return {"type" : "pawn", "position" : [[actual_position[0] - 4, actual_position[1]]]}           
            if server_json["state"]["board"][actual_position[0] - 1][actual_position[1]] == 4:
                return False 
                      
    # Condition: Est est possible de descendre si il y a un mur ?
        elif server_json["state"]["board"][actual_position[0] - 1][actual_position[1]] == 4:
            return False       
        elif server_json["state"]["board"][actual_position[0] - 1][actual_position[1]] == 4 and server_json["state"]["board"][actual_position[0] - 2][actual_position[1]] == pawn_2:
            return False

# Classe me permettant de trier la liste de mouvements et en ressortir le meilleur
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
        sorted_moves = sorted(moves, key=lambda move: self.heuristic(server_json, actual_position), reverse = True)
        print('Mouvements triés: ', sorted_moves)
        if move_bottom in sorted_moves:
            sorted_moves.remove(move_bottom)
        best_move = sorted_moves[0]  
        best_move = sorted_moves[0]
        return best_move

    def make_move(self, server_json, current_position, moves):
        best_move = self.best_first_search(server_json, current_position, moves)
        return best_move

# Classe me permettant de trier la liste de mouvements et en ressortir le meilleur
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
    def make_move(self, server_json, current_position, moves):       
        best_move = self.best_first_search(server_json, current_position, moves)
        return best_move

M0 = MoveChoice_0()
M1 = MoveChoice_1()

# Maintenant qu'on a la liste de tous les mouvements possibles, on va évaluer les possibilités pour choisir quel est le mouvement le plus optimal
# Pour ce faire, on va poser des conditions en fonctions de si le mouv se trouve dans la liste et ensuite 
# calculer la distance entre la position mise à jour du mouvement et le bord du plateau.
# Attention, il va falloir vérifier ces conditions pour les 2 cas, donc en fonction de si je suis le joueur 1 ou le joueur 0

def decide_move0(server_json, current_position): # Si je suis le joueur 0
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
        chosen_direction = M0.make_move(server_json, current_position, possible_moves)
        print(f"Direction calculée: {chosen_direction.__name__}")
        if chosen_direction:
            return chosen_direction(server_json, current_position)


def decide_move1(server_json, current_position): # Si je suis le joueur 0
    possible_moves = []
    if move_top(server_json, current_position):
        possible_moves.append(move_top)
    if move_bottom(server_json, current_position):
        possible_moves.append(move_bottom)
    if move_left(server_json, current_position):
        possible_moves.append(move_left)   
    if move_right(server_json, current_position):
        possible_moves.append(move_right)
    print ("Indice du joueur: 1")
    print("Possible moves:", possible_moves)

    if possible_moves:
        print('Liste de mouvements crée')
        chosen_direction = M1.make_move(server_json,current_position, possible_moves)
        print(f"Direction calculée: {chosen_direction.__name__}")
        if chosen_direction:
            return chosen_direction(server_json, current_position)

# Pour ajouter des murs, on doit renvoyer une liste de deux listes car le mur se place sur deux coordonées
# Stratégie : je vais essayer de faire en sorte de placer des murs aux alentours de l'adversaire chaque fois que c'est possible,
# du coup, je dois pouvoir être en mesure de connaître la position de mon adversaire après chaque tour

#Cette fonction me permet de placer un mur devant mon adversaire si je suis le joueur 0
def add_blocker_0(server_json,current_position): 
    board = server_json['state']['board']
    if server_json["state"]["players"][0] == "Ibtihal":
        server_json["state"]["current"] = 0
        pawn_2 = server_json["state"]["current"] + 1        
        s = -1
        p = -1
        position_in_list = None
        position_player_2 = None
        for i in (board):
            s += 1
            print('Ligne',s,':', i)
            if pawn_2 in i:
                for elem in i:
                    p += 1
                    print('Valeur de la cellule:',p)
                    if pawn_2 == int(elem):
                        print('OK')
                        position_in_list = p
                        position_player_2 = [s, position_in_list] 
                        break 
        print("La position de mon adversaire pour le bloquer est", position_player_2)
        if position_player_2[0] - 1 > -1 and position_player_2[1] +2 < len(server_json["state"]["board"]):
             # Vérification des coordonnées où placer un mur sont libre car 3 représente une case pour un mur où il n'y en a pas encore
            if server_json["state"]["board"][position_player_2[0]-1][position_player_2[1]] == 3 and server_json["state"]["board"][position_player_2[0]-1][position_player_2[1]+2] == 3:
                return {"type" : "blocker", "position" : [[position_player_2[0] - 1, position_player_2[1]], [position_player_2[0] - 1, position_player_2[1] + 2]]} 
            else:
                move = decide_move0(server_json, current_position)
                print ("Si tu peux pas bloquer, bouge au moins")
                return move
        else:
            move = decide_move0(server_json, current_position)
            print ("Si tu peux pas bloquer, bouge au moins")
            return move

#Cette fonction me permet de placer un mur devant mon adversaire si je suis le joueur 1
def add_blocker_1(server_json, current_position):
    board = server_json['state']['board']
    board_length = len(board)
    if server_json["state"]["players"][1] == "Ibtihal":
        server_json["state"]["current"] = 1
        pawn_2 = server_json["state"]["current"] - 1       
        s = -1
        p = -1
        position_in_list = None
        position_player_2 = None
        for i in (board):
            s += 1
            print('Ligne',s,':', i)
            if pawn_2 in i:
                for elem in i:
                    p += 1
                    print('Valeur de la cellule:',p)
                    if pawn_2 == int(elem):
                        print('OK')
                        position_in_list = p
                        position_player_2 = [s, position_in_list] 
                        break        
        print("La position de mon adversaire pour le bloquer est", position_player_2)
        if position_player_2[0] + 1 < board_length and position_player_2[1] + 2 < board_length:
        # Vérification des coordonnées où placer un mur sont libre car 3 représente une case pour un mur où il n'y en a pas encore
            if server_json["state"]["board"][position_player_2[0]+1][position_player_2[1]] == 3 and server_json["state"]["board"][position_player_2[0]+1][position_player_2[1]+2] == 3:                
                return{                    
                    "type" : "blocker",                    
                    "position" : [[position_player_2[0]+1, position_player_2[1]], [position_player_2[0]+1, position_player_2[1]+2]]                      
                }
            else:
                move = decide_move1(server_json, current_position)
                print ("Si tu peux pas bloquer, bouge au moins")
                return move
        else:
            move = decide_move1(server_json, current_position)
            print ("Si tu peux pas bloquer, bouge au moins")
            return move

# Création des fonctions décidant de la méthode de jeu
def strategy_0(server_json, current_position): # Si je suis le joueur 0
    board = server_json["state"]["board"]
    if server_json["state"]["players"][0] == "Ibtihal":
        pawn_2 = 1
        for i, elem in enumerate(board): # Récuperer la position de mon adversaire
            if pawn_2 in elem:
                position_in_list = elem.index(pawn_2)
        position_player_2 = [i, position_in_list]
        if  position_player_2[0] - 1 == 4:
            move = decide_move0(server_json, current_position)
            return move
        else :
            move = add_blocker_0(server_json, current_position) #si il est pas bloqué, je le bloque
            print('Je te bloque hehe_0: ',move)
            return move

def strategy_1(server_json, current_position): # Si je suis le joueur 1
    board = server_json["state"]["board"]
    if server_json["state"]["players"][1] == "Ibtihal":
        pawn_2 = 0
        for i, elem in enumerate(board): # Récuperer la position de mon adversaire
            if pawn_2 in elem:
                position_in_list = elem.index(pawn_2)
        position_player_2 = [i, position_in_list]

        if position_player_2[0] + 1 == 4: # Vérifier si mon adversaire est bloqué
            move = decide_move1(server_json, current_position) # Si oui, je peux avancer
            print('Verif_bouger:', move)
            return move      
        else:
            move = add_blocker_1(server_json, current_position) # Si il est pas bloqué, je le bloque
            print('Je te bloque hehe_1',move)
            return move

# Création des fonctions de jeu
def play(data_pong):
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        socket_server.bind(('0.0.0.0', 8793))
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
                    current_position = actual_position(server_json)
                    current_player = server_json['state']['current'] # Indicie de joueur
                    my_distance = distance_to_win(server_json, current_position)
                    print('Ma distance: ', my_distance)
                    your_distance = distance_player2_to_win(server_json)
                    print('Ta distance: ', your_distance)
                    if current_player == 0:
                        if my_distance < your_distance:
                            move = strategy_0(server_json, current_position)
                            print(f"Movuvement effectué_0: {move}")  # Add this line
                            response = json.dumps({
                            "response": "move",
                            "move": move,
                            "message": " C \' est moi qui joue"
                        })
                            response_encode = response.encode("utf-8")
                            print("Coup joué:", response_encode)
                            conn.sendall(response_encode)
                        if my_distance == your_distance:
                            move = strategy_0(server_json, current_position)
                            print(f"Movuvement effectué_0: {move}")  # Add this line
                            response = json.dumps({
                            "response": "move",
                            "move": move,
                            "message": " C \' est moi qui joue"
                        })
                            response_encode = response.encode("utf-8")
                            print("Coup joué:", response_encode)
                            conn.sendall(response_encode)
                        else:      
                            block = add_blocker_0(server_json, current_position)
                            response = json.dumps({
                             "response": "move",
                             "move": block,
                             "message": "Tu passes pas"
                         })
                            response_encode = response.encode("utf-8")
                            print("Blocker envoyé_0:", response_encode)
                            conn.sendall(response_encode)
                    if current_player == 1:
                        if my_distance < your_distance:
                            move = strategy_1(server_json, current_position)
                            print(f"Movuvement effectué_1: {move}")  # Add this line
                            response = json.dumps({
                            "response": "move",
                            "move": move,
                            "message": ' C \' est moi qui joue'
                        })
                            response_encode = response.encode("utf-8")
                            print("Coup joué:", response_encode)
                            conn.sendall(response_encode)
                        if my_distance == your_distance:
                            move = strategy_1(server_json, current_position)
                            print(f"Movuvement effectué_1: {move}")  
                            response = json.dumps({
                            "response": "move",
                            "move": move,
                            "message": ' C \' est moi qui joue'
                        })
                            response_encode = response.encode("utf-8")
                            print("Coup joué:", response_encode)
                            conn.sendall(response_encode)
                        else:      
                            block = add_blocker_1(server_json, current_position)
                            response = json.dumps({
                             "response": "move",
                             "move": block,
                             "message": "Tu passes pas"
                         })
                            response_encode = response.encode("utf-8")
                            print("Blocker envoyé:", response_encode)
                            conn.sendall(response_encode)
    except OSError as e:
        print("Sent failed", e)

# Appel des fonctions
game_connection(data_connection)
play(data_pong)