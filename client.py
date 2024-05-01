import socket
import json
import random

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
                elif server_json['request'] == 'play':
                    move = decide_move(server_json)
                    print(f"Move: {move}")  # Add this line
                    response = json.dumps({
                        "response": "move",
                        "move": move,
                        "message": "Fun message"
                    })
                    response_encode = response.encode("utf-8")
                    print("réponse envoyé:", response_encode)
                    conn.sendall(response_encode)
    except Exception as e:
        print("Sent failed", e)

# Appel des fonctions
game_connection(data_connection)
play(data_pong)



   

    