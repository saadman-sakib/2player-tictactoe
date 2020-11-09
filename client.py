import socket
import _thread
import pickle
import pygame
import time

pygame.init()
size = width, height = 600, 400

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode(size)

mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)


IP = "192.168.43.189"
PORT = 5004

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

#window_drawing

title = largeFont.render("Play Tic-Tac-Toe", True, white)
titleRect = title.get_rect()
titleRect.center = ((width / 2), 50)
screen.blit(title, titleRect)

temp_data = {0:[[None, None, None],
                [None, None, None],
                [None, None, None]],
             1: "",
             2: None}

result = {0: None,
          1: None}

def receive():
    while True:
        try:
            data = pickle.loads(client.recv(4096*8))  #update the temp data
            if data[1] == "O":
                temp_data[2] = "O"
                temp_data[1] = "You will play O"
            elif data[1] == "X":
                temp_data[2] = "X"
                temp_data[1] = "You will play X"
            else:
                temp_data[0] = data[0]
                temp_data[1] = data[1]

        except socket.error as e:
            quit(e)

def send():
    while True:
        if result[1] != result[0]:
            result[1] = result[0]
            client.send(pickle.dumps(result[0]))


_thread.start_new_thread(receive,())
_thread.start_new_thread(send,())

while True:
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        screen.fill(black)

        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size),
                       height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, white, rect, 3)

                move = moveFont.render(temp_data[0][i][j], True, white)
                moveRect = move.get_rect()
                moveRect.center = rect.center
                screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)


        title = temp_data[1]
        title = largeFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = (int(width / 2), 30)
        screen.blit(title, titleRect)

        pygame.display.update()
        pygame.display.flip()

        left, _, right = pygame.mouse.get_pressed()

        if left == 1:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if tiles[i][j].collidepoint(mouse):
                        result[0] = (i, j)

    except socket.error as e:
        time.sleep(10)
        print(e)

