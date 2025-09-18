# class DataObject:
#     def __init__(self, name, values):
#         self.name = name
#         self.values = values

# import socket
# import pickle

# def start_server():
#     host = '127.0.0.1'
#     port = 54321

#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind((host, port))
#     server_socket.listen(2)
#     print(f"Server listening on {host}:{port}")

#     conn, addr = server_socket.accept()
#     print(f"Connected by {addr}")

#     data = conn.recv(4096)
#     obj = pickle.loads(data)

#     print(f"Received object: name = {obj.name}, values = {obj.values}")
#     result = sum(obj.values)
#     response = f"Hello {obj.name}, sum is {result}"


#     conn.sendall(pickle.dumps(response))

#     conn.close()
#     server_socket.close()

# if __name__ == "__main__":
#     start_server()





class Object:
    def __init__(self,arr,num):
        self.arr = arr
        self.num = num




import socket
import pickle

host = "127.0.0.1"
port = 1234

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((host,port))
server_socket.listen(2)

conn,addr = server_socket.accept()

data = conn.recv(4096)
obj = pickle.loads(data)
arr = obj.arr
print(arr)
res = sum(arr)
send_data = pickle.dumps(str(res))
conn.sendall(send_data)
conn.close()





