import DataBaseAPI
import socket
import json

# def run_task_monitor(cur_machines):
# 	TaskError = {}
# 	cur_tasks = NodeAPI.get_Tasks()
# 	print(cur_machines)
# 	for task in cur_tasks:
# 		task_name = task.get_name()
# 		task_machineList = task.get_machineList()
# 		TaskError[task_name] = {}
# 		new_machine_list = []
# 		error_machine_list = []
# 		for m in task_machineList:
# 			error = True
# 			for machine in cur_machines:
# 				if m==machine:
# 					error = False
# 			if not error:
# 				new_machine_list.append(m)
# 			else:
# 				error_machine_list.append(m)
# 		TaskError[task_name]['object'] = task
# 		TaskError[task_name]['new_machine_list'] = new_machine_list
# 		TaskError[task_name]['error_machine_list'] = error_machine_list

# 	for key,value in TaskError.items():
# 		error_machine_list = value['error_machine_list']
# 		new_machine_list = value['new_machine_list']
# 		for m in error_machine_list:
# 			for machine in cur_machines:
# 				t = m.get_machine_type()
# 				if t==machine.get_machine_type() and (machine not in new_machine_list):
# 					if(not NodeAPI.is_machine_busy(machine)):
# 						machine.set_job(m.get_job())
# 						new_machine_list.append(machine)
# 						NodeAPI.AssignWork(value['object'],machine)
# 		task.set_machine_list(new_machine_list)
# 		if len(error_machine_type_list)>0:
# 			NodeAPI.Update_TaskInfo(value['object'])

class Job:
	def __init__(self,DockerFileName,DockerBuildPath,Port,job_type):
		self.DockerFileName = DockerFileName
		self.DockerBuildPath = DockerBuildPath
		self.Port = Port
		self.job_type = job_type

	def get_DockerFileName(self):
		return self.DockerFileName

	def get_DockerBuildPath(self):
		return self.DockerBuildPath

	def get_Port(self):
		return self.Port

	def get_job_type(self):
		return self.job_type


class Machine:
	def __init__(self,ip_address,machine_type,job):
		self.ip_address = ip_address
		self.type = machine_type
		self.job = job

	def get_ip_address(self):
		return self.ip_address

	def get_machine_type(self):
		return self.type

	def get_job(self):
		return self.job

	def set_job(self,job):
		self.job = job

class Task:
	def __init__(self,name,machineList):
		self.name = name
		self.machineList = machineList

	def get_name(self):
		return self.name

	def get_machineList(self):
		return self.machineList

	def set_machine_list(self,machine_list):
		self.machine_list = machine_list

class Cluster:
	def __init__(self,connect_url):
		self.clusterDataBase = DataBaseAPI.ClusterDataBase(connect_url)
		self.TaskTable = "TestTaskTable"
		self.MachineTable = "TestMachineTable"
		self.ClusterTable = "TestStateTable"
		self.DataBase = "TestDlpDataBase"


	def query_all_tasks(self):
		return self.clusterDataBase.query_all(self.TaskTable,self.DataBase)

	def query_spec_machine(self,spec):
		machine_db_obj = self.clusterDataBase.query_spec(spec,self.MachineTable,self.DataBase)
		return machine_db_obj

	def ParseDbObj(self,obj):
		ans = []
		for o in obj:
			ans.append(o)
		if len(ans)>0:
			return ans[0]
		else:
			return None

	def get_Tasks(self):
		task_db_obj = self.query_all_tasks()
		Task_List = []
		for item in task_db_obj:
			machine_list = item['machine_list']
			name = item['name']
			machine_list_obj = []
			for m in machine_list:
				machine_db_obj = self.query_spec_machine({'ip_address':m})
				machine_obj = self.ParseDbObj(machine_db_obj)
				if not machine_obj==None:
					machine_type = machine_obj['type']
					machine_job = machine_obj['job']
					tj = Job(machine_job['DockerFileName'],machine_job['DockerBuildPath'],machine_job['Port'],machine_job['job_type'])
					tm = Machine(m,machine_type,tj)
					machine_list_obj.append(tm)
			t = Task(name,machine_list_obj)
			Task_List.append(t)
		return Task_List

	def insert_one_machine(self,data):
		self.clusterDataBase.insert_one(data,self.MachineTable,self.DataBase)

	def AddMachines(self,machine_list):
		for m in machine_list:
			data = {}
			data['ip_address'] = m.get_ip_address()
			data['type'] = m.get_machine_type()
			job_obj = m.get_job()
			data['job'] = {
				"DockerFileName":job_obj.get_DockerFileName(),
				"DockerBuildPath":job_obj.get_DockerBuildPath(),
				"job_type":job_obj.get_job_type(),
				"Port":job_obj.get_Port()
			}
			self.insert_one_machine(data)

	def update_one_machine(self,query,value):
		return self.clusterDataBase.update_one(query,value,self.MachineTable,self.DataBase)

	def AssignWork(self,machine):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((machine.get_ip_address(), 8003))
		query = {'ip_address':machine.get_ip_address()}
		job = machine.get_job()
		job_db = {}
		job_db['DockerFileName'] = job.get_DockerFileName()
		job_db['DockerBuildPath'] = job.get_DockerBuildPath()
		job_db['Port'] = job.get_Port()
		job_db['job_type'] = job.get_job_type()
		value =  {
		 	"$set": {
				"job" : job_db
		 	}
		}
		self.update_one_machine(query,value)
		trans_data = job_db
		trans_data['message_type'] = "addJob"
		json_data = json.dumps(trans_data)
		s.send(bytes(json_data,encoding="utf8"))
		recv_data = s.recv(4096)
		s.close()

		recv_data = recv_data.decode()

		if recv_data=="error":
			return False
		else:
			return True

	def AssignTask(self,task):
		error_list = []
		for m in task.get_machineList():
			if not self.AssignWork(m):
				error_list.append(m)
		return error_list

	def insert_one_task(self,task):
		self.clusterDataBase.insert_one(task,self.TaskTable,self.DataBase)

	def AddTask(self,task):
		task_db = {}
		task_db['machine_list'] = []
		for m in task.get_machineList():
			task_db['machine_list'].append(m.get_ip_address())	
		task_db['name'] = task.get_name()
		self.insert_one_task(task_db)

		for m in task.get_machineList():
			query = {'ip_address':machine.get_ip_address()}
			job = machine.get_job()
			job_db = {}
			job_db['DockerFileName'] = job.get_DockerFileName()
			job_db['DockerBuildPath'] = job.get_DockerBuildPath()
			job_db['Port'] = job.get_Port()
			job_db['job_type'] = job.get_job_type()
			value =  {
			 	"$set": {
					"job" : job_db
			 	}
			}
			self.update_one_machine(query,value)



	def update_one_task(self,query,value):
		self.clusterDataBase.update_one(query,value,self.TaskTable,self.DataBase)

	def Update_TaskInfo(self,task):
		query = {"name":task.get_name()}
		machine_list = []
		for m in task.get_machineList():
			machine_list.append(m.get_ip_address())
		value =  {
		 	"$set": {
				"machine_list" : machine_list
		 	}
		}
		self.update_one_task(query,value)

	def is_machine_busy(self,machine):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((machine.get_ip_address(), 8003))

		data = {}
		data['message_type'] = 'busy'
		data['job_type'] = machine.get_job().get_job_type()

		json_data = json.dumps(data)
		s.send(bytes(json_data,encoding="utf8"))
		recv_data = s.recv(4096)
		s.close()

		recv_data = recv_data.decode()

		if recv_data=="yes":
			return True
		else:
			return False

	def query_all_cluster(self):
		return self.clusterDataBase.query_all(self.ClusterTable,self.DataBase)

	def delete_all_cluster(self):
		return self.clusterDataBase.delete_all(self.ClusterTable,self.DataBase)

	def insert_one_cluster(self,data):
		self.clusterDataBase.insert_one(data,self.ClusterTable,self.DataBase)

	def get_Machines(self):
		machines_db = self.query_all_cluster()
		machines = []
		for m in machines_db:
			machines.append(m)
		return machines

	def Update_ClusterInfo(self,machine_list):
		print(machine_list)
		self.delete_all_cluster()
		data = {}
		data['machine_list'] = machine_list
		self.insert_one_cluster(data)


	def get_Task_Error_Machines(task):
		cur_machines = get_Machines()
		task_machineList = task.get_machineList()
		TaskError[task_name] = {}
		new_machine_list = []
		error_machine_list = []
		for m in task_machineList:
			error = True
			for machine in cur_machines:
				if m==machine:
					error = False
			if error:
				error_machine_list.append(m)

		return error_machine_list



	
# connect_url = ["localhost:27017"]
# cluster1 = Cluster(connect_url)
# cluster2 = Cluster(connect_url)
# DockerFileName = 'Django'
# DockerBuildPath = '../Web'
# Port = '8000'
# job_type = "share"
# job = Job(DockerFileName,DockerBuildPath,Port,job_type)
# machine = Machine("localhost","cpu",job)
# cluster.AddMachines([machine])
# task = Task("test_task1",[machine])
# cluster.AddTask(task)
# cluster.Update_TaskInfo(task)
# machine_list = ["localhost"]
# cluster.Update_ClusterInfo(machine_list)
# print(cluster.get_Machines())
# # task_obj = cluster.query_all_tasks()
# # for t in task_obj:
# # 	print(t)
# print(cluster.get_Tasks())

# cluster.AssignWork(machine)
# error_list = cluster.AssignTask(task)
# print(error_list)
# print(cluster.is_machine_busy(machine))

