import io, os, pathlib
from django.core.files.base import File
from django.http import response, HttpResponse
from .models import ImgFaceModel, ImgProcModel, VdoFaceModel, VdoProcModel
from PIL import Image
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .face import dnnface
# Create your views here.

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
def face_extract_img(request):  #이미지에서 얼굴 추출
    if request.method == 'POST':
        img_links = []
        face_counter = 0    #얼굴마다 번호를 붙이기 위한 counter
        files = request.FILES
        # print(files)
        for image in files.getlist('image'):
            #type(image) : django.core.files.uploadedfile.InMemoryUploadedFile
            image_obj = ImgProcModel.objects.create(image=image)    #원본사진 링크 생성
            image_name_list = os.path.splitext(str(image.name))    #사진 이름과 확장자 추출
            print(image_name_list)  # aaa.jpg => aaa , jpg
            image_name = image_name_list[0] #aaa
            image_ext = image_name_list[1]  #.jpg

            img_url = 'https://bucket-for-ipl.s3.amazonaws.com/'+str(image_obj.image)   #원본url저장
            img_links.append(img_url)
            face_array_list = dnnface.image_sending(img_url) #ML을 돌려 얼굴들의 리스트 반환 type=ndarray

            for face_array in face_array_list:                
                face = Image.fromarray(face_array)  #PIL로  array를 이미지로 변환 type=PIL.Image.Image
                # face.show()
                face_io = io.BytesIO()  #메모리 저장을 위한(?) BytesIO
                face.save(face_io, format='JPEG')   #이미지를 face_io에 저장하고 format은 크게 상관없음
                print('save finish')
                face_image = File(face_io, image_name + 'f-' + str(face_counter)+image_ext)
                face_counter += 1
                face_obj = ImgFaceModel.objects.create(image=face_image)    #얼굴 저장
                img_links.append('https://bucket-for-ipl.s3.amazonaws.com/'+str(face_obj.image))
            print(img_links)
        return response.JsonResponse({'img_links': img_links})
    return response.JsonResponse({'message': 'fail get face image'})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
def img_processing(request): # 이미지 모자이크 처리, 완성 이미지 주소 반환
    if request.method == 'POST':
        img_url = request.POST['img_url']
        img_str = pathlib.Path(img_url)
        
        get_list = request.POST['human_list']
        human_list = []
        for human in eval(get_list):
            human_list.append(int(human))
        m_img_array = dnnface.image_sending(img_url, human_list)
        
        img_io = io.BytesIO()
        m_img_array.save(img_io, format='PNG')
        
        image = File(img_io, img_str.name.split('.')[0] + img_str.suffix)
        image_obj = ImgProcModel.objects.create(image=image)
        img_url = 'https://bucket-for-ipl.s3.amazonaws.com/'+str(image_obj.image)
        print(img_url)
        
        return HttpResponse(img_url)#HttpResponse(rsp.content.decode('utf8'))
    return response.JsonResponse({'message': 'image upload fail'})
    


people_list = []

@api_view(['POST'])
def face_extrac_video(request): #영상에서 사람얼굴 탐지, 얼굴 이미지 반환
    vdo_links = []
    face_counter = 0
    if request.method == 'POST':
        file = request.FILES
        for video in file.getlist('video'):
            print('video type:   '+str(type(video)))
            video_obj = VdoProcModel.objects.create(video = video)
            video_info_list = os.path.splitext(str(video.name))    #사진 이름과 확장자 추출
            print(video_info_list)  # aaa.jpg => aaa , jpg
            video_name = video_info_list[0] #aaa
            vdo_url = 'https://bucket-for-ipl.s3.amazonaws.com/'+str(video_obj.video)   #원본url저장
            vdo_links.append(vdo_url)
            global people_list
            face_array_list, people_list = dnnface.video_sending(vdo_url)
            
            # print(face_array_list)
            print(type(face_array_list))            
            for face_array in face_array_list:
                face = Image.fromarray(face_array)  #PIL로  array를 이미지로 변환 type=PIL.Image.Image
                # face.show()
                face_io = io.BytesIO()  #메모리 저장을 위한(?) BytesIO
                face.save(face_io, format='JPEG')   #이미지를 face_io에 저장하고 format은 크게 상관없음
                print('save finish')
                image = File(face_io, video_name + 'f-' + str(face_counter)+'.jpg')
                face_counter += 1
                face_obj = VdoFaceModel.objects.create(video_face=image)    #얼굴 저장
                vdo_links.append('https://bucket-for-ipl.s3.amazonaws.com/'+str(face_obj.video_face))

        return response.JsonResponse({'vdo_links': vdo_links})  #[0]:video link, [1~]face-image links
    return response.JsonResponse({'message': 'fail get face image'})
    
@api_view(['POST'])
def vdo_processing(request):    #영상 모자이크 처리, 완성 영상 주소 반환
    if request.method == 'POST':
        vdo_url = request.POST['vdo_url']
        get_list = request.POST['human_list']
        print(get_list)
        human_list = []
        for human in eval(get_list):
            human_list.append(human)
        
        vdo_url = dnnface.video_sending(vdo_url, human_list, people_list) #human_list

        people_list.clear()
        return HttpResponse(vdo_url)
    return response.JsonResponse({'message': 'video upload fail'})