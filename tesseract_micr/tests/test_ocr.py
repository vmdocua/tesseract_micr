import pytest
from tesseract_micr.ocr import TesseractOcr

def test_tesseract_version():
    t = TesseractOcr()
    s = t.tesseractVersion()
    print(" version={}".format(s))
    v = s.split(" ")[1]
    assert v.startswith("5.") or v.startswith("4."), \
        "Unsupported tesseract version {}".format(s)
