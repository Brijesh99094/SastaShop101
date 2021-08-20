from django.urls import path
from .views import *

urlpatterns =[
    path('',Index.as_view(),name="index"),
     path('order',auth_middleware( OrderView.as_view()),name="order"),
    path('signup',SignUpView.as_view(),name="signup"),
    path('login',LoginView.as_view(),name="login"),
    path('logout',logout,name='logout'),
    path('cart',auth_middleware(CartView.as_view()),name="cart"),
    path('check-out',Checkout.as_view(),name="check-out"),
    path('validated_username', validated_username,name='validated-username')
]
