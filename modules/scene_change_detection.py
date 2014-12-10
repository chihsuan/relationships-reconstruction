#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import sys
import cv2
 
def scene_change_detection():
    if len(sys.argv) < 2:
        print "Error - file name must be specified as first argument."
        return
 
    cap = cv2.VideoCapture()
    cap.open(sys.argv[1])
 
    if not cap.isOpened():
        print "Fatal error - could not open video %s." % sys.argv[1]
        return
    else:
        print "Parsing video %s..." % sys.argv[1]
 
 
    # Allow the threshold to be passed as an optional second argument to the script.
    threshold = 15
    if len(sys.argv) > 2 and int(sys.argv[2]) > 0:
        threshold = int(sys.argv[2])
    print "Detecting scenes with threshold %d." % threshold
     
    last_mean = 0       # Mean pixel intensity of the *last* frame we processed.
         
    while True:
        (rv, im) = cap.read()   # im is a valid image if and only if rv is true
        if not rv:
            break
        frame_mean = im.mean()
     
        # Detect fade in from black.
        if frame_mean >= threshold and last_mean < threshold:
            print "Detected fade in at %dms (frame %d)." % (
                cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC),
                cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES) )
     
        # Detect fade out to black.
        elif frame_mean < threshold and last_mean >= threshold:
            print "Detected fade out at %dms (frame %d)." % (
                cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC),
                cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES) )
     
        last_mean = frame_mean     # Store current mean to compare in next iteration.

    cap.release()
 
if __name__ == "__main__":
    scene_change_detection()
