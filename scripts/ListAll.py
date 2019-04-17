import os
from settings import (TEXTURES_UNPACKED_PATH)


dataset = set()


for root, dirs, files in os.walk(TEXTURES_UNPACKED_PATH):
	for fname in files:
		dataset.add(fname)



dataset = list(dataset)
dataset.sort()



for i in dataset:
	print(i)

print('\n' + str(len(dataset)))
