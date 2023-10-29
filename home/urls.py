from django.contrib import admin
from django.urls import include, path
from home import views
from django.contrib.auth.decorators import login_required
app_name = 'home'
urlpatterns = [
    path('',views.home, name="home"),
    path('register',views.register, name="register"),
    path('auth',views.auth, name="auth"),
    path('logout/',views.logout, name="logout"),
    path('afterlogin',views.afterlogin, name="afterlogin"),
    path('otp_verify',views.otp_verify, name="otp_verify"),
    path('forgotpass',views.forgotpass,name="forgotpass"),
    path('enter_otp_fp',views.enter_otp_fp,name="enter_otp_fp"),
    path('send_otp_fp',views.send_otp_fp,name="send_otp_fp"),
    path('pass_reset',views.pass_reset,name="pass_reset"),
    

    path('books', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/new/', views.book_new, name='book_new'),
    path('book/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('book/<int:pk>/delete/', views.book_delete, name='book_delete'),


    ]
