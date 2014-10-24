#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import cv2
import cv2.cv as cv

HAAR_CASCADE_PATH = "input/haarcascades/haarcascade_frontalface_alt.xml"

OUTPUT_PATH = 'output/'

def face_detect(img, framePosition, size):

    cascade = cv2.CascadeClassifier(HAAR_CASCADE_PATH)
    rects = cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=4, minSize=size, flags=cv.CV_HAAR_SCALE_IMAGE)
   
    cv2.imshow("movie", img)
    if len(rects) == 0:
        return [], []
    rects[:,2:] += rects[:,:2]
    face_position_list = []
    for rect in rects:
        face_position_list.append(rect)
    
    return face_position_list, rects


def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

def output_image(rects, img, file_name):
    show = img.copy()
    face_count = 0
    for x1, y1, x2, y2 in rects:
        face = img[y1:y2, x1:x2]
        cv2.rectangle(show, (x1-10, y1-10), (x2+5, y2+5), (127, 255, 0), 2) 
        cv2.imshow("detected", show)
        resize_face = cv2.resize(face, (150, 150), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite( file_name + '-' + str(face_count) + '.jpg', resize_face)
        face_count += 1
