import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind(("127.0.0.1", 30002))
server.listen()
conn, addr = server.accept()
print("connected by ", addr)

data = conn.recv(1024)

data_point = 2

username = data[data_point:data[0]+data_point].decode("utf-8")
data_point += data[0] 
info = data[data_point:data[1]+data_point].decode("utf-8")
data_point += data[1] 
public_key = data[data_point:44+data_point].decode("utf-8")
data_point += 44;
profile_picture = data[data_point:64+data_point].decode("utf-8")
data_point += 64;
signature = data[data_point:data_point+88].decode("utf-8")

print(username, info, profile_picture, public_key, signature, data)

conn.send(b"\x00\x00\x00\x08aaaaaaaa")