from enum import Enum
from struct import pack

# Magic ("DDS ")
DDS_MAGIC = 0x20534444

DDS_FOURCC = 0x00000004  # DDPF_FOURCC
DDS_NORMAL = 0x80000000  # DDPF_NORMAL

DDS_HEADER_FLAGS_TEXTURE = 0x00001007  # DDSD_CAPS | DDSD_HEIGHT | DDSD_WIDTH | DDSD_PIXELFORMAT
DDS_HEADER_FLAGS_MIPMAP = 0x00020000   # DDSD_MIPMAPCOUNT
DDS_HEADER_FLAGS_VOLUME = 0x00800000   # DDSD_DEPTH
DDS_HEADER_FLAGS_PITCH = 0x00000008   # DDSD_PITCH
DDS_HEADER_FLAGS_LINEARSIZE = 0x00080000   # DDSD_LINEARSIZE

DDS_SURFACE_FLAGS_TEXTURE = 0x00001000  # DDSCAPS_TEXTURE
DDS_SURFACE_FLAGS_MIPMAP = 0x00400008  # DDSCAPS_COMPLEX | DDSCAPS_MIPMAP
DDS_SURFACE_FLAGS_CUBEMAP = 0x00000008  # DDSCAPS_COMPLEX

DDS_CUBEMAP_POSITIVEX = 0x00000600  # DDSCAPS2_CUBEMAP | DDSCAPS2_CUBEMAP_POSITIVEX
DDS_CUBEMAP_NEGATIVEX = 0x00000a00  # DDSCAPS2_CUBEMAP | DDSCAPS2_CUBEMAP_NEGATIVEX
DDS_CUBEMAP_POSITIVEY = 0x00001200  # DDSCAPS2_CUBEMAP | DDSCAPS2_CUBEMAP_POSITIVEY
DDS_CUBEMAP_NEGATIVEY = 0x00002200  # DDSCAPS2_CUBEMAP | DDSCAPS2_CUBEMAP_NEGATIVEY
DDS_CUBEMAP_POSITIVEZ = 0x00004200  # DDSCAPS2_CUBEMAP | DDSCAPS2_CUBEMAP_POSITIVEZ
DDS_CUBEMAP_NEGATIVEZ = 0x00008200  # DDSCAPS2_CUBEMAP | DDSCAPS2_CUBEMAP_NEGATIVEZ

DDS_CUBEMAP_ALLFACES = (DDS_CUBEMAP_POSITIVEX | DDS_CUBEMAP_NEGATIVEX |
                        DDS_CUBEMAP_POSITIVEY | DDS_CUBEMAP_NEGATIVEY |
                        DDS_CUBEMAP_POSITIVEZ | DDS_CUBEMAP_NEGATIVEZ)


class DDS_FORMAT(Enum):
    UNKNOWN = 0
    ABGR4 = 1        # Should be the first uncompressed format with RGBA components
    ARGB4 = 2        # as needed per rgba_convert() format validation.
    GRAB4 = 3
    RGBA4 = 4
    ABGR8 = 5
    ARGB8 = 6
    GRAB8 = 7
    RGBA8 = 8        # Should be the last uncompressed format with RGBA components
    ARGB16 = 9
    ARGB32 = 10
    RXGB8 = 11
    BGR8 = 12
    R8 = 13
    UVER = 14
    DXT1 = 15
    DXT2 = 16
    DXT3 = 17
    DXT4 = 18
    DXT5 = 19
    DX10 = 20
    BC4 = 21
    BC5 = 22
    BC6 = 23
    BC7 = 24
    BC6H = 25
    BC7L = 26
    ATI1 = 27
    ATI2 = 28
    A2XY = 29
    DDS = 30
    NVTT = 31


def dds_bpb(format: DDS_FORMAT) -> int:
    # DDS format: Bytes per pixel block
    if format in [DDS_FORMAT.DXT2, DDS_FORMAT.DXT3, DDS_FORMAT.DXT4, DDS_FORMAT.DXT5, DDS_FORMAT.DX10,
                  DDS_FORMAT.BC5, DDS_FORMAT.BC6, DDS_FORMAT.BC6H, DDS_FORMAT.BC7,
                  DDS_FORMAT.ATI2, DDS_FORMAT.ARGB32]:
        return 16
    if format in [DDS_FORMAT.DXT1, DDS_FORMAT.BC4, DDS_FORMAT.ATI1, DDS_FORMAT.ARGB16]:
        return 8
    if format in [DDS_FORMAT.ABGR8, DDS_FORMAT.ARGB8, DDS_FORMAT.GRAB8, DDS_FORMAT.RGBA8, DDS_FORMAT.RXGB8]:
        return 4
    if format in [DDS_FORMAT.BGR8]:
        return 3
    if format in [DDS_FORMAT.ABGR4, DDS_FORMAT.ARGB4, DDS_FORMAT.GRAB4, DDS_FORMAT.RGBA4]:
        return 2
    if format in [DDS_FORMAT.R8]:
        return 1

    # No idea, so assert and return 0
    return 0


def dds_bpp(format: DDS_FORMAT) -> int:
    # DDS format: Bits per individual pixel
    if format == DDS_FORMAT.ARGB32:
        return 128
    if format == DDS_FORMAT.ARGB16:
        return 64
    if format in [DDS_FORMAT.ABGR8, DDS_FORMAT.ARGB8, DDS_FORMAT.GRAB8,
                  DDS_FORMAT.RGBA8, DDS_FORMAT.RXGB8]:
        return 32
    if format == DDS_FORMAT.BGR8:
        return 24
    if format in [DDS_FORMAT.ABGR4, DDS_FORMAT.ARGB4, DDS_FORMAT.GRAB4,
                  DDS_FORMAT.RGBA4]:
        return 16
    if format == DDS_FORMAT.R8:
        return 8
    if format in [DDS_FORMAT.DXT1, DDS_FORMAT.BC4, DDS_FORMAT.ATI1]:
        return 4
    if format in [DDS_FORMAT.DXT2, DDS_FORMAT.DXT3, DDS_FORMAT.DXT4,
                  DDS_FORMAT.DXT5, DDS_FORMAT.DX10, DDS_FORMAT.BC5,
                  DDS_FORMAT.BC6, DDS_FORMAT.BC6H, DDS_FORMAT.BC7,
                  DDS_FORMAT.ATI2]:
        return 8

    # No idea, so assert and return 0
    return 0


class DDS_HEADER():
    def __init__(self):
        self.flags: int = 0
        self.height: int = 0
        self.width: int = 0
        self.pitchOrLinearSize: int = 0

        self.pfflags: int = 0
        self.fourCC: int = 0

        self.mipMapCount: int = 0
        self.caps: int = 0
        self.caps2: int = 0

    def save(self) -> bytes:
        return pack('<IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII',
                    DDS_MAGIC,
                    124,  # header size
                    self.flags,  # flags
                    self.height,
                    self.width,
                    self.pitchOrLinearSize,  # pitch
                    0,  # depth
                    self.mipMapCount,  # mipmaps
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # reserved
                    32,  # pfsize
                    self.pfflags,  # pfflags
                    self.fourCC,  # fourcc
                    0,  # bitcount
                    0, 0, 0, 0,  # rgbabitmask
                    self.caps,  # dwCaps
                    self.caps2,  # dwCaps2
                    0,  # dwCaps3
                    0,  # dwCaps4
                    0,  # dwReserved2
                    )


def get_fourCC(format):
    if format == DDS_FORMAT.DXT1:
        return 0x31545844  # DXT1
    if format == DDS_FORMAT.DXT3:
        return 0x33545844  # DXT3
    if format == DDS_FORMAT.DXT5:
        return 0x35545844  # DXT5
    return 0
