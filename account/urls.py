from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView


from .views import LogInView, LogOutView, SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('login/', LogInView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogOutView.as_view(), name='logout'),
]