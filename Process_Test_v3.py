from multiprocessing import Process
import subprocess
import socket
import os
import time

Django_Server_Web_Port = 8000
Java_Sock_Port = 8001
Django_Sock_Port = 8005
               
JAVA_CMD = ['java','-cp','/home/jelix/example-zookeeper.jar','cn.itcast.zk.TestZKClient']
DJANGO_CMD = ['/home/jelix/HelloWorld/manage.py','runserver','0.0.0.0:8000']

def run_django_server(name):
    django_proc = subprocess.call(DJANGO_CMD,stdout=open('./test_3.out','w'),stderr=open('./test_4.out','w'))

# 子进程要执行的代码
def run_java_sock_proc(name):
	print('Run child process %s (%s)...' % (name, os.getpid()))
	server = socket.socket()#声明socket类型，并且生成socket连接对象
	server.bind(('localhost',Java_Sock_Port))#把服务器绑定到localhost的6969端口上
	server.listen(5)#开始监听
	print("等待连接中……")
	django_proc_flag = False
	django_proc = Process(target=run_django_server, args=('test_django',)) 
	while True:
		conn,addr = server.accept()#接收连接
		print("***连接成功***")
		data = bytes.decode(conn.recv(4096)).split() #接收客户发来的数据

		me_flag = data[-1]==data[-2]
		if me_flag and (not django_proc_flag):
			django_proc.start()
			print("Django Server Started")
			django_proc_flag = True

		if (not me_flag) and django_proc_flag:
			django_proc.terminate()
			print("Django Server Stopped")
			django_proc_flag = False

		print("接收到的命令为：",data[-1]==data[-2])
	server.close()

def run_java(name):
    java_proc = subprocess.call(JAVA_CMD,stdout=open('./test_1.out','w'),stderr=open('./test_2.out','w'))


def run_django_sock(name):
	print('Run child process %s (%s)...' % (name, os.getpid()))
	server = socket.socket()#声明socket类型，并且生成socket连接对象
	server.bind(('localhost',Django_Sock_Port))#把服务器绑定到localhost的6969端口上
	server.listen(5)#开始监听
	print("等待连接中……")
	while True:
		conn,addr = server.accept()#接收连接
		print("***连接成功***")
		data = conn.recv(4096) #接收客户发来的数据
		print("接收到的命令为：",data)

	server.close()

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    # s = Process(target=run_django_sock, args=('test_django_sock',)) 
    # s.start()
    # time.sleep(1)
    # p = Process(target=run_java_sock_proc, args=('test_java_sock',))
    # print('Child process will start.')
    # p.start()
    # time.sleep(1)
    # r = Process(target=run_java, args=('test_java',)) 
    # r.start()
    # s.join()
    # r.join()
    # p.join()
    # print('Child process end.')
    s = Process(target=run_django_sock, args=('test_django_sock',)) 
    s.start()
    s.join()

