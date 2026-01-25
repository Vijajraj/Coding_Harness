def add(a,b):
    return a + b
def subtract(a,b):
    return a - b
def multiply(a,b):
    return a*b
def divide(a,b):
    return a / b
a = float(input("enter the number:"))
b = float(input("enter the number:"))
print("add:", add(a,b))
print("sub:", subtract(a,b))
print("multiply:",multiply(a,b))
print("divide:", divide(a,b))
if b != 0:
    print("divide:", divide(a,b))
else:
    print("you cannot divide by zero")