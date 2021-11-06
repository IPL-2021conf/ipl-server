from django.urls import path
from .views import CustomTokenRefreshView, LogInView, LogOutView, SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('login/', LogInView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogOutView.as_view(), name='logout'),
]