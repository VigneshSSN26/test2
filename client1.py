import Pyro4


uri = input("Enter the server URI: ")  
calculator = Pyro4.Proxy(uri)         
a = int(input("Enter first number: "))
b = int(input("Enter second number: "))

print("Addition result:", calculator.add_numbers(a, b))
print("Multiplication result:", calculator.multiply(a, b))
