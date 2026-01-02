from django.urls import path
from user.views import UserViewSet
app_name = "users"
urlpatterns = [
    path('login/', UserViewSet.as_view({"post":"login"}), name="user_login"),
    path('sign_up/', UserViewSet.as_view({"post":"register"}), name="user_register"),

]