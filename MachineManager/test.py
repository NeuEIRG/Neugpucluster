import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('localhost', 8003))

data = {}
data['DockerFileName'] = 'Django'
data['DockerBuildPath'] = '../Web'
data['Port'] = '8000'

json_data = json.dumps(data)
s.send(bytes(json_data,encoding="utf8"))
s.close()
