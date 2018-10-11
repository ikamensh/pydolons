import socket, pickle
import sys

class ProcessData:
    process_id = 0
    project_id = 0
    task_id = 0
    start_time = 0
    end_time = 0
    user_id = 0
    weekend_id = 0


HOST = 'localhost'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)

data = conn.recv(4096)
print("bytes actually recieved: ", sys.getsizeof(data))
data_variable = pickle.loads(data)
conn.close()
print (data_variable)
# Access the information by doing data_variable.process_id or data_variable.task_id etc..,
print ('Data received from client')