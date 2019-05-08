import numpy as np

wall = np.zeros((10,10),dtype=np.int)
block = np.array([[1,2,3],
                  [1,2,3]])
print(block)
block2=np.array([[4,5,6],
                [4,5,6]])
print(block2)
x = 5
y = 3
d=wall[x:x+block.shape[0], y:y+block.shape[1]]
wall[x:x+block.shape[0], y:y+block.shape[1]] = block
print(wall)
wall[x:x+block.shape[0], y:y+block.shape[1]] =wall[x:x+block.shape[0], y:y+block.shape[1]]+ block2
print(wall)
print(np.zeros([12,12]))