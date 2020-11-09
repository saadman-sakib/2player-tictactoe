import socket
import _thread
import pickle
import time
import copy


IP = "192.168.43.189"
PORT = 5004
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server.bind((IP, PORT))
except socket.error as e:
    quit(e)

server.listen()
print("Waiting for a connection, Server Started")


class TickTackToe:
    def __init__(self):
        self.board = [[None, None, None],
                      [None, None, None],
                      [None, None, None]]

        self.player1 = "X"
        self.player2 = "O"
        self.message = "All good"

    def player(self):
        X = "X"
        O = "O"

        num_x = 0
        num_o = 0
        for row in self.board:
            for col in row:
                if col == X:
                    num_x += 1
                elif col == O:
                    num_o += 1
        if num_x > num_o:
            return O
        else:
            return X

    def update_board(self, move, player):
        if self.board[move[0]][move[1]] == None:
            self.board[move[0]][move[1]] = player
            self.message = "All good"
        else:
            self.message = "cheater detected"

    def winner(self):
        X = "X"
        O = "O"

        def check_win(_x):
            for i in range(3):
                if self.board[i] == [_x,_x,_x] or [x[i] for x in self.board] == [_x,_x,_x]:
                    return True

            if (self.board[0][0] ==_x and self.board[1][1] == _x and self.board[2][2] == _x) or (self.board[0][2] ==_x and self.board[1][1] == _x and self.board[2][0] == _x):
                return True

        if check_win(O):
            return O
        elif check_win(X):
            return X
        else:
            return None

    def end(self):
        if self.winner() != None or self.tie() == True:
            return True
        else:
            return False

    def tie(self):
        for x in self.board:
            for y in x:
                if y == None:
                    return False

        if self.winner() != None:
            return False

        return True



empty_board = [[None, None, None],
               [None, None, None],
               [None, None, None]]

def threaded_gaming(connection1, connection2, player, game):
    time.sleep(.1)

    empty_board = [[None, None, None],
                   [None, None, None],
                   [None, None, None]]
                   
    connection1.send(pickle.dumps((empty_board ,player)))
    
    while True:
        try:
            
            move1 = pickle.loads(connection1.recv(4096))
            if player != game.player():
                continue

            try:
                a, b = move1 #checking move1 is a 2 element tuple

                game.update_board(move1, player)

                if game.winner() == player:
                    connection1.send(pickle.dumps((game.board, "you win")))
                    connection2.send(pickle.dumps((game.board, "you lose")))

                if game.tie():
                    connection1.send(pickle.dumps((game.board, "Tied")))
                    connection2.send(pickle.dumps((game.board, "Tied")))

                if game.end():
                    game.board = copy.deepcopy(empty_board)

                    time.sleep(2)
                    connection1.send(pickle.dumps((game.board, "new match")))
                    connection2.send(pickle.dumps((game.board, "new match")))

                elif game.message == "All good":
                    connection1.send(pickle.dumps((game.board, "You Made Move")))
                    connection2.send(pickle.dumps((game.board, "Your Move")))

                print(game.message)
            except:
                pass
        except socket.error as e:
            print(e)
            break


client_list = []
game_list = []
while True:
    connection, adress = server.accept()
    client_list.append(connection)
    connection.send(pickle.dumps((empty_board, "Waiting for player")))

    print("new_client_connected")

    if len(client_list) == 2:

        game_list.append(TickTackToe())

        _thread.start_new_thread(threaded_gaming,(client_list[-2], client_list[-1], "X", game_list[-1]))
        _thread.start_new_thread(threaded_gaming,(client_list[-1], client_list[-2], "O", game_list[-1]))
        client_list.pop(0)
        client_list.pop(0)

