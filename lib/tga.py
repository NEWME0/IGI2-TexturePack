import numpy as np
from struct import unpack


TGA_PMAP_TYPE_NONE = 0
TGA_PMAP_TYPE_CMAP = 1
TGA_PMAP_TYPE_TRUE = 2
TGA_PMAP_TYPE_MONO = 3
TGA_PMAP_TYPE_CMAP_RLE = 9
TGA_PMAP_TYPE_TRUE_RLE = 10
TGA_PMAP_TYPE_MONO_RLE = 11

TGA_CMAP_TYPE_NONE = 0
TGA_CMAP_TYPE_HAS = 1

TGA_SIGNATURE = b'TRUEVISION-XFILE.\x00'


DTYPE_TGA_HEADER = np.dtype([
	('imid_size',        np.uint8),
	('cmap_type',        np.uint8),
	('pmap_type',        np.uint8),
	('cmap_entry_first', np.uint16),
	('cmap_entry_count', np.uint16),
	('cmap_entry_width', np.uint8),
	('pmap_origin_x',    np.uint16),
	('pmap_origin_y',    np.uint16),
	('pmap_size_x',      np.uint16),
	('pmap_size_y',      np.uint16),
	('pmap_depth',       np.uint8),
	('pmap_flags',       np.uint8),
	])


DTYPE_TGA_FOOTER = np.dtype([
	('ext_offset', np.uint32),
	('def_offset', np.uint32),
	('signature',  (np.uint8, 18)),
	])


class TGAObject:
	head = None
	imid = None
	cmap = None
	pmap = None
	foot = None

	def free(self):
		head = None
		imid = None
		cmap = None
		pmap = None
		foot = None

	def load(self, path):
		self.free()

		with open(path, 'rb') as f:
			self.head = np.frombuffer(f.read(18), DTYPE_TGA_HEADER)

			assert self.head['imid_size'] == 0,         "Tga id are unsuported"
			assert self.head['cmap_type'] == 0,         "Tga color map are unsuported"
			assert self.head['pmap_type'] == 2,         "Only TrueColor(2) are suported"
			assert self.head['pmap_depth'] in (16, 32), "Only pixel depth 16 and 32 are suported"

			x = int(self.head['pmap_size_x'][0])
			y = int(self.head['pmap_size_y'][0])
			d = int(self.head['pmap_depth'][0]) // 8

			if self.head['pmap_depth'] == 16:
				dtype = np.uint16
			elif self.head['pmap_depth'] == 32:
				dtype = np.uint32

			self.pmap = np.frombuffer(f.read(x * y * d), dtype)

			self.pmap = self.pmap.reshape((self.head['pmap_size_x'][0], self.head['pmap_size_y'][0]))

			self.foot = np.frombuffer(f.read(26), DTYPE_TGA_FOOTER)

	def save(self, path):
		with open(path, 'wb') as f:
			f.write(self.head.tobytes())
			f.write(self.pmap.tobytes())
			f.write(self.foot.tobytes())