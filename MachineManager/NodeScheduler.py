from multiprocessing import Process
import subprocess
import socket
import os
import time
import ClusterStateMonitor
import TaskAdder

def StartClusterMonitor():
	ClusterStateMonitor.run_cluster_monitor()

def StartTaskAdder():
	TaskAdder.run_task_adder()

if __name__=='__main__':
    cluster_state_monitor = Process(target=StartClusterMonitor) 
    cluster_state_monitor.start()
    task_adder = Process(target=StartTaskAdder)
    task_adder.start()
    cluster_state_monitor.join()
    task_adder.join()


    