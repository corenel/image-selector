import sys
import util
import setting

if __name__ == '__main__':
    # util.check_platform()

    image_list = util.get_image_list(setting.IMAGE_DIR)
    invalid_list = []
    valid_list = []
    current_index = 0
    keycode = 255

    while keycode != setting.VALID_KEYS['exit']:
        if keycode == setting.VALID_KEYS['discard']:
            if current_index not in invalid_list:
                invalid_list.append(current_index)
            if current_index in valid_list:
                valid_list.remove(current_index)
        elif keycode == setting.VALID_KEYS['reserve']:
            if current_index in invalid_list:
                invalid_list.remove(current_index)
            if current_index not in valid_list:
                valid_list.append(current_index)
        elif keycode == setting.VALID_KEYS['process']:
            util.process_verified_images(image_list, invalid_list, valid_list)
            if len(image_list) == 0:
                print('Done!')
                break
            else:
                current_index = 0
        elif keycode == setting.VALID_KEYS['prev']:
            if current_index not in valid_list and current_index not in invalid_list:
                valid_list.append(current_index)
            current_index = max(0, current_index - 1)
        elif keycode == setting.VALID_KEYS['next']:
            if current_index not in valid_list and current_index not in invalid_list:
                valid_list.append(current_index)
            current_index = min(len(image_list) - 1, current_index + 1)

        images = util.read_images(image_list, 1, current_index, invalid_list)
        grid = util.create_image_grid(images)
        keycode = util.show_image_grid(grid)
