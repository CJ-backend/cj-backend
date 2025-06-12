from django.urls import path
from .views import AccountCreateView
from .views import AccountRetrieveView

urlpatterns = [
    path('accounts/', AccountCreateView.as_view(), name='account-create'),
    path('account/', AccountRetrieveView.as_view(), name='account-retrieve'),
]
