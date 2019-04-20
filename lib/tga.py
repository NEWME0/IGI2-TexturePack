import numpy as np


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


from struct import unpack, pack


COLORMAP_TYPE_NONE = 0
COLORMAP_TYPE_TRUE = 1

PIXELMAP_TYPE_NONE = 0
PIXELMAP_TYPE_CMAP = 1
PIXELMAP_TYPE_TRUE = 2
PIXELMAP_TYPE_MONO = 3
PIXELMAP_TYPE_CMAP_RLE = 9
PIXELMAP_TYPE_TRUE_RLE = 10
PIXELMAP_TYPE_MONO_RLE = 11

TGA_SIGNATURE = b'TRUEVISION-XFILE.\x00'


class TGA_IO:
	_id_size = 0
	_cmap_type = COLORMAP_TYPE_NONE
	_pmap_type = PIXELMAP_TYPE_NONE
	_cmap_entry_first = 0
	_cmap_entry_count = 0
	_cmap_entry_width = 0
	_pmap_origin_x = 0
	_pmap_origin_y = 0
	_pmap_size_x = 0
	_pmap_size_y = 0
	_pmap_depth = 0
	_pmap_flags = 0
	_id = None
	_cmap = None
	_pmap = None
	_ext_offset = 0
	_dev_offset = 0
	_signature = b'TRUEVISION-XFILE.\x00'

	def reset(self):
		self._id_size = 0
		self._cmap_type = COLORMAP_TYPE_NONE
		self._pmap_type = PIXELMAP_TYPE_NONE
		self._cmap_entry_first = 0
		self._cmap_entry_count = 0
		self._cmap_entry_width = 0
		self._pmap_origin_x = 0
		self._pmap_origin_y = 0
		self._pmap_size_x = 0
		self._pmap_size_y = 0
		self._pmap_depth = 0
		self._pmap_flags = 0
		self._id = None
		self._cmap = None
		self._pmap = None
		self._ext_offset = 0
		self._dev_offset = 0
		self._signature = b'TRUEVISION-XFILE.\x00'

	def check(self):
		return True

	def save(self, path):
		with open(path, 'wb') as f:
			f.write(pack('B', self._id_size))
			f.write(pack('B', self._cmap_type))
			f.write(pack('B', self._pmap_type))
			f.write(pack('H', self._cmap_entry_first))
			f.write(pack('H', self._cmap_entry_count))
			f.write(pack('B', self._cmap_entry_width))
			f.write(pack('H', self._pmap_origin_x))
			f.write(pack('H', self._pmap_origin_y))
			f.write(pack('H', self._pmap_size_x))
			f.write(pack('H', self._pmap_size_y))
			f.write(pack('B', self._pmap_depth))
			f.write(pack('B', self._pmap_flags))

			if self._id:
				f.write(self._id)

			if self._cmap:
				f.write(self._cmap)

			if self._pmap:
				f.write(self._pmap)

			f.write(pack('I', self._ext_offset))
			f.write(pack('I', self._dev_offset))
			f.write(self._signature)

	def load(self, path):
		with open(path, 'rb') as f:
			self._id_size          = unpack('B', f.read(1))
			self._cmap_type        = unpack('B', f.read(1))
			self._pmap_type        = unpack('B', f.read(1))
			self._cmap_entry_first = unpack('H', f.read(2))
			self._cmap_entry_count = unpack('H', f.read(2))
			self._cmap_entry_width = unpack('B', f.read(1))
			self._pmap_origin_x    = unpack('H', f.read(2))
			self._pmap_origin_y    = unpack('H', f.read(2))
			self._pmap_size_x      = unpack('H', f.read(2))
			self._pmap_size_y      = unpack('H', f.read(2))
			self._pmap_depth       = unpack('B', f.read(1))
			self._pmap_flags       = unpack('B', f.read(1))

			if self._id_size:
				self._id = f.read(self._id_size)

			if self._cmap_type:
				self._cmap = f.read(self._cmap_entry_count * self._cmap_entry_width)

			if self._pmap_type:
				self._pmap = f.read(self._pmap_size_x * self._pmap_size_y * (self._pmap_depth // 8))

			self._ext_offset = unpack('I', f.read(4))
			self._dev_offset = unpack('I', f.read(4))
			self._signature = f.read(18)



class TGA_Object(TGA_IO):
	def getId(self):
		pass

	def setId(self):
		pass

	def getColorMap(self):
		pass

	def setColorMap(self):
		pass

	def getPixelMap(self):
		pass

	def setPixelMap(self):
		pass
