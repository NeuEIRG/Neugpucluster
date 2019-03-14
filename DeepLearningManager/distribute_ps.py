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

	job_name = "ps"
	task_index = sys.argv[2]

	print(task_name)
	print(param)

	# ps_spec = param['ps_spec']
	# worker_spec = param['worker_spec']


	# num_workers = len(worker_spec)
	# cluster = tf.train.ClusterSpec({"ps":ps_spec,"worker":worker_spec})
	# server = tf.train.Server(cluster,job_name=job_name,task_index=task_index)
	# server.join()