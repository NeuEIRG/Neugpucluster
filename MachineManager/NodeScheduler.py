from multiprocessing import Process
import subprocess
import socket
import os
import time
import ClusterStateMonitor
import TaskAdder
import cluster_settings
import ClusterAPI

def StartClusterMonitor(DockerFileName,DockerBuildPath,Port):
	ClusterStateMonitor.run_cluster_monitor(DockerFileName,DockerBuildPath,Port)

def StartTaskAdder():
	TaskAdder.run_task_adder()

if __name__=='__main__':
    DockerFileName = 'Django'
    DockerBuildPath = '../Web'
    Port = '8000'
    connect_url = ["localhost:27017"]
    cluster = ClusterAPI.Cluster(connect_url)
    cluster.Init(cluster_settings.machine_list)
    cluster_state_monitor = Process(target=StartClusterMonitor,args=(DockerFileName,DockerBuildPath,Port,)) 
    cluster_state_monitor.start()
    task_adder = Process(target=StartTaskAdder)
    task_adder.start()
    cluster_state_monitor.join()
    task_adder.join()


    