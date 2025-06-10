from django.urls import path

from .views import ActivateView, RegisterView

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("activate/<uuid:uid>/<str:token>/", ActivateView.as_view(), name="activate"),
]
