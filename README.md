# NetworkingApp

run:
Python snake_server.py
Python snake_client.py

Hard coded for local host: 127.0.0.1 and port 5555

Covers the snake game coded both for server and client side:
1. snake_server.py
   Accepting a connection from a single client.
   Receive and parse the controls sent by the client.
   Managing the game's logic, including recording control inputs, and updating the game state according to the game rules.
   Sending the game state to the client. 

2. snake_client.py
   Connecting to the server.
   Sending user inputs (movements) to the server.
   Receive and parse the game state from the server.
   Displaying the game interface based on the received game state. 

4. snake.py
  contains an implementation of the objects that constitute the snake game (e.g. snake, cube, snack)
  and all the functions that the server needs to run the logic of the game.
