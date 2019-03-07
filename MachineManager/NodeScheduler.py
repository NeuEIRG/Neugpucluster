from multiprocessing import Process
import subprocess
import socket
import os
import time
import NodeAPIServer
import TaskMonitor
import TaskAdder


def StartAPIServer():
	NodeAPIServer.run_API_Server()

def StartTaskMonitor():
	TaskMonitor.run_task_monitor()

def StartTaskAdder():
	TaskAdder.run_task_adder()

if __name__=='__main__':
    api_server = Process(target=StartAPIServer, args=('api_server',)) 
    api_server.start()
    time.sleep(2)

    task_monitor_process = None
    task_adder_process = None

    while True:
    	me_flag = NodeAPIServer.get_Me_Flag()
    	if me_flag and (task_monitor_process==None):
    		task_monitor_process = Process(target=StartTaskMonitor, args=('task_monitor',))

    	if (not me_flag) and (not (task_monitor_process==None)):
    		task_monitor_process.terminate()
    		task_monitor_process = None

    	if me_flag and (task_adder_process==None):
    		task_adder_process = Process(target=StartTaskAdder, args=('task_adder',))

    	if (not me_flag) and (not (task_adder_process==None)):
    		task_adder_process.terminate()
    		task_adder_process = None

    	time.sleep(1)

    api_server.join()
    if not (task_monitor_process==None):
    	task_monitor_process.join()

    if not (task_adder_process==None):
    	task_adder_process.join()
	
