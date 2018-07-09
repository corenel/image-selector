import sys
import util
import setting

if __name__ == '__main__':
    # util.check_platform()

    image_list = util.get_image_list(setting.IMAGE_DIR)
    invalid_list = []
    current_index = 0
    keycode = 255

    while keycode != setting.VALID_KEYS['exit']:
        if keycode == setting.VALID_KEYS['discard'] and current_index not in invalid_list:
            invalid_list.append(current_index)
        elif keycode == setting.VALID_KEYS['reserve'] and current_index in invalid_list:
            invalid_list.remove(current_index)
        elif keycode == setting.VALID_KEYS['prev']:
            current_index = max(0, current_index - 1)
        elif keycode == setting.VALID_KEYS['next']:
            current_index = min(len(image_list) - 1, current_index + 1)
        elif keycode == setting.VALID_KEYS['process']:
            print(invalid_list)

        images = util.read_images(image_list, 1, current_index)
        grid = util.create_image_grid(images)
        keycode = util.show_image_grid(grid)
