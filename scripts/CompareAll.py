import os
import filecmp
from collections import defaultdict
from settings import TEXTURES_UNPACKED_PATH


groups = defaultdict(list)


for root, dirs, files in os.walk(TEXTURES_UNPACKED_PATH):
	for fname in files:
		groups[fname].append(os.path.join(root, fname))


def itemwise(lst):
	for i in range(len(lst) - 1):
		yield lst[i], lst[i+1]


for fname, pathlist in groups.items():
	if len(pathlist) < 2:
		continue

	result = True

	for fileA, fileB in itemwise(pathlist):
		result = filecmp.cmp(fileA, fileB)

		if not result:
			break

	print('{0:<5} - {1}'.format(str(result), fname))
