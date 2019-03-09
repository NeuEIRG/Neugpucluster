from multiprocessing import Process
import multiprocessing
import subprocess
import socket
import os
import time
from threading import Lock
import ClusterAPI

Java_Sock_Port = 8001
JAVA_CMD = ['java','-cp','/home/jelix/example-zookeeper.jar','cn.itcast.zk.TestZKClient']


def is_equal(last,cur):
	if not len(last)==len(cur):
		return False
	else:
		for i in range(len(last)):
			if not last[i]==cur[i]:
				return False
		return True

def run_java_sock_proc():
	server = socket.socket()
	server.bind(('localhost',Java_Sock_Port))
	server.listen(5)
	connect_url = ["localhost:27017"]
	cluster = ClusterAPI.Cluster(connect_url)
	Me_Flag = False
	Last_State = []
	while True:
		conn,addr = server.accept()
		recv_list = bytes.decode(conn.recv(4096)).split() 
		Cur_State = []
		for message in recv_list:
			Cur_State.append(message)
		Me_Flag = Cur_State[-1]==Cur_State[-2]
		Cur_State.pop()
		Cur_State.pop()
		if Me_Flag:
			if not is_equal(Last_State,Cur_State):
				cluster.Update_ClusterInfo(Cur_State)
				Last_State = Cur_State
	server.close()


def run_java(name):
    java_proc = subprocess.call(JAVA_CMD,stdout=open('./java_stdout','w'),stderr=open('./java_stderr','w'))

def run_cluster_monitor():
	p = Process(target=run_java_sock_proc)
	p.start()
	time.sleep(1)
	r = Process(target=run_java, args=('java',)) 
	r.start()
	r.join()
	p.join()



