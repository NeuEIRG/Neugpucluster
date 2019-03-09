import pymongo

class ClusterDataBase:
	def __init__(self,ip_list):
		self.client = self.connect_DataBase(ip_list)

	def connect_DataBase(self,ip_list):
		connect_url = "mongodb://"
		for i in range(len(ip_list)):
			connect_url = connect_url + ip_list[i]
			if not i==(len(ip_list)-1):
				connect_url = connect_url + ','

		client = pymongo.MongoClient(connect_url)
		return client

	def get_Database(self,db_name):
		db = self.client[db_name]
		return db

	def get_Table(self,db,table_name):
		return db[table_name]

	def insert_one(self,data,table_name,db_name):
		db = self.get_Database(db_name)
		table = self.get_Table(db,table_name)
		table.insert_one(data)

	def insert_many(self,data,table_name,db_name):	
		db = self.get_Database(db_name)
		table = self.get_Table(db,table_name)
		table.insert_many(data)

	def query_all(self,table_name,db_name):
		db = self.get_Database(db_name)
		table = self.get_Table(db,table_name)
		return table.find()

	def query_spec(self,spec,table_name,db_name):
		db = self.get_Database(db_name)
		table = self.get_Table(db,table_name)
		return table.find(spec)

	def update_one(self,query,value,table_name,db_name):
		db = self.get_Database(db_name)
		table = self.get_Table(db,table_name) 
		table.update_one(query,value)

	def delete_all(self,table_name,db_name):
		db = self.get_Database(db_name)
		table = self.get_Table(db,table_name) 
		table.delete_many({})

# connect_url = ["localhost:27017"]
# ClusterDataBase = ClusterDataBase(connect_url)
# data = {
# 	"machine_list" : ["localhost:8005","localhost:8003"],
# 	"name" : "test_3"
# }
# db_name = "TestDlpDataBase"
# table_name = "TestTaskTable"
# ClusterDataBase.insert_one(data,table_name,db_name)
# spec = {"name":"test_3"}
# items = ClusterDataBase.query_sepc(spec,table_name,db_name)
# print(items[0])
# for it in items:
# 	print(it['machine_list'])

# query = {"name":"test_3"}
# value =  {
#  	"$set": {
# 		"machine_list" : ["localhost"]
#  	}
# }
# ClusterDataBase.update_one(query,value,table_name,db_name)

# spec = {"name":"test_3"}
# items = ClusterDataBase.query_sepc(spec,table_name,db_name)
# for it in items:
# 	print(it['machine_list'])