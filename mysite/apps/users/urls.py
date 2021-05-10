from django.urls import path

from .views.register import *
from .views.signup import *
from .views.auth import *


urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('account/', Account.as_view(), name='account'),


    path('signup/', Signup.as_view(), name='signup'),
    path('signup/done/', SignupComplete.as_view(), name='signup_complete'),
    # path('signup/<uidb64>/<token>/', SignupConfirm.as_view(), name='signup_confirm'),


    path('password-change/', PasswordChange.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDone.as_view(), name='password_change_done'),      
    path('password-reset/', PasswordReset.as_view(), name='password_reset'),   
    path('password-reset/done/', PasswordResetDone.as_view(), name='password_reset_done'),  
    path('reset/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetComplete.as_view(), name='password_reset_complete'),  

    
    path('<str:username>/', Profile.as_view(), name='profile'),
]