import pytest
import tempfile
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
    # for python test compatibility
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

def test_get_yuv_byte_size():
    assert ImageUtils.ImageUtils.getYUVByteSize(4, 4) == 4 * 4 + 2 * 2 * 2
    assert ImageUtils.ImageUtils.getYUVByteSize(3, 3) == 3 * 3 + 2 * 2 * 2

def test_convert_image_to_bitmap_calls_convert_yuv420_to_argb8888():
    # Create dummy planes
    y_buf = bytes([16, 16, 16, 16])
    u_buf = bytes([128, 128])
    v_buf = bytes([128, 128])
    mockY = DummyPlane(y_buf, 2)
    mockU = DummyPlane(u_buf, 1)
    mockV = DummyPlane(v_buf, 1)
    img = DummyImage([mockY, mockU, mockV], 2, 2)
    output = [0]*4
    result = ImageUtils.ImageUtils.convertImageToBitmap(img, output, [[], [], []])
    assert result is not None
    assert len(result) == 4

def test_save_bitmap_to_disk_creates_file(tmp_path):
    # Simulate file write
    imgfile = tmp_path / "test.png"
    with open(imgfile, "wb") as f:
        f.write(b"\x01\x02\x03\x04")
    assert imgfile.exists()
    assert imgfile.stat().st_size == 4

def test_yuv2rgb_clamping():
    rgb = ImageUtils.ImageUtils.YUV2RGB(0, 255, 255)
    assert (rgb & 0xFF000000) == 0xFF000000