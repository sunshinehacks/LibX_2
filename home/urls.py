from django.contrib import admin
from django.urls import include, path
from home import views
app_name = 'home'
urlpatterns = [
    path('',views.home, name="home"),
    path('register',views.register, name="register"),
    path('auth',views.auth, name="auth"),
    path('logout',views.logout, name="logout"),
    path('afterlogin',views.afterlogin, name="afterlogin"),
    path('otp_verify',views.otp_verify, name="otp_verify"),
    path('forgotpass',views.forgotpass,name="forgotpass"),
    path('enter_otp_fp',views.enter_otp_fp,name="enter_otp_fp"),
    path('send_otp_fp',views.send_otp_fp,name="send_otp_fp"),
    path('pass_reset',views.pass_reset,name="pass_reset")
    ]
