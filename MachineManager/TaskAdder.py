from multiprocessing import Process
import multiprocessing
import subprocess
import socket
import os
import time
import json
import ClusterAPI


def run_docker_proc(json_data):

	connect_url = ["localhost:27017"]
	cluster = ClusterAPI.Cluster(connect_url)

	query = json_data['query']
	running_value = json_data['running_value']
	finished_value = json_data['finished_value']

	cluster.update_one_machine(query,running_value)

	dockerfile_name = json_data['DockerFileName']
	docker_build_path = json_data['DockerBuildPath']
	port = json_data['Port']
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

	cluster.update_one_machine(query,finished_value)

def check_busy(process_list):
	return len(process_list)>0

def run_task_adder(ip_address):
	Task_Port = 8003
	server = socket.socket()
	server.bind((ip_address,Task_Port))
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
			busy = check_busy(process_list)
			if busy:
				conn.send(b"error")
			else:
				conn.send(b"success")
				# run_docker_proc(dockerfile_name,docker_build_path,port)
				# s = Process(target=run_docker_proc, args=(json_data,)) 
				# s.start()
				# process_list.append(s)
				print(json_data)
		elif message_type=="busy":
			busy = check_busy(process_list)
			if busy:
				conn.send(b"yes")
			else:
				conn.send(b"no")

	server.close()