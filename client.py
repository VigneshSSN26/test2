# class DataObject:
#     def __init__(self, name, values):
#         self.name = name
#         self.values = values

# import socket
# import pickle

# def start_client():
#     host = '127.0.0.1'
#     port = 54321

#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect((host, port))

#     name = input("Enter your name: ")
#     numbers = [1,2,3,4,5]

#     obj = DataObject(name, numbers)
#     data = pickle.dumps(obj)
#     client_socket.sendall(data)

#     response = pickle.loads(client_socket.recv(4096))
#     print(f"Response from server: {response}")

#     client_socket.close()

# if __name__ == "__main__":
#     start_client()
















import socket
import pickle

class Object:
    def __init__(self,arr,num):
        self.arr = arr
        self.num = num
    
host = "127.0.0.1" 
port = 1234

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((host,port))

obj = Object([1,2,3,4],4)
ser_obj = pickle.dumps(obj)

client_socket.sendall(ser_obj)
ans = client_socket.recv(4096)
ans = pickle.loads(ans)
print(ans)
client_socket.close()





