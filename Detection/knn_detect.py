# import the necessary packages
from sklearn.neighbors import KNeighborsClassifier
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import argparse
import imutils
import cv2
import os
import joblib

#-----------------
#testing the model
#-----------------
fixed_size = tuple((800,800))
result = []
pos=0;

def loadModel(boundingModelPath, backgroundModelPath):
    boundingModel = joblib.load(boundingModelPath)
    backgroundModel = joblib.load(backgroundModelPath)

    return boundingModel, backgroundModel

def extract_color_histogram(image, bins=(8, 8, 8)):
	# extract a 3D color histogram from the HSV color space using
	# the supplied number of `bins` per channel
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	hist = cv2.calcHist([hsv], [0, 1, 2], None, bins,
		[0, 180, 0, 256, 0, 256])
	# handle normalizing the histogram if we are using OpenCV 2.4.X
	if imutils.is_cv2():
		hist = cv2.normalize(hist)
	# otherwise, perform "in place" normalization in OpenCV 3 (I
	# personally hate the way this is done
	else:
		cv2.normalize(hist, hist)
	# return the flattened histogram as the feature vector
	return hist.flatten()

def orb_algorithm(image):
    # extract a keypoints feature using orb algorithm
    orb = cv2.ORB_create()
    img= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #keypoints
    kp = orb.detect(img,None)
    kp, des = orb.compute(img, kp)
    pts=cv2.KeyPoint_convert(kp)
    # return the keypoints as the feature vector
    return des if des is not None else np.array([]).reshape(0,128)
    
def objectDetection(detectionModel, img, fixed_size):
    img2= cv2.resize(img,fixed_size)
    
    #-------------------
    #create bounding box
    #-------------------
    
    #find the width and height of the image
    imgwidth=img.shape[0]
    imgheight=img.shape[1]
    
    #grid initialization
    y1,x1=0,0
    M=imgwidth//10
    N=imgheight//10
    i=1
    
    #bounding box initialization
    ymin,ymax,xmin,xmax=imgheight,0,imgwidth,0
    
    for x in range(0,imgwidth,M):
        for y in range(0, imgheight, N):
            #split the image into grids
            x1 = x + M
            y1 = y + N
            tiles = img[x:x1,y:y1]
            
            
            #print(i)
            #feature extraction
            features = []
            
            hist = extract_color_histogram(tiles)
            features.append(hist)
            features = np.array(features)
    
    
            #predict label of test image
            prediction = detectionModel.predict(features)
            
            if prediction == 'object':
                if xmin>x:
                    xmin=x
                if xmax<x1:
                    xmax=x1
                if ymin>y:
                    ymin=y
                if ymax<y1:
                    ymax=y1
            i=i+1

    print(xmin, ";", xmax)
    ROI = img[xmin:xmax,ymin:ymax]
    if ROI.any():
        h = xmax-xmin
        w = ymax-ymin
        
        features_box = []
        
        #feature extraction
        hist = extract_color_histogram(ROI)
        features_box.append(hist)
        features_box = np.array(features_box)
        return [xmin,ymin,h,w], features_box
    else:
        return None, None
    
    #End Object Detection

def objectClassification(classificationModel, features_box):
    prediction = classificationModel.predict(features_box)
    label = 1
    if prediction[0] == 'small':
        label = 0

    return label

def detectAndClassified(imgPath, detectionModel, classificationModel):
    img = imgPath
    coordinate, features_box = objectDetection(detectionModel, img, fixed_size)
    if coordinate:
        result = objectClassification(classificationModel, features_box)
        cv2.rectangle(img, (coordinate[0], coordinate[1]), (coordinate[0]+coordinate[3], coordinate[1]+coordinate[2]), (0, 255, 0), 2)
        if result == 0:
            label = 'small'
        else:
            label = 'big'
        img = cv2.putText(img, f'{label}', (coordinate[0], coordinate[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 1, cv2.LINE_AA)
    else:
        result = None
    return coordinate, result, img

# load the model of image localization from disk
if __name__ == "__main__":
    detectionModel, classificationModel = loadModel("background_global_colorhist_knn_model.sav","box_global_colorhist_knn_model.sav")
    result = detectAndClassified("big._0_11.jpg",detectionModel, classificationModel)
    print(result)
    #display the output image
    plt.imshow(cv2.cvtColor(result[2], cv2.COLOR_BGR2RGB))
    plt.show()

