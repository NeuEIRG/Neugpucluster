from multiprocessing import Process
import subprocess
import socket
import os
import time
from threading import Lock

Java_Sock_Port = 8001
JAVA_CMD = ['java','-cp','/home/jelix/example-zookeeper.jar','cn.itcast.zk.TestZKClient']

Me_Flag = False
Cur_State = []
lock = Lock()

def get_Me_Flag():
	lock.acquire()
	r = Me_Flag
	lock.release()
	return r

def get_Cur_State():
	lock.acquire()
	r = Cur_State
	lock.release()
	return r


def run_java_sock_proc(name):
	print('Run child process %s (%s)...' % (name, os.getpid()))
	server = socket.socket()
	server.bind(('localhost',Java_Sock_Port))
	server.listen(5)
	django_proc_flag = False
	django_proc = Process(target=run_django_server, args=('test_django',)) 
	while True:
		conn,addr = server.accept()
		lock.acquire()
		Cur_State = bytes.decode(conn.recv(4096)).split() 
		Me_Flag = data[-1]==data[-2]
		lock.release()
	server.close()

def run_java(name):
    java_proc = subprocess.call(JAVA_CMD,stdout=open('./test_1.out','w'),stderr=open('./test_2.out','w'))

def run_cluster_monitor():
    p = Process(target=run_java_sock_proc, args=('test_java_sock',))
    p.start()
    time.sleep(1)
    r = Process(target=run_java, args=('test_java',)) 
    r.start()
    r.join()
    p.join()



