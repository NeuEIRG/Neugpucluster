import json
import sys
sys.path.append("..")
import MachineManager.ClusterAPI

ClusterAPI = MachineManager.ClusterAPI

task_name = "testTask"
batch_size = 200
learning_rate = 0.01
dataset_url = "http://localhost"
with open(json_file_url,"r") as json_file:
	json_obj = json.load(json_file)
network = json.dump(json_obj)

param = {}
param['batch_size'] = batch_size
param['learning_rate'] = learning_rate
param['dataset_url'] = dataset_url
param['network'] = network

connect_url = ["localhost:27017"]
cluster = Cluster(connect_url)
cluster.UpdateTaskParam(task_name,param)