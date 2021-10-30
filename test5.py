x = 1234
y = bin(x)

print(y)
print("Last two bits: ", y[-2:])
print("Convert back to int: ", int(y))
print(type(y))