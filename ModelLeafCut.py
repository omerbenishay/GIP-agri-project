import numpy as np
from PIL import Image, ImageDraw
import json
import os 
from multiprocessing import Pool, cpu_count
import multiprocessing
# multiprocessing.set_start_method('spawn', True)
import time
import tqdm
from math import ceil

def cut(args):
    annotation_path = args.path
    limit = args.limit
    jobs = cut_jobs(annotation_path, "leaf", limit)
    start = time.time()
    jobs = list(jobs)
    total_jobs = len(jobs) if limit is None else min(limit, len(jobs))
    with Pool(cpu_count()) as pool:
        for _ in tqdm.tqdm(pool.imap_unordered(image_from_tuple, jobs), total=total_jobs):
            pass
    print("took {} seconds".format(time.time() - start))

def get_category_annotations(annotation_path, category_name, n=None):
    with open(annotation_path) as annotations_file:
        annotations = json.load(annotations_file)
        # get category id from category name
        category_id = [category["id"] for category in annotations["categories"] if category["name"] == category_name][0]
        if category_id is None:
            return None
        count = 0
        for annotation in annotations["annotations"]:
            if n is not None and count == n:
                break
            if len(annotation.get("segmentation")) != 1:
                continue
            if annotation.get("category_id") == category_id:
                count += 1
                yield annotation
            
def get_image_path(annotation_path, image_id):
    with open(annotation_path) as annotation_file:
        images = json.load(annotation_file).get("images")
        image_path = [image["path"] for image in images if image["id"] == image_id][0]
        return image_path

def image_from_tuple(tuple):
    return image_from_annotation(*tuple)

def image_from_annotation(leaf_annotation, image_path, suffix, save=True):
    
    image = None
    try:
        image = Image.open(image_path).convert("RGBA")
    except Exception as e:
        print("error occured while opening file {}".format(image_path))
        print(e)
    
    # Recreate bbox from polygon
    vertices = np.array(leaf_annotation["segmentation"][0]).reshape((-1,2)).transpose()
    x, y = tuple(   
            map( int, 
                ( min(vertices[0]), min(vertices[1]) )
            )
        )
    x_right, y_bottom = tuple(   
            map( lambda x: int(ceil(x)), 
                ( max(vertices[0]), max(vertices[1]) )
            )
        )
    
    # Keep right and bottom values inside picture borders
    x = max(0, x)
    y = max(0, y)
    x_right = min(x_right, image.size[0])
    y_bottom = min(y_bottom, image.size[1])

    # Create new cropped image
    new_image_array = np.asarray(image)[y:y_bottom, x:x_right, :3]

    # Create and apply mask from polygon
    mask_image = Image.new('L', image.size)
    ImageDraw.Draw(mask_image).polygon(leaf_annotation["segmentation"][0], fill=255, outline=0)
    mask_image_array = np.expand_dims(np.asarray(mask_image)[y:y_bottom, x:x_right], axis=2)
    new_image_array = np.concatenate((new_image_array, mask_image_array), axis=2)
    
    new_image = None
    try:
        new_image = Image.fromarray(new_image_array, "RGBA")
    except Exception as e:
        print("error occured while creating image from annotation id {}".format(leaf_annotation["id"]))
        return None

    if save:
        try:
            new_image.save("image_{}.png".format(suffix))
        except Exception as e:
            print("error occured while processing annotation id {}".format(leaf_annotation["id"]))
            return None

    return new_image

def cut_jobs(annotation_path, category='leaf', n=None):
    annotations = get_category_annotations(annotation_path, category, n)
    dir_path = os.path.dirname(annotation_path)
    for i, leaf_annotation in enumerate(annotations):
        image_relative_path = get_image_path(annotation_path, leaf_annotation["image_id"])
        image_path = os.path.join(dir_path, image_relative_path)
        yield (leaf_annotation, image_path, i)


if __name__ == "__main__":
    file_path = "/home/nomios/Documents/Projects/deep/cucumber/dataset/leaves/train/annotations.json"
    jobs = list(cut_jobs(file_path, "leaf", None))

    start = time.time()
    with Pool(cpu_count()) as pool:
        for _ in tqdm.tqdm(pool.imap_unordered(image_from_tuple, jobs), total=len(jobs)):
            pass
    print("took {} seconds".format(time.time() - start))