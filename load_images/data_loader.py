import cv2
import numpy as np
from typing import Tuple
from typing import Optional


def get_space(shorter: int, longer: int, divide_num: int = 3)->Tuple[int, int]:
    use_divide_num = divide_num if divide_num > 0 else 1
    width = abs(longer-shorter)
    return width, int(width/use_divide_num)


def load_image(img_path: str):
    """
    指定されたパスの画像ファイルを読み込む
    :param img_path: 画像ファイル
    :return:
    """
    raw_img = cv2.imread(img_path)
    return cv2.cvtColor(raw_img, cv2.COLOR_BGR2RGB)


def get_image_pixels(image)->Tuple[int, int]:
    """
    画像のピクセル数を指定する
    :param image:
    :return:
    """
    return image.shape[0], image.shape[1]


def trimming_to_square(image, divide_num: int = 3):
    """
    入力した画像を正方形に分割数分だけスライスする
    :param image: 元となる画像データ
    :param divide_num: 分割数
    :return:
    """
    raw, col = get_image_pixels(image)
    space = get_space(raw, col, divide_num)
    if raw > col:
        return [image[index*space: index*space + col, 0:col]
                for index in range(divide_num)]
    return [image[0:raw, index*space:index*space+raw]
            for index in range(divide_num)]


def load_image_to_square_set(image_path: str, divide_num: int = 3):
    raw_image = load_image(image_path)
    return trimming_to_square(raw_image, divide_num)


def normalise_img(img: np.ndarray)->np.ndarray:
    """
    画像を正規化
    :param img: 正規化する対象
    :return: 正規化後の配列
    """
    return (img.astype(np.float32) - 127.5) / 127.5


def run(image_path,
        divide_num: int = 3,
        image_resize_val: Optional[int] = None):
    raw_image_set = load_image_to_square_set(image_path, divide_num)
    if image_resize_val is None:
        return raw_image_set
    return [cv2.resize(image, (image_resize_val, image_resize_val)) for image in raw_image_set]
