
from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name="home"),
    path('about', views.about, name="about"),
    
    ########################## SIGN UP URLS #####################
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    
    ################## STUDENT PAGES URLS ######################
    path('dashboard', views.dashboard, name="dashboard"),
    path('application', views.application, name="application"),
    path('user_profile', views.user_profile, name="user_profile"),
    path('personal_details', views.personal_details, name="personal_details"),
    path('contact_details', views.contact_details, name="contact_details"),
    path('address', views.address, name="address"),
    path('qualification', views.qualification, name="qualification"),
    path('graduation', views.graduation, name="graduation"),
    path('document', views.document, name="document"),
    path('preview', views.preview, name="preview"),
    path('program_choices', views.program_choices, name='program_choices'),
    path('merit_list', views.merit_list, name='merit_list'),
    path('admin_merit_list', views.admin_merit_list, name='admin_merit_list'),
    path('approval', views.approval, name='approval'),
    path('accept_decline_seat', views.accept_decline_seat, name='accept_decline_seat'),
    path('search_user', views.search_user, name='search_user'),
    path('search_student', views.search_student, name='search_student'),
    path('course_data', views.course_data, name='course_data'),

    
    ################### ADMIN URLS ############################
    path('a_dashboard', views.a_dashboard, name="a_dashboard"),
    path('detail_view/<int:user_id>/', views.detail_view, name='detail_view')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
