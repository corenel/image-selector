import cv2
import util
import setting

if __name__ == '__main__':
    image_list = util.get_image_list(setting.IMAGE_DIR)
    images = util.read_images(image_list, 6)
    grid = util.create_image_grid(images)
    util.show_image_grid(grid)
