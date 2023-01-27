import logging
import logging.config
import sys
import os
import io
import pytesseract
from PIL import Image

from docsultant.imgproc import ImageProcessor
from docsultant.hocr import HocrParser
from docsultant.core import app_config

logger = logging.getLogger(__name__)

class TesseractOcr:

    def __init__(self):
        self.imgProc = ImageProcessor()

    def ocr_check(self, path, chain="sharpen|threshold(140)|bw") -> str:
        logger.debug(f'ocr_check(path={path})')
        img = self.imgProc.chain(path, chain)
        img = Image.open(io.BytesIO(img))
        doc = self.tesseract_micr_hocr(img)
        # TODO: do preliminary regexp filtering
        return "\n".join([line.text for line in doc.lines])

    def tesseract_plain(self, path, chain) -> str:
        logger.debug(f'tesseract_plain(path={path})')
        if chain:
            img = self.imgProc.chain(path, chain)
            path = Image.open(io.BytesIO(img))
        res = pytesseract.image_to_string(path)
        logger.debug("-> "+res)
        return res

    def tesseract_hocr(self, path, chain) -> HocrParser.Document:
        logger.debug(f'tesseract_hocr(path={path})')

        if chain:
            img = self.imgProc.chain(path, chain)
            path = Image.open(io.BytesIO(img))

        # psm 4, psm 6
        cfg = f" -c hocr_char_boxes=1" \
              " hocr"
        logger.debug(f"cfg={cfg}")
        res = pytesseract.image_to_pdf_or_hocr(path, config=cfg, extension='hocr')
        res = res.decode('utf-8')

        hp = HocrParser()
        doc = hp.parse(res)
        return doc


    def tesseract_micr(self, path) -> str:
        logger.debug(f'tesseract_micr(path={path})')
        tessdataPath = os.path.join(app_config.ROOT_PATH, "tessdata")
        cfg = f" --tessdata-dir {tessdataPath}" \
              " -l micr --psm 6" \
              " -c tessedit_char_whitelist=0123456789acd "
        logger.debug(f"cfg={cfg}")
        res = pytesseract.image_to_string(path, lang='micr', config=cfg)
        logger.debug("-> "+res)
        return res

    def tesseract_micr_hocr(self, path) -> HocrParser.Document:
        logger.debug(f'tesseract_micr_hocr(path={path})')
        tessdataPath = os.path.join(app_config.ROOT_PATH, "tessdata")
        cfg = f" --tessdata-dir {tessdataPath}" \
              " -l micr --psm 6" \
              " -c tessedit_char_whitelist=0123456789acd " \
              " -c hocr_char_boxes=1" \
              " -c lstm_choice_mode=1" \
              " -c tessedit_pageseg_mode=6" \
              " hocr"
        logger.debug(f"cfg={cfg}")
        res = pytesseract.image_to_pdf_or_hocr(path, \
                     lang='micr', config=cfg, extension='hocr')
        res = res.decode('utf-8')

        hp = HocrParser()
        doc = hp.parse(res)
        #logger.debug("-> "+res)
        return doc

    def tesseract_version(self):
        return "tesseract {}".format(pytesseract.get_tesseract_version())


