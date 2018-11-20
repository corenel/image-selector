import os

# path
IMAGE_DIR = '/Volumes/Document/Datasets/glow/999-fid/2063-reconstruction'
IMAGE_EXT = ['.jpg', '.png']
OTHER_EXT = ['.xml']
VALID_IMAGE_DIR = os.path.join(IMAGE_DIR, 'valid')
INVALID_IMAGE_DIR = os.path.join(IMAGE_DIR, 'invalid')

# display
NUM_DISPLAY = 2
DSIPALY_SCALE = 1.0

# button
VALID_KEYS = {
    'prev': 104,  # h
    'next': 108,  # l
    'down': 106,  # j
    'up': 107,  # k
    'discard': 120,  # x
    'reserve': 99,  # c
    'process': 13,  # enter
    'exit': 27,  # esc
}
GRID_KEYS = [49 + i for i in range(NUM_DISPLAY)]
