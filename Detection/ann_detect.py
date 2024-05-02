import cv2
import numpy as np
from elements.yolo import OBJ_DETECTION

obj_cls = ["small", "big"]
obj_col = list(np.random.rand(2, 3) * 255)

def loadModel():
    obj_det = OBJ_DETECTION('best.pt', obj_cls)
    return obj_det

def detect(img, model):
    coordinate =[]
    result = []
    objs = model.detect(img)
    for obj in objs:
        label = obj['label']
        score = obj['score']
        [(xmin, ymin), (xmax, ymax)] = obj['bbox']
        color = obj_col[obj_cls.index(label)]
        img = cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color, 2)
        img = cv2.putText(img, f'{label}', (xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 1, cv2.LINE_AA)
        width = xmax - xmin
        height = ymax - ymin
        coordinate.append([xmin, ymin, width, height])
        if label == 'small':
            result.append(0)
        elif label == 'big':
            result.append(1)

    return coordinate, result, img
        
