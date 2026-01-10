from .views import (SignupView, logout, ProfileView, UpdateProfileView,WishlistView, AddRemoveWishlistView,RecentlyViewedView, messenger)
from django.urls import path
app_name='users'

urlpatterns=[
    path('signup',SignupView.as_view(),name='signup'),
    path('logout/', logout, name='logout'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('update/', UpdateProfileView.as_view(), name='update_profile'),
    path('addremovewishlist/<int:product_id>', AddRemoveWishlistView.as_view(), name='addremovewishlist'),
    path('wishlists/', WishlistView.as_view(), name='wishlists'),
    path('recently-viewed', RecentlyViewedView.as_view(), name='recently_viewed'),
    path('profile/<int:pk>/messenger/', messenger, name='messenger'),

]