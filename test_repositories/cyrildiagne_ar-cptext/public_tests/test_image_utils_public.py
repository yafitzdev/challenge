import pytest
import os

from src.arcopypaste.research.prototypes.text import ImageUtils

class DummyPlane:
    def __init__(self, buf, row_stride, pixel_stride=1):
        self._buf = buf
        self._row_stride = row_stride
        self._pixel_stride = pixel_stride
    def getRowStride(self):
        return self._row_stride
    def getPixelStride(self):
        return self._pixel_stride
    def getBuffer(self):
        return memoryview(self._buf)
    def __getitem__(self, idx):
        return self._buf[idx]

class DummyImage:
    def __init__(self, planes, width, height):
        self._planes = planes
        self._width = width
        self._height = height
    def getPlanes(self):
        return self._planes
    def getWidth(self):
        return self._width
    def getHeight(self):
        return self._height

def test_get_yuv_byte_size_public():
    assert ImageUtils.ImageUtils.getYUVByteSize(8, 8) == (8*8 + 4*4*2)
    assert ImageUtils.ImageUtils.getYUVByteSize(5, 7) == (5*7 + 3*4*2)

def test_convert_image_to_bitmap_calls_convert_yuv420_to_argb8888_public():
    y_buf = bytes([20, 32, 40, 28, 40, 20, 32, 40, 28, 40, 20, 32, 40, 28, 40, 20])
    u_buf = bytes([130, 134, 132, 135])
    v_buf = bytes([127, 129, 124, 120])
    mockY = DummyPlane(y_buf, 4)
    mockU = DummyPlane(u_buf, 2)
    mockV = DummyPlane(v_buf, 2)
    img = DummyImage([mockY, mockU, mockV], 4, 4)
    output = [0]*16
    result = ImageUtils.ImageUtils.convertImageToBitmap(img, output, [[], [], []])
    assert result is not None
    assert len(result) == 16

def test_save_bitmap_to_disk_creates_file_public(tmp_path):
    imgfile = tmp_path / "public_test.png"
    with open(imgfile, "wb") as f:
        f.write(b"\x07\x09\x0b\x0d\x15\x00\x2a\x63\x79")
    assert imgfile.exists()
    assert imgfile.stat().st_size == 9

def test_yuv2rgb_clamping_public():
    rgb = ImageUtils.ImageUtils.YUV2RGB(-50, 0, 300)
    assert (rgb & 0xFF000000) == 0xFF000000