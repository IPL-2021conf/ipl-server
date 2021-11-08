import pathlib
from PIL import Image
import cv2
import numpy as np
import urllib.request
import time
import math
import copy

from img_proc.models import VdoProcModel
from django.core.files.base import File

def image_sending(img_url, human_list=None):
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
    frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    blob = cv2.dnn.blobFromImage(frame, 1, (300, 300), (104, 177, 123))
    net.setInput(blob)
    detect = net.forward()

    detect = detect[0, 0, :, :]
    (h, w) = frame.shape[:2]

    for i in range(detect.shape[0]):
        confidence = detect[i, 2]
        if confidence < 0.3:
            continue

        x1 = int(detect[i, 3] * w)
        y1 = int(detect[i, 4] * h)
        x2 = int(detect[i, 5] * w)
        y2 = int(detect[i, 6] * h)
        human.append([x1,y1,x2,y2])
        # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0))
        face_img = frame[y1:y2, x1:x2]
        face_list.append(face_img)

    if human_list is None:
        return face_list

    elif not human_list:
        return frame
    else:
        for i in range(len(human)):
            if i in human_list:   
                rate = int((human[i][2]-human[i][0] + human[i][3]-human[i][1]) /25)
                # -> 탐지된 객체의 크기의 가로 길이와 세로 길이를 합한 값을 사용해서 비율을 구함
                # 25로 나누는게 제일 적당했음..
                face_img = frame[human[i][1]:human[i][3], human[i][0]:human[i][2]]  # 탐지된 얼굴 이미지 crop
                face_img = cv2.resize(face_img, ((human[i][2]-human[i][0])//rate, (human[i][3]-human[i][1])//rate))  # rate 만큼 축소
                face_img = cv2.resize(face_img, (human[i][2]-human[i][0], human[i][3]-human[i][1]), interpolation=cv2.INTER_AREA)  # 확대
                frame[human[i][1]:human[i][3], human[i][0]:human[i][2]] = face_img  # 탐지된 얼굴 영역 모자이크 처리
        return Image.fromarray(frame)

def video_sending(video_url, human_list = None, people_list=None): # 동영상 처리
    model = 'img_proc/face/opencv_face_detector_uint8.pb'
    config = 'img_proc/face/opencv_face_detector.pbtxt'    

    cap = cv2.VideoCapture(video_url)
    if not cap.isOpened():
        print('Camera open failed!')
        exit()

    net = cv2.dnn.readNet(model, config)

    if net.empty():
        print('Net open failed!')
        exit()

    people = []  # 탐지된 객체중 사람의 위치를 저장
    mPeople_list = []
    face_list = [] # 최종적으로 서버로 보낼 얼굴 리스트

    fourcc = cv2.VideoWriter_fourcc(*'DIVX') # 영상 촬영
    out = cv2.VideoWriter('./img_proc/face/output.mp4', fourcc, 30.0, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    # output.avi = 모자이크 처리 된 영상

    f = 1
       
    if human_list is None:
        while True:
            _, frame = cap.read()
            if frame is None:
                break

            blob = cv2.dnn.blobFromImage(frame, 1, (300, 300), (104, 177, 123))
            net.setInput(blob)
            detect = net.forward()

            detect = detect[0, 0, :, :]
            (h, w) = frame.shape[:2]

            for i in range(detect.shape[0]):

                ok = 1  # 새로운 좌표를 집어 넣을까 말까 확인 변수(default: 참)

                confidence = detect[i, 2]
                if confidence < 0.3:
                    break

                x1 = int(detect[i, 3] * w)
                y1 = int(detect[i, 4] * h)
                x2 = int(detect[i, 5] * w)
                y2 = int(detect[i, 6] * h)

                for idx in range(len(people)):  # 왼쪽 위 좌표와 오른쪽 아래 좌표를 확인하기 위해 루프를 반복
                    if math.sqrt((people[idx][0] - x1) ** 2 + (people[idx][1] - y1) ** 2) < 110 or \
                            math.sqrt(
                                (people[idx][2] - x2) ** 2 + (people[idx][3] - y2) ** 2) < 110:  # 만약 리스트 안에 가까운 좌표가 이미 있다면
                        people[idx][0] = x1
                        people[idx][1] = y1
                        people[idx][2] = x2
                        people[idx][3] = y2

                        ok = 0  # ok 값 거짓으로 설정
                        break  # 갱신 후 루프를 종료
                
                if ok == 1:  # 만약 ok가 참이면 새로운 사람이 등장한 것이기 때문에 해당 좌표를 리스트에 집어 넣음
                    people.append([x1, y1, x2, y2, f]) # 새로운 사람을 리스트에 추가
                    mPeople_list.append([x1,y1,x2,y2,f])
                    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                    face_list.append(frame[y1:y2, x1:x2].copy()) # 새로운 사람이 추가 됐으므로 새로운 사람의 첫 프레임의 이미지를 face_list에 추가
                    print('added')

            f+=1  
  
        return face_list, mPeople_list#반환
    
    else:
        f = 1

        people_mosaic = [] # 얘를 사용해서 모자이크를 실행
        c=[]

        people_mosaic_del = [] # 사람이 사라지면 모자이크가 삭제되게 하는데 이용되는 리스트
        remove = [] # 삭제할 위치를 담고 있는 리스트

        old_time = time.time() # 시간 측정 시작

        while True:
            _, frame = cap.read()
            if frame is None:
                break

            blob = cv2.dnn.blobFromImage(frame, 1, (300, 300), (104, 177, 123))
            net.setInput(blob)
            detect = net.forward()

            detect = detect[0, 0, :, :]
            (h, w) = frame.shape[:2]

            for i in range(detect.shape[0]):

                ok = 1  # 새로운 좌표를 집어 넣을까 말까 확인 변수(default: 참)

                confidence = detect[i, 2]
                if confidence < 0.3:
                    break

                x1 = int(detect[i, 3] * w)
                y1 = int(detect[i, 4] * h)
                x2 = int(detect[i, 5] * w)
                y2 = int(detect[i, 6] * h)

                if time.time() - old_time>0.5:    # 이 부분은 사라진 사람의 모자이크를 삭제하는 부분입니다..
                    for i in range(len(people_mosaic)):
                        if people_mosaic[i] == people_mosaic_del[i]:
                            remove.append(people_mosaic[i].copy())

                    for i in range(len(remove)):
                        people_mosaic.remove(remove[i])

                    old_time = time.time()
                    people_mosaic_del.clear()
                    for i in range(len(people_mosaic)):
                        people_mosaic_del.append(people_mosaic[i].copy())
                    remove.clear()

                for idx in range(len(people_mosaic)):  # 왼쪽 위 좌표와 오른쪽 아래 좌표를 확인하기 위해 루프를 반복
                    if people_mosaic[idx] == [0,0,0,0,0]:
                        continue
                    if math.sqrt((people_mosaic[idx][0] - x1) ** 2 + (people_mosaic[idx][1] - y1) ** 2) < 110 or \
                        math.sqrt((people_mosaic[idx][2] - x2) ** 2 + (people_mosaic[idx][3] - y2) ** 2) < 110 :  # 만약 리스트 안에 가까운 좌표가 이미 있다면
                        people_mosaic[idx][0] = x1   # 해당 좌표 값을 갱신
                        people_mosaic[idx][1] = y1
                        people_mosaic[idx][2] = x2
                        people_mosaic[idx][3] = y2
                        ok = 0  # ok 값 거짓으로 설정
                        break  # 갱신 후 루프를 종료

                if ok == 1:  # 만약 ok가 참이면 새로운 사람이 등장한 것이기 때문에 해당 좌표를 리스트에 집어 넣음
                    people_mosaic.append([x1, y1, x2, y2, f]) # 새로운 사람을 리스트에 추가
                    people_mosaic_del.append([x1,y1,x2,y2,f]) # 인덱스 에러 방지를 위해 여기에도 추가

                
                for i in range(len(people_mosaic)):
                    if i in human_list and people_mosaic[i] != [0,0,0,0,0]:
                        if people_list[i] == people_mosaic[i]:
                            # print("i: " + str(i))
                            c.append(i)
                            c = list(dict.fromkeys(c))
                print(c)     
                for i in range(len(people_mosaic)):
                    if i in c and people_mosaic[i] != [0,0,0,0,0]:
                        rate = int((people_mosaic[i][2] - people_mosaic[i][0] + people_mosaic[i][3] - people_mosaic[i][1]) / 25)
                        face_img = frame[people_mosaic[i][1]:people_mosaic[i][3],people_mosaic[i][0]:people_mosaic[i][2]]  # 탐지된 얼굴 이미지 crop
                        face_img = cv2.resize(face_img, ((people_mosaic[i][2] - people_mosaic[i][0]) // rate, (people_mosaic[i][3] - people_mosaic[i][1]) // rate))  # 축소
                        face_img = cv2.resize(face_img, (people_mosaic[i][2] - people_mosaic[i][0], people_mosaic[i][3] - people_mosaic[i][1]), interpolation=cv2.INTER_AREA)  # 확대
                        frame[people_mosaic[i][1]:people_mosaic[i][3],
                        people_mosaic[i][0]:people_mosaic[i][2]] = face_img  # 탐지된 얼굴 영역 모자이크 처리
            f += 1


            out.write(frame)

        out.release()

        vdo_str = pathlib.Path(video_url)
        vdo_name = vdo_str.name.split('.')[0]
        video = File(open('./img_proc/face/output.mp4','rb'), vdo_name+'msc'+'.mp4')
        video_obj = VdoProcModel.objects.create(video = video)
        print('https://bucket-for-ipl.s3.amazonaws.com/'+str(video_obj.video))
        return 'https://bucket-for-ipl.s3.amazonaws.com/'+str(video_obj.video)