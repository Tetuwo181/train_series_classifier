import os
from typing import List
from typing import Tuple
from typing import Optional
from numba impor jit


IMG_EXT_LIST = ("jpg", "jpeg", "png", "gif")


def is_image(img_path:str)->bool:
    """
    拡張子から画像ファイルかどうか判定する
    :param img_path: ファイルのパス
    :return:
    """
    root, ext = os.path.splitext(img_path)
    return ext in IMG_EXT_LIST


def search_photo_paths(dir_path: str, train_series: str):
    """
    ディレクトリ直下にある指定した形式の車両の写真のパスの一覧を取得する
    :param dir_path: 調査対象のディレクトリ
    :param train_series:　鉄道の形式名 ex 223系　383系　阪急9000系など
    :return: 鉄道車両のファイルのパス(jpegかpngファイルのみ取得)
    """
    img_paths = [img_path for img_path in os.listdir(dir_path) if is_image(img_path)]
    return [os.path.join(dir_path, img_path) for img_path in img_paths
            if img_path[:len(train_series)] == train_series]


def search_photo_paths_under_dir(base_dir_path: str, train_series: str, base_paths: Optional[List[str]] = None):
    """
    ディレクトリ以下の指定した形式の車両の写真のパスの一覧を取得する
    基本的に外部から使用する際はbase_pathsを設定しないことを推奨
    :param base_dir_path:ベースとなるディレクトリのパス
    :param train_series:鉄道車両の形式
    :param base_paths:今まで取得してきたファイルのパス
    :return:
    """
    paths_now_dir = search_photo_paths(base_dir_path, train_series)
    paths = paths_now_dir if base_paths is None else base_paths + paths_now_dir
    dir_paths = [path for path in os.listdir(base_dir_path) if os.path.isdir(path)]
    if dir_paths is []:
        pass
    else:
        for dir_path in dir_paths:
            paths = paths + search_photo_paths(os.path.join(base_dir_path, dir_path), train_series)
    return paths


@jit
def get_train_paths_with_class(base_dir_path: str, train_series_set: List[str])->List[Tuple[str, int]]:
    """
    ディレクトリ以下の指定した形式の車両の写真のパスの一覧を取得する
    :param base_dir_path:ベースとなるディレクトリのパス
    :param train_series_set:鉄道車両の形式のリスト
    :return: 鉄道車両の形式とクラス分類のインデックス
    """
    result = []
    for index, series in enumerate(train_series_set):
        base_path_set = searcj_photo_paths_under_dir(base_dir_path, series)
        for path in base_path_set:
            result.append((index, path))
    return result
