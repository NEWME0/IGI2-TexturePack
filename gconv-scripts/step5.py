import os
import subprocess
from settings import (TEXTURES_PACKED_PATH,
					  GCONV_PATH)


exit()


for root, folders, files in os.walk(TEXTURES_PACKED_PATH):
	for filename in files:
		name, ext = os.path.splitext(filename)

		if ext != '.qsc':
			continue

		filepath = os.path.join(root, filename)

		subprocess.call(GCONV_PATH + ' ' + filepath)

