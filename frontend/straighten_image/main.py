import sys

import cv2
import numpy as np


# read image
def cyclic_intersection_pts(pts):
    """
    Sorts 4 points in clockwise direction with the first point been closest to 0,0
    Assumption:
        There are exactly 4 points in the input and
        from a rectangle which is not very distorted
    """
    if pts.shape[0] != 4:
        return None

    perechea = 0
    minn = float('inf')

    for i in range(1, len(pts)):
        if (abs(pts[i][0][1] - pts[0][0][1]) < minn):
            minn = abs(pts[i][0][1] - pts[0][0][1])
            perechea = i

    perechea1 = [0, i]
    perechea2 = [x for x in range(1, 4) if x != i]

    # facem distantele dintre perechi in ele si dintre ele
    # print(pts[perechea1[0]].flatten()[0],' ',pts[perechea1[1]].flatten()[1])
    # print(pts[perechea1[0]].flatten(),' ',pts[perechea2[0]].flatten())

    dist_intre = np.sqrt(((pts[perechea1[0]].flatten()[0] - pts[perechea1[1]].flatten()[0]) ** 2) + (
                (pts[perechea1[0]].flatten()[1] - pts[perechea1[1]].flatten()[1]) ** 2))
    dist_dintre = np.sqrt(((pts[perechea1[0]].flatten()[0] - pts[perechea2[0]].flatten()[0]) ** 2) + (
                (pts[perechea1[0]].flatten()[1] - pts[perechea2[0]].flatten()[1]) ** 2))

    # print("dist_intre: ", dist_intre)
    # print("dist_dintre: ", dist_dintre)
    # print("perechea 1: ", pts[perechea1[0]], ' ', pts[perechea1[1]])
    # print("perechea 2: ", pts[perechea2[0]], ' ', pts[perechea2[1]])

    cyclic_pts = [[], [], [], []]  # sus stg, sus dreapta, jos dreapta, jos stg
    if dist_intre > dist_dintre:
        # daca distanta intre e mai mare, avem fiecare pereche de sus-jos
        if pts[perechea1[0]].flatten()[0] < pts[perechea2[0]].flatten()[0]:
            # perechea 2 dreapta, perechea 1 stanga
            tmp = perechea1
            perechea1 = perechea2
            perechea2 = tmp

        # perechea 1 dreapta, perechea 2 stanga
        # perechea 1: [[906  61]][[914 1210]] - dreapta jos, sus

        # perechea 2: [[105  79]][[110 1198]] - stanga
        if pts[perechea2[0]].flatten()[1] < pts[perechea2[1]].flatten()[1]:
            cyclic_pts[0] = (pts[perechea2[1]].flatten())
            cyclic_pts[3] = (pts[perechea2[0]].flatten())
        else:
            cyclic_pts[3] = (pts[perechea2[1]].flatten())
            cyclic_pts[0] = (pts[perechea2[0]].flatten())

        if pts[perechea1[0]].flatten()[1] < pts[perechea1[1]].flatten()[1]:
            cyclic_pts[1] = (pts[perechea1[1]].flatten())
            cyclic_pts[2] = (pts[perechea1[0]].flatten())
        else:
            cyclic_pts[2] = (pts[perechea1[1]].flatten())
            cyclic_pts[1] = (pts[perechea1[0]].flatten())

    else:  # sus stg, sus dreapta, jos dreapta, jos stg
        # daca distanta dintre e mai mare, avem fiecare pereche st-dr
        # perechea 1: [[556 1046]][[3031 1068]] - jos
        # perechea 2: [[446 4623]][[3077 4668]] - sus
        if pts[perechea1[0]].flatten()[1] > pts[perechea2[0]].flatten()[1]:
            tmp = perechea1
            perechea1 = perechea2
            perechea2 = tmp

        # perechea 1 e jos, perechea 2 e sus
        if pts[perechea1[0]].flatten()[0] < pts[perechea1[1]].flatten()[0]:
            # perechea 1: stanga jos, dreapta jos
            cyclic_pts[3] = pts[perechea1[0]].flatten()
            cyclic_pts[2] = pts[perechea1[1]].flatten()
        else:
            # perechea 1: dreapta jos, stanga jos
            cyclic_pts[2] = pts[perechea1[0]].flatten()
            cyclic_pts[3] = pts[perechea1[1]].flatten()

        if pts[perechea2[0]].flatten()[0] < pts[perechea2[1]].flatten()[0]:
            # perechea 2: stanga sus, dreapta sus
            cyclic_pts[0] = pts[perechea2[0]].flatten()
            cyclic_pts[1] = pts[perechea2[1]].flatten()
        else:
            # perechea 2: dreapta sus, stanga sus
            cyclic_pts[1] = pts[perechea2[0]].flatten()
            cyclic_pts[0] = pts[perechea2[1]].flatten()

    return np.array(cyclic_pts)

def straighten_image(img):
    color = cv2.resize(img, (0, 0), fx=0.15, fy=0.15)

    # convert img to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # blur image
    blur = cv2.GaussianBlur(gray, (3, 3), 0)

    # do otsu threshold on gray image
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # apply morphology
    kernel = np.ones((7, 7), np.uint8)
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)

    # get largest contour
    contours = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    area_thresh = 0
    for c in contours:
        area = cv2.contourArea(c)
        if area > area_thresh:
            area_thresh = area
            big_contour = c

    # draw white filled largest contour on black just as a check to see it got the correct region
    page = np.zeros_like(img)
    cv2.drawContours(page, [big_contour], 0, (255, 255, 255), -1)

    # get perimeter and approximate a polygon
    peri = cv2.arcLength(big_contour, True)
    corners = cv2.approxPolyDP(big_contour, 0.04 * peri, True)

    # draw polygon on input image from detected corners
    polygon = img.copy()
    cv2.polylines(polygon, [corners], True, (0, 0, 255), 1, cv2.LINE_AA)
    # Alternate: cv2.drawContours(page,[corners],0,(0,0,255),1)

    # print the number of found corners and the corner coordinates
    # They seem to be listed counter-clockwise from the top most corner


    # Sort the points in cyclic order
    intersect_pts = cyclic_intersection_pts(corners)

    # out = img.copy()
    # for pts in intersect_pts:
    #     cv2.rectangle(out, (pts[0] - 1, pts[1] - 1), (pts[0] + 1, pts[1] + 1), (0, 0, 255), 2)
    # cv2.imwrite('resultImg/intersect_points.png', out)

    # 1-2 si 3-4
    width1 = np.sqrt(
        ((intersect_pts[0][0] - intersect_pts[1][0]) ** 2) + ((intersect_pts[0][1] - intersect_pts[1][1]) ** 2))
    width2 = np.sqrt(
        ((intersect_pts[2][0] - intersect_pts[3][0]) ** 2) + ((intersect_pts[2][1] - intersect_pts[3][1]) ** 2))
    maxWidth = max(int(width1), int(width2))

    # 1-3 si 2-4
    height1 = np.sqrt(
        ((intersect_pts[0][0] - intersect_pts[2][0]) ** 2) + ((intersect_pts[0][1] - intersect_pts[2][1]) ** 2))
    height2 = np.sqrt(
        ((intersect_pts[1][0] - intersect_pts[3][0]) ** 2) + ((intersect_pts[1][1] - intersect_pts[3][1]) ** 2))
    maxHeight = max(int(height1), int(height2))

    # print('maxWidth: ', maxWidth)
    # print('maxHeight: ', maxHeight)
    #
    # latime 1000
    # sus stg, sus dreapta, jos dreapta, jos stg
    output_pts = np.float32([ [0, maxHeight-1], [maxWidth-1, maxHeight-1], [maxWidth-1, 0], [0, 0]])
    intersect_pts = np.float32(intersect_pts)
    # print(intersect_pts)
    # Compute the perspective transform M
    M = cv2.getPerspectiveTransform(intersect_pts, output_pts)

    out = cv2.warpPerspective(img, M, (maxWidth, maxHeight), flags=cv2.INTER_LINEAR)
    # cv2.imwrite('resultImg/result.png', out)


    scale_percent = int(1000*100/maxWidth)
    width = int(out.shape[1] * scale_percent / 100)
    height = int(out.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(out, dim, interpolation = cv2.INTER_AREA)
    # cv2.imshow("segments", resized)
    # cv2.waitKey(0)

    return resized
