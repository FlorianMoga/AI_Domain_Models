import cv2
import pytesseract
from pytesseract import Output
from .Rectangle import Rectangle
from sklearn.cluster import DBSCAN
import torch
import random

import matplotlib.pyplot as plt


def inside(coordinate, table):
    middleX, middleY = coordinate.get_middle()

    topX, topY = table.get_topLeft()
    botX, botY = table.get_bottomRight()

    return topX <= middleX <= botX and topY >= middleY >= botY


class Photo:
    def __init__(self, path):
        self.path = path
        self.image = cv2.imread(path)
        self.image_copy = None
        self.height, self.width, _ = self.image.shape
        self.clusters = []
        self.n_clusters = 0
        self.table = None
        self.coordinates = []
        self.logo_coordinates = []
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=r'C:\Users\andre\Desktop\gep\AI_Domain_Models\backend\extract_text\Weights\best.pt',
                                    force_reload=True)

        self.change_ratio()
        self.set_logo_coords()

    def change_ratio(self):
        ratio = 1000 / self.width
        self.width, self.height = 1000, int(self.height * ratio)
        dim = (self.width, self.height)
        self.image = cv2.resize(self.image, dim, interpolation=cv2.INTER_AREA)
        self.image_copy = self.image.copy()

    def set_logo_coords(self):
        results = self.model(self.image, size=640)
        print(results)
        coords = results.xyxyn[0][:, :-1]

        for coord in coords:
            # if coord[4] >= 0.7:
            x1, y1, x2, y2 = int(coord[0] * self.width), int(coord[1] * self.height), int(coord[2] * self.width), \
                             int(coord[3] * self.height)
            self.logo_coordinates.append([x1, y1, x2, y2])

            self.image_copy = cv2.rectangle(self.image_copy, [x1, y1], [x2, y2], (0, 0, 0))
            self.image_copy = cv2.putText(self.image_copy, f'Logo {str(int(coord[4] * 100))}%', (x1, y1 - 3),
                                          cv2.FONT_HERSHEY_SIMPLEX,
                                          1, (0, 0, 0), 1, cv2.LINE_AA)

        print(f"Logo Coordinates : {self.logo_coordinates}")

    def set_table(self, table_format):
        left_y = self.height - table_format[1]
        left_x = table_format[0]

        right_y = self.height - table_format[3]
        right_x = table_format[2]
        self.table = Rectangle([left_x, left_y], [right_x, right_y])

    def in_table(self, rectangle):
        if self.table is None:
            return False
        min_x, max_y = self.table.get_topLeft()
        max_x, min_y = self.table.get_bottomRight()
        return min_x <= rectangle.get_middle()[0] <= max_x and min_y <= self.height - rectangle.get_middle()[1] <= max_y

    def in_logo(self, rectangle):
        if not self.logo_coordinates:
            return False
        for logo in self.logo_coordinates:
            min_x, max_y, max_x, min_y = logo
            max_y = self.height - max_y
            min_y = self.height - min_y

            if min_x <= rectangle.get_middle()[0] <= max_x and \
                    min_y <= self.height - rectangle.get_middle()[1] <= max_y:
                return True
        return False

    def get_characters_middlepoint(self):
        boxes = pytesseract.image_to_boxes(self.image, config=r'--psm 11 --oem 3')
        table_is_present = True

        if self.table is None:
            table_is_present = False

        for box in boxes.splitlines():
            box = box.split(" ")
            top_x, top_y, bot_x, bot_y = int(box[1]), self.height - int(box[2]), int(box[3]), self.height - int(box[4])

            rectangle = Rectangle([top_x, top_y], [bot_x, bot_y])

            if not table_is_present and self.logo_coordinates == []:
                self.coordinates.append(rectangle)
            elif not self.in_table(rectangle) and not self.in_logo(rectangle):
                self.coordinates.append(rectangle)

        middle_coordinates = [[r.get_middle()[0], self.height - r.get_middle()[1]] for r in self.coordinates]

        # image_to_be_drawn = self.image.copy()
        # for coord in self.coordinates:
        #     min_x, max_y = coord.get_topLeft()
        #     max_x, min_y = coord.get_bottomRight()
        #     image_to_be_drawn = cv2.rectangle(self.image, (min_x, max_y), (max_x, min_y), (0, 0, 255))
        #
        # cv2.imshow("middle coordinates", image_to_be_drawn)

        return middle_coordinates

    def define_clusters(self):

        # fig, ax = plt.subplots(figsize=(18, 18))
        # plt.ylim([0, self.height])
        # plt.xlim([0, self.width])

        middle_coordinates = self.get_characters_middlepoint()
        print(middle_coordinates)

        cv2.imshow("image", self.image)
        cv2.waitKey(0)
        db = DBSCAN(eps=40, min_samples=3).fit(middle_coordinates)
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

        if noise:
            colors.pop()
            colors.append([0, 0, 0])

        clusters_colors = []
        clusters_coordinates = []
        for i in range(len(labels)):
            clusters_coordinates.append(labels[i])
            clusters_colors.append(colors[labels[i]])

        for i in range(len(middle_coordinates)):
            self.coordinates[i].set_cluster(clusters_coordinates[i])
        #     plt.plot(middle_coordinates[i][0], middle_coordinates[i][1], marker="x", markersize=20,
        #              markeredgecolor=clusters_colors[i], markerfacecolor=clusters_colors[i])
        #
        # plt.savefig('coordinate clustered.png')

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
        cl1_maxX, cl1_minY = cl1_rectangle.get_bottomRight()
        cl2_minX, cl2_maxY = cl2_rectangle.get_topLeft()
        cl2_maxX, cl2_minY = cl2_rectangle.get_bottomRight()

        if abs(cl1_maxY - cl2_maxY) + abs(cl1_minY - cl2_minY) >= 15:
            return False
        else:
            size_cl1 = self.get_rectangles_by_cluster(cl1_rectangle.get_cluster())
            size_cl2 = self.get_rectangles_by_cluster(cl2_rectangle.get_cluster())

            associated_outer_table = Rectangle([min(cl1_minX, cl2_minX), max(cl1_maxY, cl2_maxY)],
                                               [max(cl1_maxX, cl2_maxX), min(cl1_minY, cl2_minY)])

            cl12_coords = [1 for coordinate in self.coordinates if inside(coordinate, associated_outer_table)]

            if len(size_cl1) + len(size_cl2) != sum(cl12_coords):
                return False

            return True

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

                    # draws segments rectangles
                    # min_x, max_y = cluster_rectangle.get_topLeft()
                    # max_x, min_y = cluster_rectangle.get_bottomRight()
                    # image_to_be_drawn = cv2.rectangle(self.image, (min_x, max_y), (max_x, min_y), (0, 0, 0))
                    # crops segments
                    # some_segment = crop_segment(original_image, cluster_rectangle)
                    # extracts text from cropped segment
                    # data = pytesseract.image_to_data(some_segment, config = r'--psm 6 --oem 3', output_type = Output.DICT)
                    # some_text.append(data['text'])

                    # crop_img = imgage_to_be_drawn[y:y+h, x:x+w]
                    # cv2.imshow("cropped", crop_img)
                    # cv2.waitKey(0)

            # image_to_be_drawn = cv2.rectangle(self.image, (608, 1073), (911, 1088), (0,128, 255))

            must_associate = self.associable_clusters(outer_rectangles)

            if must_associate is None:
                break

            cluster_merge1, cluster_merge2 = must_associate
            print(f"Associable clusters {cluster_merge1} {cluster_merge2}")
            self.change_rectangle_cluster(cluster_merge2.get_cluster(), cluster_merge1.get_cluster())
            self.clusters.remove(cluster_merge2.get_cluster())
            self.n_clusters -= 1

        # cv2.imshow("segments", image_to_be_drawn)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    def get_text_from_segments(self):
        text = []

        for cl_num in self.clusters:
            if cl_num != -1:
                cluster = self.get_rectangles_by_cluster(cl_num)
                cluster_rectangle = self.get_outer_rectangle(cluster)
                topX, topY = cluster_rectangle.get_topLeft()
                botX, botY = cluster_rectangle.get_bottomRight()

                if botY != 0:
                    botY -= 1
                if topX != 0:
                    topY -= 1
                if botX != self.width:
                    botX += 1
                if topY != self.height:
                    topY += 1

                cropped_segment = self.image[botY:topY, topX:botX]
                # print(topX, botX, topY, botY)

                # extracts text from cropped segment
                data = pytesseract.image_to_string(cropped_segment, config=r'--psm 6 --oem 3', output_type=Output.DICT)
                text.append(data['text'])

        text_file = open(f'C:/Users/andre/Desktop/gep/AI_Domain_Models/backend/extract_text/TXT/{self.path.split("/")[-1]}.txt', "w")
        for segment in text:
            text_file.write(segment)
            text_file.write('---')
            text_file.write('\n')
        text_file.close()

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
                self.image_copy = cv2.rectangle(self.image_copy, [topX, topY], [botX, botY], (0, 0, 0))

        # cv2.imwrite('Clustered_Invoices/clustered_image.jpg', self.image)

    def show_img(self):
        cv2.imshow("image", self.image)
        cv2.waitKey(0)

    def save_processed(self):
        cv2.imwrite(f'C:/Users/andre/Desktop/gep/AI_Domain_Models/backend/extract_text/Clustered_Invoices/{self.path.split("/")[-1]}.jpg', self.image_copy)
