
from mrcnn import utils
from PIL import Image
import os
import math
import random
import numpy as np
from DatasetUtils import *

class LeafsDataset(utils.Dataset):
    def __init__(self, folder_objects=None, folder_bgs=None, min_leaf=None, max_leaf=None):
        utils.Dataset.__init__(self)
        self.folder_objects = folder_objects
        self.folder_bgs = folder_bgs
        self.min_leaf = min_leaf
        self.max_leaf = max_leaf
        self.img2 = []
        self.bg = []

        if self.folder_objects is not None:
            self.init_objects()
        if self.folder_bgs is not None:
            self.init_bgs()    


    def init_objects(self):
        for root, _, files in os.walk(self.folder_objects):
            for filename in files:
                img = Image.open(os.path.join(root, filename))
                temp = img.copy()
                img.close()
                self.img2.append(temp)
        print("folder: " + folder_objects + " initialized")

    def init_bgs(self):
        for root, _, files in os.walk(self.folder_bgs):
            for filename in files:
                self.bg.append(Image.open(os.path.join(root, filename)))
        _, _, files_bgs = next(os.walk(self.folder_bgs))
        self.number_of_bgs = len(files_bgs)
        print("folder: " + folder_bgs + " initialized")

        _, _, files_objects = next(os.walk(self.folder_objects))
        self.number_of_leafs = len(files_objects)
    def load_shapes(self, count, height, width):
        # Add classes
        self.add_class("leaves", 1, "leaf")

        for i in range(count):
            print('Image', i, end='\r')
            bg_color, shapes = self.random_image(height, width)
            self.add_image("leaves", image_id=i, path=None, width=width, height=height, bg_color=bg_color,
                           shapes=shapes)

    def random_image(self, height, width):
        bg_color = np.array([random.randint(0, 255) for _ in range(3)])

        shapes = []
        boxes = []
        indexes = []
        N = random.randint(self.min_leaf, self.max_leaf)

        # AZ START INSERT
        prev_angle = random.randint(0, 360)
        min_x = math.floor(0.4 * width)
        max_x = math.floor(0.6 * width)
        min_y = math.floor(0.4 * height)
        max_y = math.floor(0.6 * height)
        x_location = random.randint(min_x, max_x)
        y_location = random.randint(min_y, max_y)
        # AZ END INSERT

        for _ in range(N):
            # AZ modified
            #shape, location, scale, angle, index = self.random_shape(height, width)
            shape, location, scale, angle, index = self.random_shape_centered(height, width, x_location, y_location, prev_angle)
            prev_angle = angle

            y, x, channels = np.asarray(self.img2[index]).shape
            shapes.append((shape, location, scale, angle, index))
            boxes.append([location[1], location[0], location[1] + y, location[0] + x])

        keep_ixs = utils.non_max_suppression(np.array(boxes), np.arange(N), 0.5)    # 0.3
        shapes = [s for i, s in enumerate(shapes) if i in keep_ixs]
        return bg_color, shapes

    def random_shape(self, height, width):
        shape = random.choice(["leaf"])
        #x_location = random.randint(0, width)
        #y_location = random.randint(0, height)
        x_location = random.randint(math.floor(0.25*width), math.floor(0.75*width))  # AZ get away from image borders
        y_location = random.randint(math.floor(0.25*height), math.floor(0.75*height))

        # x_scale = random.uniform(MIN_SCALE, MAX_SCALE) * random.uniform(MIN_ASPECT_RATIO, MAX_ASPECT_RATIO)
        # y_scale = random.uniform(MIN_SCALE, MAX_SCALE)
        x_scale = random.uniform(MIN_SCALE, MAX_SCALE)
        y_scale = x_scale * random.uniform(MIN_ASPECT_RATIO, MAX_ASPECT_RATIO)

        angle = random.randint(0, 360)
        index = random.randint(0, self.number_of_leafs - 1)

        return shape, (x_location, y_location), (x_scale, y_scale), angle, index


    def random_shape_centered(self, height, width, x_loc, y_loc, prev_angle):
        shape = random.choice(["leaf"])

        # x_scale = random.uniform(MIN_SCALE, MAX_SCALE) * random.uniform(MIN_ASPECT_RATIO, MAX_ASPECT_RATIO)
        # y_scale = random.uniform(MIN_SCALE, MAX_SCALE)
        x_scale = random.uniform(MIN_SCALE, MAX_SCALE)
        y_scale = x_scale * random.uniform(MIN_ASPECT_RATIO, MAX_ASPECT_RATIO)

        angle = (prev_angle + 70 + random.randint(-20, 20)) % 360   # (prev_angle + 120 + random.randint(-10, 10))
        #angle = random.randint(0, 360)

        x_location = math.floor(x_loc - 64 * math.sin(math.radians(angle))) # 64 is approx half size of leaf height in pixels
        y_location = math.floor(y_loc - 64 * math.cos(math.radians(angle))) # 64   120      80  100

        index = random.randint(0, self.number_of_leafs - 1)

        return shape, (x_location, y_location), (x_scale, y_scale), angle, index


    def load_image(self, image_id):
        info = self.image_info[image_id]

        index = random.randint(0, self.number_of_bgs - 1)

        y_max, x_max, channels = np.asarray(self.bg[index]).shape

        x = random.randint(0, x_max - TRAIN_IMAGE_SIZE)  # AZ 1024   512
        y = random.randint(0, y_max - TRAIN_IMAGE_SIZE)  # AZ 1024   512

        area = (x, y, x + TRAIN_IMAGE_SIZE, y + TRAIN_IMAGE_SIZE)  # AZ 1024  512
        image = self.bg[index].crop(area)

        for shape, location, scale, angle, index in info['shapes']:
            image = self.draw_leaf(image, shape, location, scale, angle, index)
        return np.array(image)

    def draw_leaf(self, image, shape, location, scale, angle, index):
        if shape == 'leaf':
            x_location, y_location = location
            x_scale, y_scale = scale
            image = add_image(image, self.img2[index], x_location, y_location, x_scale, y_scale, angle)
        return image

    def load_mask(self, image_id):
        info = self.image_info[image_id]
        shapes = info['shapes']
        count = len(shapes)

        mask = np.zeros([info['height'], info['width'], count], dtype=np.uint8)
        num_valid_masks = 0

        for i, (shape, location, scale, angle, index) in enumerate(info['shapes']):
            image = np.zeros([info['height'], info['width'], 3], dtype=np.uint8)
            #temp = image_to_mask(self.draw_leaf_without_transparency(image, shape, location, scale, angle, index))
            temp = self.draw_leaf_without_transparency(image, shape, location, scale, angle, index)
            temp = image_to_mask(temp)
            if np.amax(temp) == False:
                print("")
                print(" !!!!!!!!!!!!! EMPTY MASK")
                # mask[:, :, num_valid_masks] = temp[:, :]
                # num_valid_masks = num_valid_masks + 1
            mask[:, :, i] = temp[:, :]

        # if count != num_valid_masks:
        #     count = num_valid_masks
        #     mask = mask[:,:,0:num_valid_masks]

        occlusion = np.logical_not(mask[:, :, -1]).astype(np.uint8)
        for i in range(count - 2, -1, -1):
            mask[:, :, i] = mask[:, :, i] * occlusion
            occlusion = np.logical_and(occlusion, np.logical_not(mask[:, :, i]))
        class_ids = np.array([self.class_names.index(s[0]) for s in shapes])
        return mask.astype(np.bool), class_ids.astype(np.int32)

    def draw_leaf_without_transparency(self, image, shape, location, scale, angle, index):
        """Draws a shape from the given specs."""
        if shape == 'leaf':
            x_location, y_location = location
            x_scale, y_scale = scale
            image = add_image_without_transparency(image, np.array(self.img2[index]), x_location, y_location, x_scale,
                                                   y_scale, angle)
        return image

