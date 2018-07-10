import sys
import util
import setting

if __name__ == '__main__':
    # util.check_platform()

    image_list = util.get_image_list(setting.IMAGE_DIR)
    assert len(image_list) != 0
    invalid_list = []
    valid_list = []
    current_index = 0
    keycode = 255

    while keycode != setting.VALID_KEYS['exit']:
        # numeric keys
        if setting.NUM_DISPLAY == 1:
            if keycode == setting.VALID_KEYS['discard']:
                util.update_list(invalid_list, valid_list, current_index)
            elif keycode == setting.VALID_KEYS['reserve']:
                util.update_list(valid_list, invalid_list, current_index)
        elif keycode in setting.GRID_KEYS:
            for i in range(setting.NUM_DISPLAY):
                if current_index + i not in invalid_list and current_index + i not in valid_list:
                    valid_list.append(current_index + i)
            grid_index = keycode - 49 + current_index
            print('grid: {}'.format(grid_index))
            if grid_index in invalid_list:
                util.update_list(valid_list, invalid_list, grid_index)
            elif grid_index in valid_list:
                util.update_list(invalid_list, valid_list, grid_index)

        # operation keys
        if keycode == setting.VALID_KEYS['process']:
            util.process_verified_images(image_list, invalid_list, valid_list)
            if len(image_list) == 0:
                print('Done!')
                break
            else:
                current_index = 0
        elif keycode == setting.VALID_KEYS['prev']:
            current_index = max(0, current_index - setting.NUM_DISPLAY)
        elif keycode == setting.VALID_KEYS['next']:
            current_index = min(len(image_list) - 1, current_index + setting.NUM_DISPLAY)

        # refresh display
        images = util.read_images(image_list, setting.NUM_DISPLAY,
                                  current_index, invalid_list)
        grid = util.create_image_grid(images)
        util.valid_images(invalid_list, valid_list, current_index, setting.NUM_DISPLAY)
        keycode = util.show_image_grid(grid)

        # debug
        print('curr: {}'.format(current_index))
        print('invalid: {}'.format(invalid_list))
        print('valid: {}'.format(valid_list))

