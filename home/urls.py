from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
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
    path('pass_reset',views.pass_reset,name="pass_reset"),
    path('addbook_view',views.addbook_view,name="addbook_view"),
    path('updatebook_view',views.updatebook_view,name="updatebook_view"),
    path('viewbook_view',views.viewbook_view,name="viewbook_view"),
    path('viewTask',views.viewTask,name="viewTask"),
    path('addTask',views.addTask,name="addTask"),
    path('updateTask/<id>',views.updateTask,name="updateTask"),
    path('deleteTask/<id>',views.deleteTask,name="deleteTask"),
    path('upload_csv',views.upload_csv, name='upload_csv'),
    path('download_task_csv',views.download_task_csv, name='download_task_csv'),
    path('download_book_csv',views.download_book_csv, name='download_book_csv'),    
    path('bulk_Upload_book',views.bulk_Upload_book, name='bulk_Upload_book'),
    path('bulk_upload_task',views.bulk_upload_task, name='bulk_upload_task'),
    path('upload_csv_book',views.upload_csv_book, name='upload_csv_book'),
    path('issuebook_view', views.issuebook_view,name="issuebook_view"),
    path('viewissuedbook_view', views.viewissuedbook_view,name="viewissuedbook_view"),
    path('viewuser_view', views.viewuser_view,name="viewuser_view"),
    path('viewissuedbookbyuser', views.viewissuedbookbyuser,name="viewissuedbookbyuser"),
    path('feedback',views.feedback,name="feedback"),
    path('userafterlogin',views.userafterlogin,name="userafterlogin"),
    path('viewbookuser_view',views.viewbookuser_view,name="viewbookuser_view"),
    path('requestbook',views.requestbook,name="requestbook"),
    path('book_request_view',views.book_request_view,name="book_request_view"),
    path('delete_requests/',views.delete_requests_view, name='delete_requests'),
    path('contact',views.contactus,name="contactus"),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    ]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    