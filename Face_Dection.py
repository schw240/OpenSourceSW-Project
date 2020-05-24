import cv2
%matplotlib inline 
from matplotlib import pyplot as plt
from PIL import Image
def detectFaceOpenCVDnn(net, frame):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (frameHeight, frameWidth), [104, 117, 123], False, False)

    net.setInput(blob)
    detections = net.forward()
    bboxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            bboxes.append([x1, y1, x2, y2])
            if not(x1<30 or y1<30 or x2>frameWidth-30 or y2>frameHeight-30):
              y1, y2 = y1-20, y2+20
              x1, x2 = x1-20, x2+20
            else:
              continue
            crop_img = frameOpencvDnn[y1:y2, x1:x2]
            crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB).astype("float32")
            cv2.imwrite("cropped"+str(i)+".jpg", crop_img)
            inp = np.array([gan.data_loader.get_img(crop_img)])
            old_img = gan.g_AB.predict([inp])
            new_img = revert_img(old_img[0], (y2-y1, x2-x1))
            new_img = cv2.cvtColor(new_img, cv2.COLOR_RGB2BGR).astype("float32")
            frameOpencvDnn[y1:y2, x1:x2] = new_img
            scipy.misc.imsave("after"+str(i)+".jpg", new_img)
    return frameOpencvDnn, bboxes
  
conf_threshold = 0.8
modelFile = "opencv_face_detector_uint8.pb"
configFile = "opencv_face_detector.pbtxt"
net = cv2.dnn.readNetFromTensorflow(modelFile, configFile)
frame = cv2.imread("addicted.jpg")
outOpencvDnn, bboxes = detectFaceOpenCVDnn(net,frame,0)
cv2.imwrite("addicted_after.jpg", outOpencvDnn)
