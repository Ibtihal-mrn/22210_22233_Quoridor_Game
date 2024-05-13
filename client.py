import socket
import json
import random
from simpleai.search import SearchProblem, astar
import math as m
from collections import deque

 
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


# Fonction de connection au serveur
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

# Fonction qui permet de réperer ma position actuelle à chaque tour 
def actual_position(server_json):
    board = server_json['state']['board']
    player = server_json['state']['current']
    for i, elem in enumerate(board):
        if player in elem:
            position_in_list = elem.index(player)
            return [i, position_in_list]


#Fonction qui calcule la distantce qui me sépare du bord du plateau en fonction de la position initiale (joueur 0 ou 1)
def distance_to_win(server_json, actual_position):

    board = server_json['state']['board']

    if server_json['state']['current'] == 0 : # Je vérifie que je suis le joueur 0
        print('Indice de mon pion:', server_json['state']['current'])
        print('Longueur du plateau:', len(board))
        a = len(board) - actual_position[0] - 1
        print('Ma distance calculée:',a)
        return a  # Je renvoie la distance verticale qui me sépare du bord  
     
    # Je vérifie si la case sur laquelle je me trouve est un 1
    elif  server_json['state']['current'] == 1 :
            print('Indice de mon pion:', server_json['state']['current']) 
            print('Longueur du plateau:', len(board)) # Je renvoie la distance verticale qui me renvoie du bord
            board_length = len(board)
            Distance_1 = 17 - actual_position[0] 
            a = board_length - Distance_1
            print('Ma distance calculée:',a)
            return a

# Fonction qui permet de calculer la distance qui séparer le joueur 2 du bord du plateau en fonction de sa position intiale (joueur 1 ou 0)           
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

# Fonctions qui gèrent les déplacements à gauche, à droite, en haut, en bas

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
        elif server_json["state"]["board"][actual_position[0] + 1][actual_position[1]] == 4 and server_json["state"]["board"][actual_position[0] + 2][actual_position[1]] == pawn_2 :
            return False


 
def move_bottom(server_json, actual_position):
    pawn_2 = float(1)
    if server_json["state"]["players"][1] == "Ibtihal":
        pawn_2 = float (0)
    if actual_position[0] - 2 > -1:
    # Condition: Est est possible de descendre ?
        if server_json["state"]["board"][actual_position[0] - 2][actual_position[1]] == 2 and server_json["state"]["board"][actual_position[0] - 1][actual_position[1]] != 4:
            return {"type" : "pawn", "position" : [[actual_position[0] - 2, actual_position[1]]]}
    # Condition: Est est possible de descendre si le joueur est dans la case suivante ?
        elif server_json["state"]["board"][actual_position[0] - 2][actual_position[1]] == pawn_2:
            if server_json["state"]["board"][actual_position[0] - 1][actual_position[1]] != 4 and server_json["state"]["board"][actual_position[0] - 1][actual_position[1]]  > -1 :   # si il n'y a pas de mur entre les 2 joueur
                return {"type" : "pawn", "position" : [[actual_position[0] - 4, actual_position[1]]]}
            if server_json["state"]["board"][actual_position[0] - 1][actual_position[1]] == 4:
                return False 
        # Condition: Est est possible de descendre si il y a un mur ?
        elif server_json["state"]["board"][actual_position[0] - 1][actual_position[1]] == 4:
            return False
        elif server_json["state"]["board"][actual_position[0] - 1][actual_position[1]] == 4 and server_json["state"]["board"][actual_position[0] - 2][actual_position[1]] == pawn_2:
            return False


class MoveChoice_0(SearchProblem):
    def best_first_search(self,server_json, current_position):
        print('Commencement algorithme')
        server_json["state"]["current"] = 0
        pawn_2 = server_json["state"]["current"] + 1      
        board = server_json["state"]["board"]
        board_length = len(board)
        start = (current_position[0], current_position[1])
        end = (float(16),float(7)) 
        queue = deque([(start, [])])
        visited = {start}
        shortest_path = None 
        print('Suite algorithme') 
        while queue:
            print('Suite algorithme 1') 
            (noeud, path) = queue.popleft()
            x, y = noeud
            if x == board_length - 1:
                print('Suite algorithme_x') 
                path = path + [noeud]
            if shortest_path is None or len(path) < len(shortest_path):
                print('Suite algorithme_X2')
                shortest_path = path
            for dx, dy in [(2, 0), (0, 2), (-2, 0), (0, -2)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < board_length  and 0 <= ny < board_length  and (nx, ny) not in visited:
                    print('Nx:',nx)
                    print('Ny:',ny)
                    if board[int(nx)][int(ny)] == pawn_2 and 0 <= x + 2*dx < board_length and 0 <= y + 2*dy < board_length and board[int(x + 2*dx)][int(y + 2*dy)] == 2:
                        if board[int(x + dx//2)][int(y + dy//2)] != 5 and board[int(x + 3*dx//2)][int(y + 3*dy//2)] != 5:
                            if board[int(x + dx)][int(y + dy)] != 4:
                                nx, ny = x + 2*dx, y + 2*dy
                    if board[int(nx)][int(ny)] == 2:
                        if board[int(x + dx//2)][int(y + dy//2)] == 3:
                            if not any(board[i][j] == 4 for i in range(min(int(x), int(nx)), max(int(x), int(nx))+1) for j in range(min(int(y), int(ny)), max(int(y), int(ny))+1)):
                                queue.append(((nx, ny), path + [noeud]))
                                visited.add((nx, ny))
            break
        print('Suite algorithme_2')
        if shortest_path is not None and len(shortest_path) > 1:
            print('Suite algorithme_3')
            next_move = [shortest_path, shortest_path[1]]
            if next_move[0] < actual_position[0]:
                return move_top(server_json,actual_position)
            if next_move[0] > actual_position[0]:
                return move_bottom(server_json,actual_position)
            if next_move[1] < actual_position[1]:
                return move_right(server_json,actual_position)
            if next_move[1] > actual_position[1]:
                return move_left(server_json, actual_position)
    
        else:
            return shortest_path, None

class MoveChoice_1(SearchProblem):
    def best_first_search(self,server_json, current_position):
        print('Commencement algorithme')
        server_json["state"]["current"] = 1
        pawn_2 = server_json["state"]["current"] - 1
        board = server_json["state"]["board"]
        board_length = len(board)
        start = (current_position[0], current_position[1])
        end = (0,7) 
        queue = deque([(start, [])])
        visited = {start}
        shortest_path = None  
        print('Suite algorithme') 
        while queue:
            print('Suite algorithme 1') 
            (noeud, path) = queue.popleft()
            x, y = noeud
            if x == board_length - 1:
                print('Suite algorithme_x') 
                path = path + [noeud]
            if shortest_path is None or len(path) < len(shortest_path):
                print('Suite algorithme_X2') 
                shortest_path = path
            for dx, dy in [(2, 0), (0, 2), (-2, 0), (0, -2)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < board_length  and 0 <= ny < board_length  and (nx, ny) not in visited:
                    print('Nx:',nx)
                    print('Ny:',ny)
                    if board[int(nx)][int(ny)] == pawn_2 and 0 <= x + 2*dx < board_length and 0 <= y + 2*dy < board_length and board[int(x + 2*dx)][int(y + 2*dy)] == 2:
                        if board[int(x + dx//2)][int(y + dy//2)] != 5 and board[int(x + 3*dx//2)][int(y + 3*dy//2)] != 5:
                            if board[int(x + dx)][int(y + dy)] != 4:
                                nx, ny = x + 2*dx, y + 2*dy
                    if board[int(nx)][int(ny)] == 2:
                        if board[int(x + dx//2)][int(y + dy//2)] == 3:
                            if not any(board[i][j] == 4 for i in range(min(int(x), int(nx)), max(int(x), int(nx))+1) for j in range(min(int(y), int(ny)), max(int(y), int(ny))+1)):
                                print('AH BOOOOOOOOOOOOOOOOOOOOOOOOON')
                                queue.append(((nx, ny), path + [noeud]))
                                visited.add((nx, ny))
            break
        print('Suite algorithme_2') 
        if shortest_path is not None and len(shortest_path) > 1:
            print('Suite algorithme_3')
            next_move = [shortest_path, shortest_path[1]]
            if next_move[0] < actual_position[0]:
                return move_top(server_json,current_position)
            if next_move[0] > actual_position[0]:
                return move_bottom(server_json,current_position)
            if next_move[1] < actual_position[1]:
                return move_right(server_json,current_position)
            if next_move[1] > actual_position[1]:
                return move_left(server_json, current_position)
    
        else:
            return shortest_path, None

M0 = MoveChoice_0()
M1 = MoveChoice_1()

    # Maintenant qu'on a la liste de tous les mouv possibles, on va évaluer les possibilités pour choisir quel est le mouvement le plus optimal

    # Pour ce faire, on va poser des conditions en fonctions de si le mouv se trouve dans la liste et ensuite calculer la distance entre la position mise à jour

    # avec le mouv et le bord du plateau.

    # Attention, il va falloir vérifier ces conditions pour les 2 cas, donc en fonction de si je suis en 1 ou en 0

 #Fonction qui permet de choisir un mouvement grâce à l'algorithme dans le cas où on est le joueur 0
def decide_move0(server_json, current_position):
    print ("Indice du joueur: 0")
    chosen_direction = M0.best_first_search(server_json,current_position)
    if chosen_direction:
        return chosen_direction
     
#Fonction qui permet de choisir un mouvement grâce à l'algorithme dans le cas où on est le joueur 1
def decide_move1(server_json, current_position):
    print ("Indice du joueur: 1")
    chosen_direction = M1.best_first_search(server_json,current_position)
    print('Direction:',chosen_direction)
    return chosen_direction
 
#Créer la méthode qui permet d'ajouter des murs

# Pour ajouter des murs, on doit renvoyer une liste de deux listes car le mur se place sur deux coordonées

# Stratégie : je vais essayer de faire en sorte de placer des murs aux alentours de l'adversaire chaque fois que c'est possible, du coup, je dois pouvoir être en mesure

# De connaître la position de mon adversaire après chaque tour

#Cette fonction me permet de placer un mur devant mon adversaire

def add_blocker_0(server_json,current_position):

    #Commencer par déterminer si je suis le 1 ou le 0

    board = server_json['state']['board']

    # par défaut je suis le joueur 0

    #Mais si dans l'état du jeu je correspond au seconde jouer, alors je suis sur une case 1, ce qui implique que le joueur 2 est sur la case 0

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
                break
        print("La position de mon adversaire pour le bloquer est", position_player_2)
        if position_player_2[0] - 1 > -1 and position_player_2[1] +2 < len(server_json["state"]["board"]):

            if server_json["state"]["board"][position_player_2[0]-1][position_player_2[1]] == 3 and server_json["state"]["board"][position_player_2[0]-1][position_player_2[1]+2] == 3:

                return {"type" : "blocker", "position" : [[position_player_2[0] - 1, position_player_2[1]], [position_player_2[0] - 1, position_player_2[1] + 2]]}
        
            else:
                move = decide_move0(server_json, current_position)
                print ("Si tu peux pas bloquer, bouge au moins")
                return move
            
        if position_player_2[0] - 1 == 4:
            print ("Si tu peux pas bloquer, bouge au moins")
            move = decide_move0(server_json, current_position)
            return move
         
def add_blocker_1(server_json, current_position):
    board = server_json['state']['board']
    board_length = len(board)
    # par défaut je suis le joueur 1

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
                break  
        
        print("La position de mon adversaire pour le bloquer est", position_player_2)

        if position_player_2[0] + 1 < board_length and position_player_2[1] + 2 < board_length:
            print('OK')
        # Je vais vérifier si les deux coordonnées où je veux mettre un mur sont dispo dispo pour un mur car 3 représente une case pour un mur où il n'y en a pas encore
            if server_json["state"]["board"][position_player_2[0]+1][position_player_2[1]] == 3 and server_json["state"]["board"][position_player_2[0]+1][position_player_2[1]+2] == 3:
                print('OK2')
                return{
                    "type" : "blocker", 
                    "position" : [[position_player_2[0]+1, position_player_2[1]], [position_player_2[0]+1, position_player_2[1]+2]]          
                }
            else:
                print ("OK3")
                move = decide_move1(server_json, current_position)
                print ("Si tu peux pas bloquer, bouge au moins")
                return move
        if position_player_2[0] + 1 == 4:
            print ("Si tu peux pas bloquer, bouge au moins")
            move = decide_move1(server_json, current_position)
            return move

# Création des fonctions décidant de la méthode de jeu
def strategy_0(server_json, current_position):
    board = server_json["state"]["board"]
    if server_json["state"]["players"][0] == "Ibtihal":
        pawn_2 = 1
        for i, elem in enumerate(board):
            if pawn_2 in elem:
                position_in_list = elem.index(pawn_2)
        position_player_2 = [i, position_in_list]
        print(position_player_2)

        if  position_player_2[0] - 1 == 4 and position_player_2[1] -1 == 4:
            move = decide_move0(server_json, current_position)
            return move
        else :
            print('OK20')
            move = add_blocker_0(server_json, current_position) #si il est pas bloqué, je le bloque
            print('Je te bloque hehe_0: ',move)
            return move

 
def strategy_1(server_json, current_position):
    board = server_json["state"]["board"]
    if server_json["state"]["players"][1] == "Ibtihal":
        pawn_2 = 0
        #récuperer la position de mon adversaire
        for i, elem in enumerate(board):
            if pawn_2 in elem:
                position_in_list = elem.index(pawn_2)
        position_player_2 = [i, position_in_list]
        # vérifier si mon player_2 est bloqué
        if  position_player_2[0] + 1 == 4 and position_player_2[1] + 1 == 4:
            #si il est bloqué, je peux avancer
            move = decide_move1(server_json, current_position)
            print('Verif_bouger:', move)
            return move
        else:
            move = add_blocker_1(server_json, current_position) #si il est pas bloqué, je le bloque
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
                        print('Ok0')
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
                        print('OK1')
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
                            print(f"Movuvement effectué_1: {move}")  # Add this line
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
