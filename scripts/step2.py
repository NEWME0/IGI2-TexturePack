import shutil
from settings import (TEXTURES_VANILLA_PATH,
					  TEXTURES_UNPACKED_PATH)


# copy textures-vanilla to textures-unpacked
shutil.copytree(TEXTURES_VANILLA_PATH, TEXTURES_UNPACKED_PATH)
