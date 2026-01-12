from django.urls import path
from . import views
from .views import IndexView, CategoryView, AboutView, ContactView

app_name='main'

urlpatterns=[
    path('',IndexView.as_view(),name='index'),
    path('category/<int:pk>/', CategoryView.as_view(), name='category'),
    path("about/", AboutView.as_view(), name="about"),
    path("contact/", ContactView.as_view(), name="contact"),
    path('public-offer/', views.PublicOfferView.as_view(), name='public_offer'),
    path('team/<int:pk>/', views.team_detail, name='team_detail')
]