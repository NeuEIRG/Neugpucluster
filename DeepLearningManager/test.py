# import json
# import sys
# import socket 
# import time

# sys.path.append("../MachineManager")

# import ClusterAPI

# task_name = "testTask"
# batch_size = 200
# learning_rate = 0.01
# dataset_url = "http://localhost"
# with open('./test.json',"r") as json_file:
# 	json_obj = json.load(json_file)
# network = json.dumps(json_obj)

# param = {}
# param['batch_size'] = batch_size
# param['learning_rate'] = learning_rate
# param['dataset_url'] = dataset_url
# param['network'] = network

# connect_url = ["localhost:27017"]
# cluster = ClusterAPI.Cluster(connect_url)
# cluster.UpdateTaskParam(task_name,param)
# print(cluster.getTaskParam(task_name))


#!/usr/bin/env python
# -*- coding: utf-8 -*-

