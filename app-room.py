
import libroom
import sys
import socket
import selectors
import traceback
# Create a new server socket for the room

sel = selectors.DefaultSelector()

rsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
rsock.bind(('localhost', 0))  # Bind to a random port on localhost
rsock.listen()
rsock.setblocking(False)
sel.register(rsock, selectors.EVENT_READ, data=None)
print(f"Room created at {(rsock.getsockname())}")

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    message = libroom.Message(sel, conn, addr)
    sel.register(conn, selectors.EVENT_READ, data=message)
    players.append((conn, addr))
    print(f"Player connected to room from {addr}")

# Wait for up to 4 players to join the room
players = []
try:    
    while len(players) < 4:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                message = key.data
                try:
                    message.process_events(mask)
                except Exception:
                    print(
                        f"Main: Error: Exception for {message.addr}:\n"
                        f"{traceback.format_exc()}"
                    )
                    message.close()

except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()

# Start the game once all 4 players have joined
print("All players have joined the room. Starting the game...")
# TODO: Implement game logic here

# HOST = "127.0.0.1"
# PORT = 5001
# MAX_PLAYERS = 4

# players = []

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((HOST, PORT))
# s.listen()

# while True:
#     conn, addr = s.accept()
#     print(f"Player {len(players)+1} connected from {addr}")
#     players.append((conn, addr))
#     if len(players) == MAX_PLAYERS:
#         print("Starting game...")
#         # TODO: Start the game