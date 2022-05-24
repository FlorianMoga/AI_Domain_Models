import cv2
import pytesseract
from pytesseract import Output

from Model.Rectangle import Rectangle
import numpy as np

from sklearn.cluster import DBSCAN

import random

import matplotlib.pyplot as plt


def inside(coordinate, table):
    middleX, middleY = coordinate.get_middle()

    topX, topY = table.get_topLeft()
    botX, botY = table.get_bottomRight()

    return topX <= middleX <= botY and topY >= middleY >= botX

class Photo:
    def __init__(self, path):
        self.path = path
        self.image = cv2.imread(path)
        self.height, self.width, _ = self.image.shape

        self.clusters = []
        self.n_clusters = 0
        self.table = None
        self.coordinates = []

        self.change_ratio()

    def change_ratio(self):
        ratio = 1000 / self.width
        self.width, self.height = 1000, int(self.height * ratio)
        dim = (self.width, self.height)
        self.image = cv2.resize(self.image, dim, interpolation=cv2.INTER_AREA)

    def set_table(self, table_format):
        left_y = self.height - table_format[1]
        left_x = table_format[0]

        right_y = self.height - table_format[3]
        right_x = table_format[2]
        self.table =  Rectangle([left_x, left_y], [right_x, right_y])

    def in_table(self, rectangle):
        min_x, max_y = self.table.get_topLeft()
        max_x, min_y = self.table.get_bottomRight()
        return min_x <= rectangle.get_middle()[0] <= max_x and min_y <= self.height - rectangle.get_middle()[1] <= max_y

    def get_characters_middlepoint(self):
        boxes = pytesseract.image_to_boxes(self.image, config=r'--psm 11 --oem 3')

        for box in boxes.splitlines():
            box = box.split(" ")
            top_x, top_y, bot_x, bot_y = int(box[1]), self.height - int(box[2]), int(box[3]), self.height - int(box[4])

            rectangle = Rectangle([top_x, top_y], [bot_x, bot_y])

            if not self.in_table(rectangle):
                self.coordinates.append(rectangle)

        middle_coordinates = [[r.get_middle()[0], self.height - r.get_middle()[1]] for r in self.coordinates]

        return middle_coordinates

    def define_clusters(self):

        # fig, ax = plt.subplots(figsize=(18, 18))
        # plt.ylim([0, self.height])
        # plt.xlim([0, self.width])

        middle_coordinates = self.get_characters_middlepoint()

        db = DBSCAN(eps=50, min_samples=3).fit(middle_coordinates)
        labels = db.labels_
        self.n_clusters = len(set(labels))
        self.clusters = set(labels)

        if -1 in list(labels):
            noise = True
        else:
            noise = False

        # print(f"There are {n_clusters - int(noise)}")

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
            self.coordinates[i].set_cluster(clusters_coordinates[i])
            # plt.plot(middle_coordinates[i][0], middle_coordinates[i][1], marker="x", markersize=20, markeredgecolor=clusters_colors[i], markerfacecolor=clusters_colors[i])

        # plt.show()

    def get_rectangles_by_cluster(self, cluster_nr):
        rectangles = [rectangle for rectangle in self.coordinates if rectangle.get_cluster() == cluster_nr]
        return rectangles

    def change_rectangle_cluster(self, initial_cluster, new_cluster):
        [rectangle.set_cluster(new_cluster) for rectangle in self.coordinates if
         rectangle.get_cluster() == initial_cluster]

    def get_outer_rectangle(self, cluster):

        max_x, min_x, max_y, min_y = 0, self.width, 0, self.height

        for r in cluster:
            top_x, top_y = r.get_topLeft()
            bottom_x, bottom_y = r.get_bottomRight()

            if top_x < min_x:
                min_x = top_x

            if top_y > max_y:
                max_y = top_y

            if bottom_x > max_x:
                max_x = bottom_x

            if bottom_y < min_y:
                min_y = bottom_y

        rectangle = Rectangle([min_x, max_y], [max_x, min_y])
        rectangle.set_cluster(cluster[0].get_cluster())

        return rectangle

    def test_associable_clusters(self, cl1_rectangle, cl2_rectangle):
        cl1_minX, cl1_maxY = cl1_rectangle.get_topLeft()
        _, cl1_minY = cl1_rectangle.get_bottomRight()
        _, cl2_maxY = cl2_rectangle.get_topLeft()
        cl2_maxX, cl2_minY = cl2_rectangle.get_bottomRight()

        size_cl1 = self.get_rectangles_by_cluster(cl1_rectangle.get_cluster())
        size_cl2 = self.get_rectangles_by_cluster(cl2_rectangle.get_cluster())

        associated_outer_table = Rectangle([cl1_minX, cl1_maxY], [cl2_maxX, cl2_minY])

        cl12_coords = [1 for coordinate in self.coordinates if inside(coordinate, associated_outer_table)]

        if len(size_cl1) + len(size_cl2) != sum(cl12_coords):
            return False
        else:
            return abs(cl1_maxY - cl2_maxY) + abs(cl1_minY - cl2_minY) < 10

    def associable_clusters(self, outer_rectangles):
        for cl1 in outer_rectangles:
            for cl2 in outer_rectangles:
                if cl1.get_cluster() < cl2.get_cluster() and self.test_associable_clusters(cl1, cl2):
                    return cl1, cl2

    def associate_clusters(self):

        while True:
            outer_rectangles = []
            for cl_num in self.clusters:
                if cl_num != -1:
                    cluster = self.get_rectangles_by_cluster(cl_num)
                    cluster_rectangle = self.get_outer_rectangle(cluster)
                    outer_rectangles.append(cluster_rectangle)
                    '''#draws segments rectangles
                    imgage_to_be_drawn = cv2.rectangle(imgage_to_be_drawn, (cluster_rectangle[0], cluster_rectangle[1]), (cluster_rectangle[2], cluster_rectangle[3]), (0, 0, 0))  
                    #crops segments
                    some_segment = crop_segment(original_image, cluster_rectangle)
                    #extracts text from cropped segment
                    data = pytesseract.image_to_data(some_segment, config = r'--psm 6 --oem 3', output_type = Output.DICT)
                    some_text.append(data['text'])

                    """crop_img = imgage_to_be_drawn[y:y+h, x:x+w]
                    cv2.imshow("cropped", crop_img)
                    cv2.waitKey(0)"""

            imgage_to_be_drawn = cv2.rectangle(imgage_to_be_drawn, (608, 1073), (911, 1088), (0,128, 255))
        '''
            must_associate = self.associable_clusters(outer_rectangles)

            if must_associate == None:
                break

            cluster_merge1, cluster_merge2 = must_associate
            print(cluster_merge1, cluster_merge2)
            self.change_rectangle_cluster(cluster_merge2.get_cluster(), cluster_merge1.get_cluster())
            self.clusters.remove(cluster_merge2.get_cluster())
            self.n_clusters -= 1
        '''cv2.imshow("segments", imgage_to_be_drawn)
        cv2.waitKey(0)
        cv2.destroyAllWindows()'''

    def get_text_from_segments(self):
        text = []

        for cl_num in self.clusters:
            if cl_num != -1:
                cluster = self.get_rectangles_by_cluster(cl_num)
                cluster_rectangle = self.get_outer_rectangle(cluster)
                topX, topY = cluster_rectangle.get_topLeft()
                botX, botY = cluster_rectangle.get_bottomRight()
                cropped_segment = self.image[botY-1:topY+1, topX-1:botX+1]

                # extracts text from cropped segment
                data = pytesseract.image_to_string(cropped_segment, config=r'--psm 6 --oem 3' , output_type=Output.DICT)
                text.append(data['text'])

        return text


    def crop_segment(self, original_img, coordinates):
        crop_img = original_img[coordinates[1]:coordinates[3], coordinates[0]:coordinates[2]]
        """cv2.imshow("cropped", crop_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()"""
        return crop_img

    def draw_all_segments(self):

        for cl_num in self.clusters:
            if cl_num != -1:
                cluster = self.get_rectangles_by_cluster(cl_num)
                cluster_rectangle = self.get_outer_rectangle(cluster)
                topX, topY = cluster_rectangle.get_topLeft()
                botX, botY = cluster_rectangle.get_bottomRight()
                self.image = cv2.rectangle(self.image, [topX, topY], [botX, botY], (0, 0, 0))
        self.show_img()

    def show_img(self):
        cv2.imshow("image", self.image)
        cv2.waitKey(0)