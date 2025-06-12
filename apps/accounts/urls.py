from django.urls import path
from .views import AccountCreateView

urlpatterns = [
    path('accounts/', AccountCreateView.as_view(), name='account-create'),
]

