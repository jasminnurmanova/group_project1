from .views import SignupView
from django.urls import path
app_name='users'

urlpatterns=[
    path('signup',SignupView.as_view(),name='signup')
]