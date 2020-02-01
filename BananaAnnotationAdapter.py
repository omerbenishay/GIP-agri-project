import json


class BananaAnnotationAdapter(object):
    def __init__(self, coco_file_path, n=None):
        with open(coco_file_path, 'r') as f:
            self.data = json.load(f)
        self.n = n
        self.category = 'leaf'
        self.generator = self._annotation_generator()

    def __iter__(self):
        return self

    def _annotation_generator(self):
        category_id = [category["id"] for category in self.data["categories"] if category["name"] == self.category][0]
        if category_id is None:
            return None
        count = 0
        for annotation in self.data["annotations"]:
            if self.n is not None and count == self.n:
                break
            # Discard objects with more than one polygon
            if len(annotation.get("segmentation")) != 1:
                continue
            # Discard objects of size 0
            if annotation["bbox"][2] < 1 or annotation["bbox"][3] < 1:
                continue
            if annotation.get("category_id") == category_id:
                count += 1
                yield annotation

    def __next__(self):
        return next(self.generator).get("segmentation")[0]

