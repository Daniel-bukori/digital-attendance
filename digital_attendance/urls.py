from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('attendance/submit/', views.submit_attendance, name='submit_attendance'),
    path('announcement/post/', views.post_announcement, name='post_announcement'),
    path('material/upload/', views.upload_material, name='upload_material'),
    # Ongeza mstari huu ndani ya urlpatterns = [ ... ]
    path('view-document/<str:file_type>/<int:file_id>/', views.view_document, name='view_document'),
    # CHINI KABISA YA PATH ZILIZOPO KWENYE URLS.PY:
    path('session/create/', views.cr_start_session, name='cr_start_session'),
    path('attendance/submit-smart/', views.submit_attendance_smart, name='submit_attendance_smart'),
    path('attendance/pdf/<int:session_id>/', views.download_attendance_pdf, name='download_attendance_pdf'),
]