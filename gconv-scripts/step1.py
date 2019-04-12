import os
from settings import (FILELIST_JPG_PATH,
					  FILELIST_RES_PATH,
					  FILELIST_TEX_PATH,
					  FILELIST_TGA_PATH,
					  TEXTURES_VANILLA_PATH)


# check if exist filelists
if not os.path.isfile(FILELIST_JPG_PATH):
	raise Exception("Need filelist to continue: filelist-jpg.txt not found")

if not os.path.isfile(FILELIST_RES_PATH):
	raise Exception("Need filelist to continue: filelist-res.txt not found")

if not os.path.isfile(FILELIST_TEX_PATH):
	raise Exception("Need filelist to continue: filelist-tex.txt not found")

if not os.path.isfile(FILELIST_TGA_PATH):
	raise Exception("Need filelist to continue: filelist-tga.txt not found")


# check if vanila textures are present
def check_filelist(filelist):
	warnings = list()

	with open(filelist, 'r') as filelist:
		for line in filelist:
			if line.endswith('\n'):
				line = line[:-1]

			filepath = os.path.join(TEXTURES_VANILLA_PATH, line)

			if not os.path.isfile(filepath):
				warnings.append("File not fount at {0}".format(filepath))

	return warnings


jpg_warnings = check_filelist(FILELIST_JPG_PATH)
res_warnings = check_filelist(FILELIST_RES_PATH)
tex_warnings = check_filelist(FILELIST_TEX_PATH)
tga_warnings = check_filelist(FILELIST_TGA_PATH)


if jpg_warnings:
	print(*jpg_warnings, sep='\n')

if res_warnings:
	print(*res_warnings, sep='\n')

if tex_warnings:
	print(*tex_warnings, sep='\n')

if tga_warnings:
	print(*tga_warnings, sep='\n')


if jpg_warnings or res_warnings or tex_warnings or tga_warnings:
	raise Exception("textures-vanilla corupted")