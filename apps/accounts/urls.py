from django.urls import path
from .views import AccountCreateView
from .views import AccountRetrieveView
from .views import AccountUpdateView

urlpatterns = [
    path('accounts/', AccountCreateView.as_view(), name='account-create'),
    path('account/', AccountRetrieveView.as_view(), name='account-retrieve'),
    path('account/update/', AccountUpdateView.as_view(), name='account-update'),
]
