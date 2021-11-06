from django.contrib.auth.base_user import AbstractBaseUser
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import RefreshDBModel, User

User = get_user_model()
class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    
    def create(self, validated_data):
        user = User.objects.create(
            email = validated_data['email'],
            username = validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class RefreshDBSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefreshDBModel
        fields = ['email', 'refresh',]
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token
        
    refresh_serializer = RefreshDBSerializer(read_only=True)
    def validate(self, attrs):        
        try:
            request = self.context['request']
            email = request.POST['email']
            password = request.POST['password']
            user = User.objects.get(email=email)
        except KeyError:
            pass
        
        # 로그인 시 DB에 refresh token이 남아있는지 확인
        if RefreshDBModel.objects.filter(email = email).exists():
            if AbstractBaseUser.check_password(user, password):
                print("Password: checked")
                # refresh token을 이용해 access token만 재발급
                refresh_obj = RefreshDBModel.objects.get(email=email)            
                print('refresh_data is exists')
                print('refresh_data: ', str(refresh_obj.refresh))           
                refresh = RefreshToken(refresh_obj.refresh)
                data = {'access': str(refresh.access_token)}
                return data
            else:
                return {"error: password is not matched"}
        else:
            # 전부 다 발급
            print('create new token')
            data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
            refresh_obj = RefreshDBModel.objects.create(email=email, refresh=data.get('refresh'))
            print(refresh_obj.refresh)
            return data

    # def validate(self, attrs):
    #     try:
    #         request = self.context['request']
    #     except KeyError:
    #         pass

    #     print(attrs)
    #     try:
    #         refresh = RefreshToken(request.POST['refresh'])
    #         data = {'access': str(refresh.access_token)}
    #         return data            
            
    #     except:
    #         # 엑세스 토큰만 발급
    #         data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
    #         return data
