import json
import tensorflow as tf
import numpy as np
import time
import os
import sys
import random
import pickle
import tempfile 

sys.path.append("../MachineManager")

import ClusterAPI
import cluster_settings

if __name__ == '__main__':

	task_name = sys.argv[1]

	# connect_url = ["localhost:27017"]
	connect_url = cluster_settings.connect_url
	cluster = ClusterAPI.Cluster(connect_url)
	param = cluster.getTaskParam(task_name)
	param = param[0]['param']

	job_name = "ps"
	task_index = int(sys.argv[2])

	# print(task_name)
	# print(param)

	ps_spec = param[u'ps_spec']
	worker_spec = param[u'worker_spec']
	port = param[u'port']


	for i in range(len(ps_spec)):
		ps_spec[i] = ps_spec[i] + ":" + port

	for i in range(len(worker_spec)):
		worker_spec[i] = worker_spec[i] + ":" + port


	num_workers = len(worker_spec)
	cluster = tf.train.ClusterSpec({"ps":ps_spec,"worker":worker_spec})
	server = tf.train.Server(cluster,job_name=job_name,task_index=task_index)
	server.join()