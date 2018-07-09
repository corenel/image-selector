import numpy as np

import os
import cv2
import click
import shutil

import setting


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


def pop_images(image_list, image_num):
    """
    Read numbers of images from list and pop

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


def read_images(image_list, image_num, start_idx=0, invalid_list=None):
    """
    Read numbers of images from list

    :param image_list: list of image files
    :type image_list: list[str]
    :param image_num: number of images to read
    :type image_num: int
    :param start_idx: start index of image to read
    :type start_idx: int
    :param invalid_list: list of invalid image (convert to grayscale)
    :type invalid_list: list[int]
    :return: image objects
    :rtype: np.ndarray
    """
    image_num = min(image_num, len(image_list))
    images = None
    for i in range(image_num):
        image_idx = start_idx + i
        image_filename = image_list[start_idx + i]
        image_temp = cv2.imread(os.path.join(setting.IMAGE_DIR, image_filename))
        if invalid_list is not None and image_idx in invalid_list:
            gray_image = cv2.cvtColor(image_temp, cv2.COLOR_BGR2GRAY)
            image_temp = np.stack((gray_image,) * 3, axis=-1)
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
        grid[y: y + img_h, x: x + img_w, ...] = images[idx]
    return grid


def show_image_grid(grid, scale=0.5):
    """
    Show image grid with scale factor

    :param grid: image grid
    :type grid: np.ndarray
    :param scale: image scale factor
    :type scale: float
    :return: pressed key
    :rtype: int
    """
    if scale != 1.0:
        scale_w = int(scale * grid.shape[1])
        scale_h = int(scale * grid.shape[0])
        grid = cv2.resize(grid, (scale_w, scale_h))

    cv2.imshow('image grid', grid)
    keycode = cv2.waitKey(0)

    return keycode


def process_verified_images(image_list, invalid_list, valid_list):
    """
    Move verified images to specific directory

    :param image_list: list of all images
    :type image_list: list[str]
    :param invalid_list: list of invalid image indices
    :type invalid_list: list[int]
    :param valid_list: list of valid image indices
    :type valid_list: list[int]
    """

    def move_images(index_list, dst):
        """
        Move images to given directory

        :param index_list: list of image indices
        :type index_list: list[int]
        :param dst: destination
        :type dst: str
        :return:
        :rtype:
        """
        if not os.path.exists(dst):
            os.makedirs(dst)
        for idx in index_list:
            image_filename = image_list[idx]
            src_path = os.path.join(setting.IMAGE_DIR, image_filename)
            dst_path = os.path.join(dst, image_filename)
            print('move {} to {}'.format(image_filename, dst_path))
            shutil.move(src_path, dst_path)

    move_images(invalid_list, setting.INVALID_IMAGE_DIR)
    move_images(valid_list, setting.VALID_IMAGE_DIR)

    filenames = [image_list[idx] for idx in invalid_list + valid_list]
    for filename in filenames:
        image_list.remove(filename)
    invalid_list.clear()
    valid_list.clear()


# def check_platform():
#     """
#     Check platform
#     """
#     import platform
#     if platform.system() == 'Darwin':
#         warning('[Notice] you need to run this program as root user in macOS')


def confirm(text, fg='blue', **kwargs):
    """
    Confirm prompt

    :param text: prompt text
    :type text: str
    :param fg: foreground color
    :type fg: str
    :param kwargs: other arguments
    :return: confirmation result
    :rtype: str
    """
    return click.confirm(
        click.style('> {}'.format(text), fg=fg, bold=True), **kwargs)


def confirmation(text, **confirm_args):
    """
    Decorator for confirmation (Yes for running function, No for not)

    :param text: prompt text
    :type text: str
    :param confirm_args: arguments for confirmation
    :return: confirmation result
    :rtype: str
    """

    def real_decorator(func):
        def wrapper(*args, **kwargs):
            if confirm(text, **confirm_args):
                func(*args, **kwargs)

        return wrapper

    return real_decorator


def prompt(text, **kwargs):
    """
    Popup a prompt

    :param text: prompt text
    :type text: str
    :param kwargs: other arguments
    :return: user input
    :rtype: str
    """
    return click.prompt(
        click.style('> {}'.format(text), fg='blue', bold=True), **kwargs)


def choice(text, choices, **kwargs):
    """
    Popup a choice prompt

    :param text: prompt text
    :type text: str
    :param choices: choices for user to choose
    :type choices: List[str}
    :param kwargs: other arguments
    :return: user choice
    :rtype: str
    """
    return click.prompt(
        click.style('> {}'.format(text), fg='blue', bold=True),
        type=click.Choice(choices),
        **kwargs)


def status(text):
    """
    Print running status

    :param text: status text
    :type text: str
    """
    click.secho('{}'.format(text), fg='blue', bold=True)


def info(text):
    """
    Print running info

    :param text: status text
    :type text: str
    """
    click.secho('{}'.format(text), fg='green', bold=True)


def warning(text):
    """
    Print warning message

    :param text: warning message
    :type text: str
    """
    click.secho('{}'.format(text), fg='yellow', bold=True)


def error(text):
    """
    Print error message

    :param text: error message
    :type text: str
    """
    click.secho('{}'.format(text), fg='red', bold=True)
