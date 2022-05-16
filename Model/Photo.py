import cv2
import pytesseract
from pytesseract import Output

from Model.Rectangle import Rectangle
import numpy as np

from sklearn.cluster import DBSCAN

import random

import matplotlib.pyplot as plt



class Photo:
    def __init__(self, path):
        self.path = path
        self.image = cv2.imread(path)
        self.height, self.width, _ = self.image.shape

        self.n_clusters = 0

        self.change_ratio()

    def change_ratio(self):
        ratio = 1000 / self.width
        self.width, self.height = 1000, int(self.height * ratio)
        dim = (self.width, self.height)
        self.image = cv2.resize(self.image, dim, interpolation = cv2.INTER_AREA)

    def get_characters_middlepoint(self):
        boxes = pytesseract.image_to_boxes(self.image, config = r'--psm 11 --oem 3')
        coordinates = []

        for box in boxes.splitlines():
            box = box.split(" ")
            top_x, top_y, bot_x, bot_y = int(box[1]), self.height - int(box[2]), int(box[3]), self.height - int(box[4])

            coordinates.append(Rectangle([top_x, top_y], [bot_x, bot_y]))

            #self.image = cv2.rectangle(self.image, (top_x, top_y), (bot_x, bot_y), (0, 0, 255))

        middle_coordinates = [[r.get_middle()[0], self.height - r.get_middle()[1]] for r in coordinates]

        return coordinates, middle_coordinates

    def define_clusters(self):

        #fig, ax = plt.subplots(figsize=(18, 18))
        #plt.ylim([0, self.height])
        #plt.xlim([0, self.width])

        coordinates, middle_coordinates = self.get_characters_middlepoint()

        db = DBSCAN(eps=50, min_samples=3).fit(middle_coordinates)
        labels = db.labels_
        self.n_clusters = len(set(labels))

        if -1 in list(labels):
            noise = True
        else:
            noise = False

        #print(f"There are {n_clusters - int(noise)}")

        color = lambda: [random.random(), random.random(), random.random()]
        colors = []

        for i in range(self.n_clusters):
            colors.append(color())

        if noise == True:
            colors.pop()
            colors.append([0, 0, 0])

        clusters_colors = []
        clusters_coordinates = []
        for i in range(len(labels)):
            clusters_colors.append(colors[labels[i]])
            clusters_coordinates.append(labels[i])

        for i in range(len(middle_coordinates)):
            coordinates[i].set_cluster(clusters_coordinates[i])
            #plt.plot(middle_coordinates[i][0], middle_coordinates[i][1], marker="x", markersize=20, markeredgecolor=clusters_colors[i], markerfacecolor=clusters_colors[i])

        #plt.show()
        return coordinates

    def get_rectangles_by_cluster(self, cluster_nr, coordinates):
        rectangles = [rectangle for rectangle in coordinates if rectangle.get_cluster() == cluster_nr]
        return rectangles

    def get_outer_rectangle(self, cluster):
        max_x, min_x, max_y, min_y = 0, self.width, 0, self.height

        for rectangle in cluster:
            top_x, top_y = rectangle.get_topLeft()
            bottom_x, bottom_y = rectangle.get_bottomRight()

            if top_x < min_x:
                min_x = top_x

            if top_y > max_y:
                max_y = top_y

            if bottom_x > max_x:
                max_x = bottom_x

            if bottom_y < min_y:
                min_y = bottom_y

        return [min_x, min_y, max_x, max_y]

    def crop_segment(self, original_img, coordinates):
        crop_img = original_img[coordinates[1]:coordinates[3], coordinates[0]:coordinates[2]]
        """cv2.imshow("cropped", crop_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()"""
        return crop_img

    def draw_all_segments(self, coordinates):
        original_img = Photo(self.path)

        for cl_num in range(self.n_clusters-1):
            if cl_num != -1:
                cluster = self.get_rectangles_by_cluster(cl_num, coordinates)
                cluster_rectangle = self.get_outer_rectangle(cluster)
                # draws segments rectangles
                original_img.image = cv2.rectangle(original_img.image, (cluster_rectangle[0], cluster_rectangle[1]),
                                                   (cluster_rectangle[2], cluster_rectangle[3]), (0, 0, 0))
                # crops segments
                some_segment = self.crop_segment(self.image, cluster_rectangle)
                # extracts text from cropped segment
                data = pytesseract.image_to_data(some_segment, config=r'--psm 6 --oem 3', output_type=Output.DICT)
                print(data['text'])
        original_img.show_img()

    def show_img(self):
        cv2.imshow("image", self.image)
        cv2.waitKey(0)