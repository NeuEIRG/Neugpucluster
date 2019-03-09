from multiprocessing import Process
import multiprocessing
import subprocess
import socket
import os
import time
import json
# import NodeAPIServer

Share_Flag = multiprocessing.Value("b",1)

def run_docker_proc(DockerFileName,DockerBuildPath,Port,job_type):
	if job_type=="noshare":
		Share_Flag = 0 
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
	if job_type=="noshare":
		Share_Flag = 1

def check_busy(json_data,process_list):
	job_type = json_data['job_type']
	if (not Share_Flag) or (len(process_list)>0 and job_type=="noshare"):
		return True
	else:
		return False

def run_task_adder():
	Task_Port = 8003
	server = socket.socket()
	server.bind(('localhost',Task_Port))
	server.listen(5)
	process_list = []
	while True:
		conn,addr = server.accept()
		recv_data = bytes.decode(conn.recv(4096))
		# print(recv_data)
		tp = []
		for p in process_list:
			if p.is_alive():
				tp.append(p)
		process_list = tp
		json_data = json.loads(recv_data)
		message_type = json_data['message_type']
		if message_type=="addJob":
			busy = check_busy(json_data,process_list)
			if busy:
				conn.send(b"error")
			else:
				conn.send(b"success")
				dockerfile_name = json_data['DockerFileName']
				docker_build_path = json_data['DockerBuildPath']
				port = json_data['Port']
				job_type = json_data['job_type']
				# run_docker_proc(dockerfile_name,docker_build_path,port)
				s = Process(target=run_docker_proc, args=(dockerfile_name,docker_build_path,port,job_type,)) 
				s.start()
				process_list.append(s)
		elif message_type=="busy":
			busy = check_busy(json_data,process_list)
			if busy:
				conn.send(b"yes")
			else:
				conn.send(b"no")

	server.close()