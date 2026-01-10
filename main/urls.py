from django.urls import path
from .views import IndexView,CategoryView
app_name='main'

urlpatterns=[
    path('',IndexView.as_view(),name='index'),
    path('category/<int:pk>/', CategoryView.as_view(), name='category')
]