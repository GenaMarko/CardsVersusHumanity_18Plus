import socket 

HOST = "0.0.0.0" 
PORT = 5555 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((HOST, PORT)) 
server.listen() 

print("Сервер запущен!") 
print(f"Порт: {PORT}") 
print("Ожидание подключения игрока...") 

while True: 
    connection, address = server.accept() 
    print(f"Игрок подключился: {address}") 
    connection.close()