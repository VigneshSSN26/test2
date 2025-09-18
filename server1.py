import Pyro4

@Pyro4.expose   
class Calculator:
    def add_numbers(self, a, b):
        return a + b

    def multiply(self, a, b):
        return a * b



daemon = Pyro4.Daemon()           # start a Pyro daemon
uri = daemon.register(Calculator) # register Calculator class as a Pyro object
print("Server is ready. URI:", uri)
daemon.requestLoop()              # keep server running, waiting for clients


