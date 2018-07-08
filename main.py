import cv2
import util
import setting
from pynput import keyboard


def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
        print('special key {0} pressed'.format(key))


def on_release(key):
    print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False


if __name__ == '__main__':
    util.check_platform()
    # image_list = util.get_image_list(setting.IMAGE_DIR)
    # images = util.read_images(image_list, 6)
    # grid = util.create_image_grid(images)
    # util.show_image_grid(grid)
    # Collect events until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
