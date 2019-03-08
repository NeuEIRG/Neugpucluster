import socket
import os
import time
import NodeAPIServer

def run_task_monitor():
	while True:
		TaskError = {}
		cur_tasks = NodeAPIServer.get_Tasks()
		cur_machines = NodeAPIServer.get_Machines()
		print(cur_machines)
		# for task in cur_tasks:
		# 	task_name = task.get_name()
		# 	task_machineList = task.get_machineList()
		# 	TaskError[task_name] = {}
		# 	new_machine_list = []
		# 	error_machine_list = []
		# 	for m in task_machineList:
		# 		error = True
		# 		for machine in cur_machines:
		# 			if m==machine:
		# 				error = False
		# 		if not error:
		# 			new_machine_list.append(m)
		# 		else:
		# 			error_machine_list.append(m)
		# 	TaskError[task_name]['object'] = task
		# 	TaskError[task_name]['new_machine_list'] = new_machine_list
		# 	TaskError[task_name]['error_machine_list'] = error_machine_list

		# for key,value in TaskError.items():
		# 	error_machine_list = value['error_machine_list']
		# 	new_machine_list = value['new_machine_list']
		# 	for m in error_machine_list:
		# 		for machine in cur_machines:
		# 			t = m.get_machine_type()
		# 			if t==machine.get_machine_type() and (machine not in new_machine_list):
		# 				if(not NodeAPIServer.is_machine_busy(machine)):
		# 					machine.set_job(m.get_job())
		# 					new_machine_list.append(machine)
		# 					NodeAPIServer.AssignWork(value['object'],machine)
		# 	task.set_machine_list(new_machine_list)
		# 	if len(error_machine_type_list)>0:
		# 		NodeAPIServer.Update_TaskInfo(value['object'])

		time.sleep(1)






