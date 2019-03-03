import math 
import tempfile 
import time
import tensorflow as tf 
from tensorflow.examples.tutorials.mnist import input_data

data_dir = '/tmp/mnist-data'
hidden_units = 100
train_steps = 1000000
batch_size = 100
learning_rate = 0.01
sync_replicas = False
replicas_to_aggregate = None 
ps_hosts = ["172.28.54.158:2222"]
worker_hosts = ["172.28.54.158:2222"]
job_name = "worker"
task_index = 0 
image_height = 28
image_width = 28

if __name__ == '__main__':
	mnist = input_data.read_data_sets(data_dir,one_hot=True)
	ps_spec = ps_hosts
	worker_spec = worker_hosts
	num_workers = len(worker_spec)
	cluster = tf.train.ClusterSpec({"ps":ps_spec,"worker":worker_spec})
	server = tf.train.Server(cluster,job_name=job_name,task_index=task_index)
	if job_name == "ps":
		server.join()
	is_chief = (task_index==0)
	worker_device = "job:worker/task:%d/gpu:0" % task_index
	with tf.device(tf.train.replica_device_setter(
		worker_device=worker_device,
		ps_device="/job:ps/cpu:0",
		cluster=cluster)):

		global_step = tf.Variable(0,name="global_step",trainable=False)
		hid_w = tf.Variable(tf.truncated_normal([image_height*image_width,hidden_units],
			stddev=1.0/image_height),name="hid_w")		
		hid_b = tf.Variable(tf.zeros([hidden_units]),name="hid_b")
		sm_w = tf.Variable(tf.truncated_normal([hidden_units,10],
			stddev=1.0/math.sqrt(hidden_units)),name="sm_w")
		sm_b = tf.Variable(tf.zeros([10]),name="sm_b")

		x = tf.placeholder(tf.float32,[None,image_width*image_height])
		y_ = tf,placeholder(tf.float32,[None,10])

		hid_lin = tf.nn.xw_plus_b(x,hid_w,hid_b)
		hid = tf.nn.relu(hid_lin)

		y = tf.nn.softmax(tf.nn.xw_plus_b(hid,sm_w,sm_b))
		cross_entropy = -tf.reduce_sum(y_*tf.log(tf.clip_by_value(y,1e-10,1.0)))
		opt = tf.train.AdamOptimizer(learning_rate)

	if sync_replicas:
		if replicas_to_aggregate is None:
			replicas_to_aggregate = num_workers 

		opt = tf.train.SyncReplicasOptimizer(
			opt,
			replicas_to_aggregate=replicas_to_aggregate,
			total_num_replicas=num_workers,
			replica_id=task_index,
			name="mnist_sync_replicas")

	train_step = opt.minimize(cross_entropy,global_step=global_step)

	if sync_replicas and is_chief:
		chief_queue_runner = opt.get_chief_queue_runner()
		init_tokens_op = opt.get_init_tokens_op()

	init_op = tf.global_variables_initializer()
	train_dir = tempfile.mkdtemp()
	sv = tf.train.Supervisor(is_chief=is_chief,
							logdir=train_dir,
							init_op=init_op,
							recovery_wait_secs=1,
							global_step=global_step)
	sess_config = tf.ConfigProto(
							allow_soft_placement=True,
							log_device_placement=False,
							device_filters=["/job:ps",
											"/job:worker/task:%d" % task_index])

	sess = sv.prepare_or_wait_for_session(server.target,config=sess_config)

	if sync_replicas and is_chief:
		sv.start_queue_runners(sess,[chief_queue_runner])
		sess.run(init_tokens_op)

	time_begin = time.time()
	local_step = 0
	while True:
		batch_xs,batch_ys = mnist.train.next_batch(batch_size)
		train_feed = {x:batch_xs,y_:batch_ys}
		_,step = sess.run([train_step,global_step],feed_dict=train_feed)
		local_step += 1

		now = time.time()

		if step>=train_steps:
			break
	time_end = time.time()
	training_time = time_end - time_begin

	val_feed = {x:mnist.vaalidation.images,y_:mnist.validation.labels}
	val_xent = sess.run(cross_entropy,feed_dict=val_feed)
	




