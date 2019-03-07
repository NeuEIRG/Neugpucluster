import ClusterStateMonitor

class MachineState:
	free = 0
	busy = 1

class Job:
	def __init__(self,docker_param):
		self.docker_param = docker_param

class Machine:
	def __init__(self,ip_address,machine_type,state,job):
		self.ip_address = ip_address
		self.type = machine_type
		self.state = state
		self.job = job

	def get_ip_address():
		return self.ip_address

	def get_machine_type():
		return self.machine_type

	def get_machine_state():
		return self.state

	def get_job():
		return self.job

	def set_job(job):
		self.job = job

class Task:
	def __init__(self,name,machineList):
		self.name = name
		self.machineList = machineList

	def get_name():
		return self.name

	def get_machineList():
		return machineList

	def set_machine_list(machine_list):
		self.machine_list = machine_list

def get_Me_Flag():
	return ClusterStateMonitor.get_Me_Flag()

def get_Cur_State():
	return ClusterStateMonitor.get_Cur_State()

def run_API_Server():
	ClusterStateMonitor.run_cluster_monitor()


def get_Tasks():
	pass

def get_Machines():
	pass

def AssignWork(task,machine):
	pass

def Update_TaskInfo(task):
	pass

def is_machine_busy(machine):
	pass