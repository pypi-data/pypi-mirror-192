import base64
import io
from typing import Optional, List, Tuple, Union

import requests
from PIL import Image
from pydantic.main import BaseModel

from filedata.config import Config
from filedata.retry import retry_api
from filedata.utils import edit_distance

RegionBox = Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int]]


class OCRRegion(BaseModel):
    confidence: float = None
    text: str
    text_region: RegionBox


@retry_api
def ocr(source: Union[bytes, Image.Image], timeout: int = 20) -> List[OCRRegion]:
    if isinstance(source, Image.Image):
        img_bytes_io = io.BytesIO()
        source.save(img_bytes_io, format='jpeg')
        source = img_bytes_io.getvalue()

    image = base64.b64encode(source).decode('utf8')
    data = {"images": [image]}
    resp = requests.post(
        url=f'http://{Config.PADDLE_OCR_HOST}/predict/ocr_system',
        json=data,
        timeout=timeout,
    )
    resp.raise_for_status()
    res = resp.json()['results'][0]
    return [OCRRegion(**i) for i in res]


def get_content_by_ocr(source: Union[bytes, Image.Image], timeout: int = 20) -> str:
    """
    基于OCR获取文本内容
    :param source: 原始图片
    :param timeout: 超时时间
    :return:
    """
    if isinstance(source, Image.Image):
        img_bytes_io = io.BytesIO()
        source.save(img_bytes_io, format='jpeg')
        source = img_bytes_io.getvalue()
    # TODO 根据框的位置排列文本，加入适当的空格和换行，换行个数可以考虑根据文本框的高度来确定


def select_longest_region(regions: List[OCRRegion]) -> Optional[OCRRegion]:
    """
    选择字数最多的区域
    """
    m = 0
    region = None
    for r in regions:
        _m = len(r.text)
        if _m > m:
            m = _m
            region = r
    return region


def crop_region(
        img: Union[bytes, Image.Image],
        box: RegionBox,
        margin: int = 0,
        angle: int = 0,
) -> bytes:
    if isinstance(img, bytes):
        img: Image.Image = Image.open(io.BytesIO(img))
        img = img.convert('RGB')

    x1 = min(box[0][0], box[3][0])
    x2 = max(box[1][0], box[2][0])
    y1 = min(box[0][1], box[1][1])
    y2 = max(box[2][1], box[3][1])

    _crop = img.crop((
        max(x1 - margin, 0),
        max(y1 - margin, 0),
        min(x2 + margin, img.width),
        min(y2 + margin, img.height),
    ))

    if angle != 0:
        _crop = _crop.rotate(angle, expand=True)

    img_bytes_io = io.BytesIO()
    _crop.save(img_bytes_io, format='jpeg')
    return img_bytes_io.getvalue()


def detect_direction(
        img: Union[bytes, Image.Image],
        ocr_result: List[OCRRegion],
        timeout: int = 20,
) -> int:
    """
    根据OCR结果判断图片方向

    :param img: 原始图片
    :param ocr_result: OCR结果
    :return: 0, 90, 180, 270, 表示图片被顺时针旋转了多少度
    """

    if isinstance(img, bytes):
        img: Image.Image = Image.open(io.BytesIO(img))
        img = img.convert('RGB')

    region = select_longest_region(ocr_result)

    t = region.text_region
    if t[1][0] - t[0][0] > t[3][1] - t[0][1]:
        angle = 0
    else:
        angle = 90

    x1 = min(t[0][0], t[3][0])
    x2 = max(t[1][0], t[2][0])
    y1 = min(t[0][1], t[1][1])
    y2 = max(t[2][1], t[3][1])
    rw = (x2 - x1) // 2
    rh = (y2 - y1) // 2

    if angle == 0:
        r = (
            (x1, y1),
            (x1 + rw, y1),
            (x1 + rw, y2),
            (x1, y2),
        )
    else:
        r = (
            (x1, y1),
            (x2, y1),
            (x2, y1 + rh),
            (x1, y1 + rh),
        )
    crop_bytes = crop_region(img, r, margin=20, angle=angle)

    crop_result = ocr(crop_bytes, timeout=timeout)
    crop_text = ''.join([i.text for i in crop_result])

    mid = len(region.text) // 2
    if edit_distance(crop_text, region.text[:mid]) > edit_distance(crop_text, region.text[mid:]):
        angle += 180

    return angle


def rotate_region_box_90(box: RegionBox, width: int, height: int) -> RegionBox:
    """
    顺时针旋转90度
    """
    # TODO


def save_to_jpeg(img: Union[bytes, Image.Image]) -> bytes:
    """
    图片转为jpeg，具有去除EXIF方向信息的功能
    """
    if isinstance(img, bytes):
        img: Image.Image = Image.open(io.BytesIO(img))
        img = img.convert('RGB')

    img_bytes_io = io.BytesIO()
    img.save(img_bytes_io, format='jpeg')
    return img_bytes_io.getvalue()
