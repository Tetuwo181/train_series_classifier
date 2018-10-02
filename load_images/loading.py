from load_images import data_loader
from load_images import get_path
from typing import List
from typing import Optional


def load_images(base_dir_path: str,
                train_series_set: List[str],
                divide_num: int = 3,
                resize_val: Optional[int] = None ):
    """

    :param base_dir_path:
    :param train_series_set:
    :param divide_num:
    :param resize_val:
    :return:
    """
    path_and_class_set = get_path.get_train_paths_with_class(base_dir_path, train_series_set)
    results = []
    for path_and_class in path_and_class_set:
        images = data_loader.load_image_to_square_set(path_and_class[0], divide_num)
        image_and_class_set = [(image, path_and_class[1]) for image in images]
        results.extend(image_and_class_set)
    return results
