import os
import subprocess
from settings import (FILELIST_RES_PATH,
					  TEXTURES_UNPACKED_PATH,
					  GCONV_PATH,
					  QSCRIPT_PATH,
					  BAT_PATH)


# check if exist game converter
if not os.path.isfile(GCONV_PATH):
	raise Exception("Game converter not fond at {0}".format(GCONV_PATH))


with open(QSCRIPT_PATH, 'w') as qscript:
	with open(FILELIST_RES_PATH, 'r') as filelist:
		for line in filelist:
			if line.endswith('\n'):
				line = line[:-1]

			qscript.write("ExtractResource(\"{0}\");\n".format(line))



#-InputPath=export/ -OutputPath=output/

INPUT_PATH = "-OutputPath=" + '..\\' + TEXTURES_UNPACKED_PATH


ARGS = GCONV_PATH + ' ' + QSCRIPT_PATH + ' ' + INPUT_PATH
ARGS = ARGS.replace('\\', '/')
print(ARGS)

with open(BAT_PATH, 'w') as bat:
	bat.write(ARGS + '\n')
	bat.write("pause\n")

subprocess.call(ARGS)
