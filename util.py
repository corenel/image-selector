import os
import cv2
import setting
import numpy as np


def get_image_list(path):
    """
    Get list of image files in given directory

    :param path: path of image directory
    :type path: str
    :return: list of image files
    :rtype: list[str]
    """
    return [f for f in os.listdir(path)
            if os.path.splitext(f)[1] in setting.IMAGE_EXT]


def read_images(image_list, image_num):
    """
    Read numbers of images from list

    :param image_list: list of image files
    :type image_list: list[str]
    :param image_num: number of images to read
    :type image_num: int
    :return: image objects
    :rtype: np.ndarray
    """
    image_num = min(image_num, len(image_list))
    images = None
    for i in range(image_num):
        image_filename = image_list.pop()
        image_temp = cv2.imread(os.path.join(setting.IMAGE_DIR, image_filename))
        if images is None:
            images = np.expand_dims(image_temp, axis=0)
        else:
            images = np.concatenate((images, np.expand_dims(image_temp, axis=0)),
                                    axis=0)
    return images


def create_image_grid(images, grid_size=None):
    """
    Create a image grid with given images

    :param images: some images in shape of (N, H, W, C)
    :type images: np.ndarray
    :param grid_size: grid size like (grid_w, grid_h)
    :type grid_size: tuple
    :return: image grid
    :rtype: np.ndarray
    """
    assert images.ndim == 4
    num, img_c, img_w, img_h = images.shape[0], images.shape[3], images.shape[2], images.shape[1]

    if grid_size is not None:
        grid_w, grid_h = tuple(grid_size)
    else:
        grid_w = max(int(np.ceil(np.sqrt(num))), 1)
        grid_h = max((num - 1) // grid_w + 1, 1)

    grid = np.zeros([grid_h * img_h, grid_w * img_w, img_c], dtype=images.dtype)
    for idx in range(num):
        x = (idx % grid_w) * img_w
        y = (idx // grid_w) * img_h
        print(x, y)
        grid[y: y + img_h, x: x + img_w, ...] = images[idx]
    return grid


def show_image_grid(grid, scale=0.5):
    """
    Show image grid with scale factor

    :param grid: image grid
    :type grid: np.ndarray
    :param scale: image scale factor
    :type scale: float
    """
    if scale != 1.0:
        scale_w = int(scale * grid.shape[1])
        scale_h = int(scale * grid.shape[0])
        grid = cv2.resize(grid, (scale_w, scale_h))

    cv2.imshow('image grid', grid)
    cv2.waitKey(0)

