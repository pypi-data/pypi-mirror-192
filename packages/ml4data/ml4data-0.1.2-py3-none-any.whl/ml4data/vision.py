from typing import Any, BinaryIO, Dict, Optional, Union
from ml4data.base import FileType, ML4DataClient
from PIL import Image
from io import BytesIO
from pathlib import Path

ImageType = Union[str, Path, Image.Image, BinaryIO]


class VisionClient(ML4DataClient):
    base_url = ML4DataClient.base_url + '/vision'

    def _send_image(self,
                    endpoint: str,
                    img: Optional[ImageType] = None,
                    url: Optional[str] =None) -> Any:
        if (img is None and url is None) or (img is not None and url is not None):
            raise ValueError("Pass either a path, file handler, Pillow image or url as argument")

        if img is not None:
            if isinstance(img, (str, Path)):
                with open(img, 'rb') as fp:
                    r = self._post(endpoint=endpoint,
                                   files={'file': fp})
            elif isinstance(img, Image.Image):
                b = BytesIO()
                img.save(b, 'png')
                b.seek(0)
                r = self._post(endpoint=endpoint,
                               files={'file': b})
            else: # file-like
                r = self._post(endpoint=endpoint,
                               files={'file': img})
        else: # url is not None:
            r = self._get(endpoint=endpoint,
                          params={'url': url})
        return r

    def detect_object(self,
                      img: Optional[ImageType] = None,
                      url: Optional[str] = None) -> Dict:
        """ Detect objects in an image

        Pass either one of img, url as arguments

        Params:
            img (str, file-like or PIL.Image): Path to the image, or file
                handler of the opened image, or Pillow image
            url (str): Image url
        """
        return self._send_image('/object-detection',
                                img=img,
                                url=url)

    def detect_facemask(self,
                        img: Optional[ImageType] = None,
                        url: Optional[str] = None) -> Dict:
        """ Detect face maks in an image

        Pass either one of path, fp, img, url as arguments

        Params:
            img (str, file-like or PIL.Image): Path to the image, or file
                handler of the opened image, or Pillow image
            url (str): Image url
        """
        return self._send_image('/facemask-detection',
                                img=img,
                                url=url)

    def classify_product(self,
                         img: Optional[ImageType] = None,
                         url: Optional[str] = None) -> Dict:
        """ Classify the main product in an image

        Pass either one of path, fp, img, url as arguments

        Params:
            img (str, file-like or PIL.Image): Path to the image, or file
                handler of the opened image, or Pillow image
            url (str): Image url
        """
        return self._send_image('/products',
                                img=img,
                                url=url)

    def ocr(self,
            img: Optional[ImageType] = None,
            url: Optional[str] = None) -> Dict:
        """ Extract text from an image

        Pass either one of path, fp, img, url as arguments

        Params:
            img (str, file-like or PIL.Image): Path to the image, or file
                handler of the opened image, or Pillow image
            url (str): Image url
        """
        return self._send_image('/ocr',
                                img=img,
                                url=url)

    def colors(self,
               img: Optional[ImageType] = None,
               url: Optional[str] = None) -> Dict:
        """ Find main colors in an image

        Pass either one of path, fp, img, url as arguments

        Params:
            img (str, file-like or PIL.Image): Path to the image, or file
                handler of the opened image, or Pillow image
            url (str): Image url
        """
        return self._send_image('/colors',
                                img=img,
                                url=url)

    def create_qrs(self,
                   file: FileType,
                   code_column: str,
                   label_column: str,
                   sheet_name: Optional[str] = None,
                   page_size: str = 'A4',
                   dpi: int = 72,
                   font_size: int = 8,
                   qr_size: float = 2,
                   fg_color: str = 'black',
                   bg_color: str = 'white') -> bytes:
        """ Create QR codes from an file

        Params:
            file (FileType): Path to the file, or file handler of the opened file
            code_column (str): Column name for code
            label_column (str): Column name for label
            sheet_name (str): Sheet name for Excel file
            page_size (str): Page size, e.g. A4, A5, A6, Letter, Legal
            dpi (int): DPI
            font_size (int): Font size
            qr_size (float): QR size
            fg_color (str): Foreground color
            bg_color (str): Background color
        """
        res =  self._send_file('/qr-maker',
                               file,
                               params={'code_column': code_column,
                                       'label_column': label_column,
                                       'sheet_name': sheet_name,
                                       'page_size': page_size,
                                       'dpi': dpi,
                                       'font_size': font_size,
                                       'qr_size': qr_size,
                                       'fg_color': fg_color,
                                       'bg_color': bg_color})
        return res
