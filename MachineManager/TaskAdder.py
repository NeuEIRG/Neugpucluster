from multiprocessing import Process
import subprocess
import socket
import os
import time
import json
# import NodeAPIServer

def run_docker_proc(DockerFileName,DockerBuildPath,Port):
	std_out_file = './'+DockerFileName+'.out'
	std_err_file = './'+DockerFileName+'.err'
	DockerFilePath = '../DockerImages/' + DockerFileName + "Image/" + DockerFileName + "Dockerfile" 
	Docker_Build_Cmd = ['docker','build','-t','dlm/'+DockerFileName.lower(),'-f',DockerFilePath,DockerBuildPath]
	# print(DockerFilePath)
	# print(Docker_Build_Cmd)
	docker_build_proc = subprocess.call(Docker_Build_Cmd,stdout=open(std_out_file,'w'),stderr=open(std_err_file,'w'))
	Docker_Run_Cmd = ['docker','run','-p',Port+":"+Port,'dlm/'+DockerFileName.lower()]
	# print(Docker_Run_Cmd)
	docker_run_proc = subprocess.call(Docker_Run_Cmd,stdout=open(std_out_file,'w'),stderr=open(std_err_file,'w'))



def run_task_adder():
	Task_Port = 8003
	server = socket.socket()
	server.bind(('localhost',Task_Port))
	server.listen(5)
	while True:
		conn,addr = server.accept()
		recv_data = bytes.decode(conn.recv(4096))
		# print(recv_data)
		json_data = json.loads(recv_data)
		dockerfile_name = json_data['DockerFileName']
		docker_build_path = json_data['DockerBuildPath']
		port = json_data['Port']
		run_docker_proc(dockerfile_name,docker_build_path,port)
	server.close()


run_task_adder()