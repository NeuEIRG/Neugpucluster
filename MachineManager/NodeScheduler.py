from multiprocessing import Process
import subprocess
import socket
import os
import time
import ClusterStateMonitor
import TaskAdder
import cluster_settings
import ClusterAPI

def StartClusterMonitor(DockerFileName,DockerBuildPath,Port,ip_address):
	ClusterStateMonitor.run_cluster_monitor(DockerFileName,DockerBuildPath,Port,ip_address)

def StartTaskAdder(ip_address):
	TaskAdder.run_task_adder(ip_address)

if __name__=='__main__':
    DockerFileName = 'Django'
    DockerBuildPath = '../Web'
    Port = '8000'
    connect_url = ["localhost:27017"]
    ip_address = "172.28.54.158"
    cluster = ClusterAPI.Cluster(connect_url)
    cluster.Init(cluster_settings.machine_list)
    cluster_state_monitor = Process(target=StartClusterMonitor,args=(DockerFileName,DockerBuildPath,Port,ip_address,)) 
    cluster_state_monitor.start()
    task_adder = Process(target=StartTaskAdder,args=(ip_address,))
    task_adder.start()
    cluster_state_monitor.join()
    task_adder.join()


    