import DataBaseAPI
import socket
import json
from copy import deepcopy

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
	def __init__(self,DockerFileName,DockerBuildPath,Port,job_type,job_state):
		self.DockerFileName = DockerFileName
		self.DockerBuildPath = DockerBuildPath
		self.Port = Port
		self.job_type = job_type
		self.job_state = job_state
		self.task_id = 0

	def set_TaskId(self,task_id):
		self.task_id = task_id

	def get_TaskId(self):
		return self.task_id

	def get_DockerFileName(self):
		return self.DockerFileName

	def get_DockerBuildPath(self):
		return self.DockerBuildPath

	def get_Port(self):
		return self.Port

	def get_job_type(self):
		return self.job_type

	def get_job_state(self):
		return self.job_state


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
		self.TaskParamTable = "TestTaskParamTable"
		self.LockTable = "TestLockTable"

	def query_lock(self):
		return self.clusterDataBase.query_all(self.LockTable,self.DataBase)

	def insert_lock(self):
		data = {}
		data['locked'] = "yes"
		self.clusterDataBase.insert_one(data,self.LockTable,self.DataBase)

	def Parse_Lock_db_obj(self,lock_db):
		ret = []
		for l in lock_db:
			ret.append(l)
		if len(ret)==0:
			return None
		return ret

	def get_lock(self):
		lock_db = self.query_lock()
		lock = self.Parse_Lock_db_obj(lock_db)
		if lock==None:
			self.insert_lock()
			return True
		else:
			return False

	def release_lock(self):
		return self.clusterDataBase.delete_all(self.LockTable,self.DataBase)

	def query_spec_task_param(self,spec):
		return self.clusterDataBase.query_spec(spec,self.TaskParamTable,self.DataBase)

	def insert_one_task_param(self,data):
		self.clusterDataBase.insert_one(data,self.TaskParamTable,self.DataBase)

	def update_one_task_param(self,query,value):
		return self.clusterDataBase.update_one(query,value,self.TaskParamTable,self.DataBase)

	def exist_task_param(self,task_name):
		spec = {"task_name":task_name}
		obj = self.query_spec_task_param(spec)
		ret = []
		for o in obj:
			ret.append(o)
		return not len(ret)==0

	def UpdateTaskParam(self,task_name,param):
		if self.exist_task_param(task_name):
			query = {'task_name':task_name}
			value =  {
			 	"$set": {
					"param" : param
			 	}
			}
			self.update_one_task_param(query,value)
		else:
			data = {}
			data['task_name'] = task_name
			data['param'] = param
			self.insert_one_task_param(data)

	def query_spec_task_param(self,spec):
		return self.clusterDataBase.query_spec(spec,self.TaskParamTable,self.DataBase)


	def getTaskParam(self,task_name):
		spec = {"task_name":task_name}
		obj = self.query_spec_task_param(spec)
		ret = []
		for o in obj:
			ret.append(o)
		return ret



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
					tj = Job(machine_job['DockerFileName'],machine_job['DockerBuildPath'],machine_job['Port'],machine_job['job_type'],machine_job['job_state'])
					tm = Machine(m,machine_type,tj)
					machine_list_obj.append(tm)
			t = Task(name,machine_list_obj)
			Task_List.append(t)
		return Task_List

	def insert_one_machine(self,data):
		self.clusterDataBase.insert_one(data,self.MachineTable,self.DataBase)

	def Init(self,machine_list):
		for m in machine_list:
			spec = {'ip_address':m['ip_address']}
			machine_db_obj = self.query_spec_machine(spec)
			machine_obj = self.ParseDbObj(machine_db_obj)
			if machine_obj==None:
				m['job'] = "none"
				self.insert_one_machine(m)

	def ParseJob(self,job_obj):
		ret = {
				"DockerFileName":job_obj.get_DockerFileName(),
				"DockerBuildPath":job_obj.get_DockerBuildPath(),
				"job_type":job_obj.get_job_type(),
				"Port":job_obj.get_Port(),
				"job_state":job_obj.get_job_state(),
				"task_id":job_obj.get_TaskId()
			}
		return ret

	def AddMachines(self,machine_list):
		for m in machine_list:
			data = {}
			data['ip_address'] = m.get_ip_address()
			data['type'] = m.get_machine_type()
			job_obj = m.get_job()
			data['job'] = self.ParseJob(job_obj)
			self.insert_one_machine(data)

	def update_one_machine(self,query,value):
		return self.clusterDataBase.update_one(query,value,self.MachineTable,self.DataBase)

	def get_running_job(self,job_db):
		job_db = deepcopy(job_db)
		job_db['job_state'] = "running"
		ret = {
		 	"$set": {
				"job" : job_db
		 	}
		}
		return ret

	def get_finished_job(self,job_db):
		job_db = deepcopy(job_db)
		job_db['job_state'] = "finished"
		ret = {
		 	"$set": {
				"job" : job_db
		 	}
		}
		return ret

	def AssignWork(self,machine,task_name):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((machine.get_ip_address(), 8003))
		query = {'ip_address':machine.get_ip_address()}
		job = machine.get_job()
		job_db = self.ParseJob(job)
		value =  {
		 	"$set": {
				"job" : job_db
		 	}
		}
		self.update_one_machine(query,value)
		trans_data = deepcopy(job_db)
		trans_data['message_type'] = "addJob"
		trans_data['query'] = query
		print(job_db)
		trans_data['running_value'] = self.get_running_job(job_db)
		print(job_db)
		trans_data['finished_value'] = self.get_finished_job(job_db)
		print(job_db)
		trans_data['task_name'] = task_name
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
		task_name = task.get_name()
		for m in task.get_machineList():
			if not self.AssignWork(m,task_name):
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

		for machine in task.get_machineList():
			query = {'ip_address':machine.get_ip_address()}
			job = machine.get_job()
			job_db = self.ParseJob(job)
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

		json_data = json.dumps(data)
		s.send(bytes(json_data,encoding="utf8"))
		recv_data = s.recv(4096)
		s.close()

		recv_data = recv_data.decode()

		if recv_data=="yes":
			return True
		else:
			return False

	def is_machine_busy_with_ip_address(self,ip_address):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((ip_address, 8003))

		data = {}
		data['message_type'] = 'busy'

		json_data = json.dumps(data)
		s.send(bytes(json_data,encoding="utf8"))
		recv_data = s.recv(4096)
		s.close()

		recv_data = recv_data.decode()

		if recv_data=="yes":
			return True
		else:
			return False

	def get_AviableMachines(self):
		machine_list = self.get_Machines()
		ret = []
		for m in machine_list:
			if not self.is_machine_busy_with_ip_address(m):
				ret.append(m)
		return ret

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
		return machines[0]['machine_list']

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

