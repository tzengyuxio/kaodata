from struct import pack
from dds import *

# Known flags
G1T_FLAG_STANDARD_FLAGS = 0x000000011200  # Flags that are commonly set
G1T_FLAG_EXTENDED_DATA = 0x000000000001  # Set if the texture has local data in the texture entry.
G1T_FLAG_SRGB = 0x000000002000  # Set if the texture uses sRGB
G1T_FLAG_NORMAL_MAP = 0x030000000000  # Usually set for normal maps (but not always)
G1T_FLAG_SURFACE_TEX = 0x000000000001  # Set for textures that appear on a model's surface
G1T_FLAG_TEXTURE_ARRAY = 0x0000F00F0000
# This one is not used in G1Ts, but only in this application
G1T_FLAG_CUBE_MAP = 0x000100000000


class G1tHeader:
    def __init__(self):
        self.magic: str = ''
        self.version: str = ''
        self.total_size: int = 0
        self.header_size: int = 0
        self.nb_textures: int = 0
        self.platform: int = 0
        self.extra_size: int = 0

    def to_bytes(self) -> bytes:
        return pack('<4s4sIIIII', self.magic, self.version,
                    self.total_size, self.header_size, self.nb_textures,
                    self.platform, self.extra_size)


class G1tTexHeader:
    def __init__(self):
        self.z_mipmaps: int = 0
        self.mipmaps: int = 0
        self.type: int = 0
        self.dx: int = 0
        self.dy: int = 0
        self.flags: list = []


def write_dds_header(format, width: int, height: int, mipmaps: int, flags) -> bytes:
    if width == 0 or height == 0:
        return bytes()

    bpb = dds_bpb(format)
    use_dx10 = (format == DDS_FORMAT.BC7) or (format == DDS_FORMAT.DX10) or (
        flags[0] & G1T_FLAG_SRGB) or (flags[1] & G1T_FLAG_TEXTURE_ARRAY)

    header = DDS_HEADER()
    header.flags = DDS_HEADER_FLAGS_TEXTURE | DDS_HEADER_FLAGS_LINEARSIZE
    header.height = height
    header.width = width
    header.pitchOrLinearSize = ((width+3)//4) * ((height+3)//4) * bpb if bpb >= 8 else width * height * bpb

    header.pfflags = DDS_FOURCC
    header.fourCC = get_fourCC(format)

    header.mipMapCount = mipmaps
    header.caps = DDS_SURFACE_FLAGS_TEXTURE
    header.caps2 = 0
    if mipmaps != 0:
        header.flags |= DDS_HEADER_FLAGS_MIPMAP
        header.caps |= DDS_SURFACE_FLAGS_MIPMAP
    if flags[1] & G1T_FLAG_CUBE_MAP:
        header.caps |= DDS_SURFACE_FLAGS_CUBEMAP
        header.caps2 = DDS_CUBEMAP_ALLFACES
    if flags[0] & G1T_FLAG_NORMAL_MAP:
        header.pfflags |= DDS_NORMAL

    return header.save()
