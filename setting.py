import os

# path
IMAGE_DIR = '/Volumes/Document/Datasets/Crypko-50'
IMAGE_EXT = ['.jpg', '.png']
SELECTED_IMAGE_DIR = os.path.join(IMAGE_DIR, 'selected')

# display
NUM_DISPLAY = 1

# button
VALID_KEYS = {
    'prev': 104,  # h
    'next': 108,  # l
    'discard': 120,  # x
    'reserve': 99,  # c
    'process': 13,  # enter
    'exit': 27,  # esc
}
