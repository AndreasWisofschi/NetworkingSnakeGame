import pygame
import socket
import threading
from threading import Lock

def listen_for_server_messages(client_socket, snake_positions, snack_positions, data_lock):
    while True:
        try:
            server_message = client_socket.recv(1024).decode()
            #print(server_message)

            if '|' in server_message:
                with data_lock:
                    snake_data, snacks_data = server_message.split('|')
                    snake_positions[:] = [tuple(map(int, pos.strip('()').split(','))) for pos in snake_data.split('*')]
                    snack_positions[:] = [tuple(map(int, pos.strip('()').split(','))) for pos in snacks_data.split('**')]
                    #print("Server data received and positions updated")  # Debug output
        except BlockingIOError:
            # No data available, continue the loop
            continue
        except ConnectionResetError:
            break
        except ValueError as ve:
            print(f"ValueError occurred: {ve}")
            pass

def snake_game(server_ip, server_port):
    pygame.init()
    lock = Lock()
    black = (0, 0, 0)
    grey = (150, 150, 150)
    green = (0, 255, 0)
    red = (255, 0, 0)

    width, height = 400, 400
    game_display = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Snake Game')
    clock = pygame.time.Clock()
    snake_block = 20

    snake_positions = []
    snack_positions = []

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    threading.Thread(target=listen_for_server_messages, args=(client_socket, snake_positions, snack_positions, lock), daemon=True).start()

    def our_snake(snake_block, snake_list):
        first_square = True
        for x, y in snake_list:
            pygame.draw.rect(game_display, red, [x * snake_block, y * snake_block, snake_block, snake_block])
            if first_square:
                font = pygame.font.SysFont(None, int(snake_block))
                text = font.render('  ••', True, (0, 0, 0))  # Assuming black color for text
                game_display.blit(text, (x * snake_block, y * snake_block))
                first_square = False


    def draw_snacks(snack_list):
        for x, y in snack_list:
            pygame.draw.rect(game_display, green, [x * snake_block, y * snake_block, snake_block, snake_block])

    def draw_grid():
        for x in range(0, width, snake_block):
            pygame.draw.line(game_display, grey, (x, 0), (x, height))
        for y in range(0, height, snake_block):
            pygame.draw.line(game_display, grey, (0, y), (width, y))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client_socket.close()
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    client_socket.send(b'left')
                if event.key == pygame.K_RIGHT:
                    client_socket.send(b'right')
                if event.key == pygame.K_UP:
                    client_socket.send(b'up')
                if event.key == pygame.K_DOWN:
                    client_socket.send(b'down')
                if event.key == pygame.K_g:
                    client_socket.send(b'get')
                    print("\nGame state:\nSnake Position: ",snake_positions,"\nSnack Position: ",snack_positions)
                if event.key == pygame.K_r:
                    client_socket.send(b'reset')
                if event.key == pygame.K_q:
                    client_socket.send(b'quit')
                    pygame.quit()
                    quit()

        game_display.fill(black)

        with lock:
            our_snake(snake_block, snake_positions)
            draw_snacks(snack_positions)

        draw_grid()

        pygame.display.update()
        clock.tick(30)

        #In order to get constant time updates on coordinates i need to call this at every step.
        client_socket.send("get".encode())


if __name__ == "__main__":
    snake_game('127.0.0.1', 5555)