from io import StringIO
import io
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile

from .models import ImgFaceModel, ImgProcModel
from .face import dnnface
import numpy as np
from PIL import Image
import os
import sys
# Create your views here.

@csrf_exempt
def img_processing(request):
    if request.method == 'POST':
        post_data = request.POST
        img_links = []
        email = post_data['useremail']
        name = post_data['username']
        desc = request.POST['desc']
        files = request.FILES
        # print(files)
        for image in files.getlist('image'):
            print(type(image))  #django.core.files.uploadedfile.InMemoryUploadedFile
            # 이미지가 하나씩 넘어가므로 ml돌릴수 있음 좋겠음
            # ml돌리는 함수에 이미지 넣고 이미지들의 주소를 반환받음
            # 포문 한번 더 돌려서 반환받은거 싹 다 s3에 저장(create)  
            
            # ================원본, 얼굴 이미지만 출력==================
            image_obj = ImgProcModel.objects.create(image=image)    #원본사진 링크 생성
            image_name_list = str(image.name).split('.')    #사진 이름과 확장자 추출
            print(image_name_list)  # aaa.jpg => aaa , jpg
            image_name = image_name_list[0] #aaa
            image_ext = '.'+image_name_list[1]  #jpg

            img_url = 'https://bucket-for-ipl.s3.amazonaws.com/'+str(image_obj.image)   #원본url저장
            img_links.append(img_url)   #html에 보낼 사진 링크 리스트에 추가
            face_array_list = dnnface.image_sending(img_url) #ML을 돌려 얼굴들의 리스트 반환 type=ndarray
            face_counter = 0    #얼굴마다 번호를 붙이기 위한 counter
            for face_array in face_array_list:                
                face = Image.fromarray(face_array)  #PIL로  array를 이미지로 변환 type=PIL.Image.Image
                # face.show()
                face_io = io.BytesIO()  #메모리 저장을 위한(?) BytesIO
                face.save(face_io, format='JPEG')   #이미지를 face_io에 저장하고 format은 크게 상관없음
                print('save finish')
                image.file = face_io    #InMemoryUploadedFile을 새로 만들기 어려워 기존에 있던것의 이미지만 바꿔 사용
                image.name = image_name + 'f-' + str(face_counter)+image_ext    #위와 같이 기존의 변경된 파일에 얼굴마다 count를 붙여 이름저장
                face_counter += 1
                image_obj = ImgFaceModel.objects.create(image=image)    #얼굴 저장
                img_links.append('https://bucket-for-ipl.s3.amazonaws.com/'+str(image_obj.image))
            print(img_links)
            # ==================================================

            # ================모자이크 이미지 출력=========================          
            # image_obj = ImgProcModel.objects.create(image=image)
            # img_url = 'https://bucket-for-ipl.s3.amazonaws.com/'+str(image_obj.image)
            # img_array = dnnface.image_sending(img_url)#ndarray
            # print('image_obj:     ',image_obj)
            # img = Image.fromarray(img_array)  #PIL.Image.Image
            # # img.show()
            # img_io = io.BytesIO()
            # img.save(img_io, format='JPEG')
            # print('save finish')            
            # image.file = img_io
            # image_obj = ImgProcModel.objects.create(image=image)
            # img_links.append('https://bucket-for-ipl.s3.amazonaws.com/'+str(image_obj.image))
            # print(img_links)
            # ==============================================
            
        return render(request, 'image.html', {'email': email, 'name': name, 'desc': desc, 'img_links': img_links})
    else:
        return render(request, 'image.html')