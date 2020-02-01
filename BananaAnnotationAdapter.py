import numpy as np
import json
import os


class BananaAnnotationAdapter(object):
    IMAGE_FORMATS = ['jpg', 'jpeg', 'png']

    def __init__(self, file_path, n=None):
        with open(file_path, 'r') as f:
            self.data = json.load(f)
        self.n = n
        self.dir_path = os.path.dirname(file_path)
        self.generator = self._cut_jobs()
        self.annotations = {}
        self._annotation_generate()
        self.index_to_leaf_key_lut = []

    def __iter__(self):
        return self

    def _cut_jobs(self):
        for i, (leaf_key, leaf_data) in enumerate(self.annotations.items()):
            image_relative_path = self._get_image_path(leaf_data["image"])
            image_path = os.path.join(self.dir_path, image_relative_path)
            # Save reference of index to original annotation to retrieve 'point' if needed
            self.index_to_leaf_key_lut.append(leaf_key)
            yield (leaf_data["polygon"], image_path, i)

    def get_point(self, index):
        """
        Get the point of a leaf if it exists in the annotation file
        :param index:   Index passed with the leaf annotation by the collection
        :return:        an array [x, y] with the location of the point if it exists
                        if points doesn't exists, returns None
        """
        return self.annotations[self.index_to_leaf_key_lut[index]].get("point", None)

    def _annotation_generate(self):
        for image_key, leaves_array in self.data.items():
            for leaf_data in leaves_array:
                leaf_id = leaf_data["_id"]
                if leaf_data["annotation_type"] == "polygon":
                    self.annotations[leaf_id] = {}
                    leaf_polygon_coords = [[ann['x'], ann['y']] for ann in leaf_data["annotations"]]
                    leaf_polygon = np.array(leaf_polygon_coords).reshape((-1,)).tolist()
                    self.annotations[leaf_id]["polygon"] = leaf_polygon
                # if leaf_data["annotation_type"] == "point":
                    # self.annotations[leaf_id]["point"] = [leaf_data["annotations"]["x"], leaf_data["annotations"]["y"]]
                    self.annotations[leaf_id]["image"] = leaf_data["frame_id"]

    def _get_image_path(self, image_id):
        file_list = os.listdir(self.dir_path)
        match = [file_name for file_name in file_list if file_name.startswith(str(image_id))
                 and file_name.split(".")[-1].lower() in self.IMAGE_FORMATS][0]
        return match

    def __next__(self):
        """
        Needs to be implemented in order to iterate through the annotations

        :return:    A tuple (leaf_annotation, image_path, i) where
                    leaf annotation is a list of coordinates [x,y,x,y,x,y,...]
                    image_path is a full or relative path to the image
                    i is a running index used for example to name the leaf picture
        """
        return next(self.generator)


if __name__ == "__main__":
    b = BananaAnnotationAdapter('/home/nomios/Documents/Projects/model-cmd/Phenomics_tst/tmp/task_30', 2)
    for image_data in b:
        print(image_data)
