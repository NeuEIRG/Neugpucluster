from multiprocessing import Process
import multiprocessing
import subprocess
import socket
import os
import time
from threading import Lock

Java_Sock_Port = 8001
JAVA_CMD = ['java','-cp','/home/jelix/example-zookeeper.jar','cn.itcast.zk.TestZKClient']

# Me_Flag = False
# Cur_State = []

Me_Flag = multiprocessing.Value("b",0)
Cur_State = multiprocessing.Manager().list([])

def get_Me_Flag():
	return Me_Flag.value

def get_Cur_State():
	return Cur_State


def run_java_sock_proc(Me_Flag,Cur_State):
	server = socket.socket()
	server.bind(('localhost',Java_Sock_Port))
	server.listen(5)
	while True:
		conn,addr = server.accept()
		recv_list = bytes.decode(conn.recv(4096)).split() 
		while len(Cur_State):
			Cur_State.pop()
		for message in recv_list:
			Cur_State.append(message)
		Me_Flag.value = Cur_State[-1]==Cur_State[-2]
	server.close()


def run_java(name):
    java_proc = subprocess.call(JAVA_CMD,stdout=open('./java_stdout','w'),stderr=open('./java_stderr','w'))

def run_cluster_monitor():
    p = Process(target=run_java_sock_proc, args=(Me_Flag,Cur_State,))
    p.start()
    time.sleep(1)
    r = Process(target=run_java, args=('java',)) 
    r.start()
    r.join()
    p.join()



