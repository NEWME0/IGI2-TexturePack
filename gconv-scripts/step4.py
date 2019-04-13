import shutil
from settings import (TEXTURES_UNPACKED_PATH,
					  TEXTURES_PACKED_PATH)


# copy textures-vanilla to textures-unpacked
shutil.copytree(TEXTURES_UNPACKED_PATH, TEXTURES_PACKED_PATH)