from PIL import Image
import cv2
import numpy as np
import urllib.request


def image_sending(img_url, human_list=None):
    # print(img_url)    
    model = 'img_proc/face/opencv_face_detector_uint8.pb'
    config = 'img_proc/face/opencv_face_detector.pbtxt'

    human = []
    face_list = []
    net = cv2.dnn.readNet(model, config)

    if net.empty():
        print('Net open failed!')
        exit()

    opener = urllib.request.URLopener()
    url_response = opener.open(img_url)   
    img_array = np.array(bytearray(url_response.read()), dtype=np.uint8) 
    image = cv2.imdecode(img_array, -1)
    # frame = cv2.imread(img)
    # frame = cv2.flip(img_array,1)
    frame = image

    blob = cv2.dnn.blobFromImage(frame, 1, (300, 300), (104, 177, 123))
    net.setInput(blob)
    detect = net.forward()

    detect = detect[0, 0, :, :]
    (h, w) = frame.shape[:2]

    for i in range(detect.shape[0]):
        confidence = detect[i, 2]
        if confidence < 0.5:
            continue

        x1 = int(detect[i, 3] * w)
        y1 = int(detect[i, 4] * h)
        x2 = int(detect[i, 5] * w)
        y2 = int(detect[i, 6] * h)
        human.append([x1,y1,x2,y2])
        # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0))
        face_img = frame[y1:y2, x1:x2]
        face_list.append(face_img)
        label = ""
        cv2.putText(frame, label, (x1, y1 - 1), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)

    if human_list is None:
        return face_list
    elif not human_list:
        return frame
    else:
        for i in range(len(human)):
            if i in human_list:   
                face_img = frame[human[i][1]:human[i][3], human[i][0]:human[i][2]]  # 탐지된 얼굴 이미지 crop        
                face_img = cv2.resize(face_img, ((human[i][2]-human[i][0])//15, (human[i][3]-human[i][1])//15))  # 축소
                face_img = cv2.resize(face_img, (human[i][2]-human[i][0], human[i][3]-human[i][1]), interpolation=cv2.INTER_AREA)  # 확대        
                frame[human[i][1]:human[i][3], human[i][0]:human[i][2]] = face_img  # 탐지된 얼굴 영역 모자이크 처리
        return Image.fromarray(frame)
    
    
# plt.imshow(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB),cmap='gray')
# plt.xticks([]), plt.yticks([]) 
# plt.show()

