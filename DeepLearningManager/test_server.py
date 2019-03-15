import socket

Task_Port = 8003
server = socket.socket()
server.bind(("localhost",Task_Port))
server.listen(0)
while True:
	conn,addr = server.accept()
	recv_data = bytes.decode(conn.recv(4096))
	if recv_data == "busy":
		conn.send(b"no")
		recv_data = bytes.decode(conn.recv(4096))