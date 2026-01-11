from .views import *
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
    path('messenger/', messenger_inbox, name='messenger_inbox'),
    path('profile/<int:pk>/messenger/', messenger, name='messenger'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<int:product_id>/', CartCreateView.as_view(), name='add-to-cart'),
    path('cart-update/<int:cart_id>/', CartUpdateView.as_view(), name='cart-update'),
    path('order-create', OrderCreateView.as_view(), name='order-create'),
    path('deposit', DepositRequestView.as_view(), name='deposit'),
]

