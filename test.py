import numpy as np

x = np.arange(10)
x2 = np.reshape(x, (2,5))

print(x2)
print(np.roll(x2, (1,2),(0,1)))