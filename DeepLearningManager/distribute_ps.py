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


if __name__ == '__main__':

	task_name = sys.argv[0]

	connect_url = ["localhost:27017"]
	cluster = ClusterAPI.Cluster(connect_url)
	param = cluster.getTaskParam(task_name)

	job_name = "ps"
	task_index = sys.argv[1]

	ps_spec = param['ps_spec']
	worker_spec = param['worker_spec']

	num_workers = len(worker_spec)
	cluster = tf.train.ClusterSpec({"ps":ps_spec,"worker":worker_spec})
	server = tf.train.Server(cluster,job_name=job_name,task_index=task_index)
	server.join()