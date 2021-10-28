from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView, status
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import CustomTokenObtainPairSerializer, UserCreateSerializer
from .models import RefreshDBModel, User
from rest_framework_simplejwt.state import token_backend

# Create your views here.
class SignUpView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            if User.objects.filter(email=request.POST['email']).exists():
                return Response({'message': 'Email already exists'}, status =400)

            serializer = UserCreateSerializer(data=request.data)
            
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error"}, status=status.HTTP_409_CONFLICT)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            print('user created and saved')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class LogInView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class LogOutView(APIView):
    def post(self, request):
        try:
            # request의 헤더에서 토큰을 가져와서 메일만 추출
            access_token = request.headers['Authorization'].replace('Bearer ', '')
            access_token = AccessToken(access_token)
            email = access_token.payload.get('email')
            
            if(RefreshDBModel.objects.filter(email=email).exists()):
                #  해당 메일을 기반으로 DB에 refresh token이 있는지 검색
                refresh_obj = RefreshDBModel.objects.get(email=email)
                token = RefreshToken(refresh_obj.refresh)
                #   있다면 DB에서 삭제하고 블랙리스트에 등록해서 재사용 차단
                refresh_obj.delete()
                token.blacklist()
            else:
                return Response({'message: theres no data in refreshDB'})
            return Response({'message: blacklist add finish'}, status=status.HTTP_205_RESET_CONTENT)
        except:
            return Response({"message: blacklist add fail"}, status=status.HTTP_400_BAD_REQUEST)

