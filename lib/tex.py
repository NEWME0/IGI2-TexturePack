import numpy as np


TEX_SIGNATURE = b'LOOP'


DTYPE_TEX_HEADER = np.dtype([
    ('signature', (np.uint8, 4)),
    ('unk11',  np.uint32),
    ('ptype',  np.uint32),
    ('multi',  np.uint32),
    ('unk00',  np.uint32),
    ('unk05',  np.uint16),
    ('sizex0', np.uint16),
    ('sizey0', np.uint16),
    ('sizex',  np.uint16),
    ('sizey',  np.uint16),
    ('psize',  np.uint16),
    ])


class TEXObject:
    head = None
    pmap = None

    def free(self):
        self.head = None
        self.pmap = None

    def load(self, path):
        self.free()

        with open(path, 'rb') as f:
            self.head = np.frombuffer(f.read(32), DTYPE_TEX_HEADER)

            x = int(self.head['sizex'])
            y = int(self.head['sizey'])
            d = int(self.head['psize'])

            if d == 2:
                dtype = np.uint16
            elif d == 4:
                dtype = np.uint32

            self.pmap = np.frombuffer(f.read(x * y * d), dtype)

    def save(self, path):
        with open(path, 'wb') as f:
            f.write(self.head.tobytes())
            f.write(self.pmap.tobytes())


PTYPE_ARGB_1555_TRUE = 2
PTYPE_ARGB_8888_NONE = 3
PTYPE_ARGB_1555_NONE = 66
PTYPE_ARGB_8888_TRUE = 67

PTYPE_VALID          = (PTYPE_ARGB_1555_TRUE,
                        PTYPE_ARGB_8888_NONE,
                        PTYPE_ARGB_1555_NONE,
                        PTYPE_ARGB_8888_TRUE)

MULTI_FALSE          = 0
MULTI_TRUE           = 524288

MULTI_VALID          = (MULTI_FALSE,
                        MULTI_TRUE)

MULTI_DEFAULT        = MULTI_FALSE

INFRA_SCALE_2        = 2
INFRA_SCALE_3        = 3
INFRA_SCALE_4        = 4
INFRA_SCALE_5        = 5
INFRA_SCALE_6        = 6
INFRA_SCALE_7        = 7
INFRA_SCALE_8        = 8

INFRA_SCALE_VALID    = (INFRA_SCALE_2,
                        INFRA_SCALE_3,
                        INFRA_SCALE_4,
                        INFRA_SCALE_5,
                        INFRA_SCALE_6,
                        INFRA_SCALE_7,
                        INFRA_SCALE_8)

INFRA_SCALE_DEFAULT  = INFRA_SCALE_5


class TEXObj:
    def reset(self):
        _signature = b'LOOP'
        _0         = 11
        _ptype     = None
        _multi     = 0
        _1         = 0
        _infra     = 5
        _as_width  = None
        _as_height = None
        _width     = None
        _height    = None
        _psize     = None
        _pmap      = None
        _lod0      = None
        _lod1      = None
        _lod2      = None
        _lod3      = None
        _lod4      = None
        _lod5      = None
        _lod6      = None
        _lod7      = None
        _lod8      = None

    def set_pixel_type(self, ptype):
        if ptype in PTYPE_ARGB_8888_TRUE, PTYPE_ARGB_8888_NONE:
            self._ptype = ptype
            self._psize = 4

        elif ptype in PTYPE_ARGB_1555_TRUE, PTYPE_ARGB_1555_NONE:
            self._ptype = ptype
            self._psize = 2

        else:
            raise ValueError("Unsuported pixel type")

    def set_image_data(self, pmap, width, height):
        if not isinstance(pmap, np.array):
            raise ValueError("Image data should be numpy array")

        if width * height != len(pmap):
            raise ValueError("Wrong image data")

        self._width = width
        self._as_width = width
        self._height = height
        self._as_height = height

        self._pmap = pmap
