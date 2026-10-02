import socket 

HOST = "127.0.0.1" 
PORT = 5555 

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
client.connect((HOST, PORT)) 

message = client.recv(1024).decode("utf-8") 

print("Сообщение от сервера:") 
print(message) 

client.close()