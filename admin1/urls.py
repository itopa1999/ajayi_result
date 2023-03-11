from django.urls import path
from admin1 import views
from django.contrib.auth.views import LogoutView,LoginView


urlpatterns = [
    path("", views.login_user, name="login_user"),
    path("registerlecturer/", views.registerlecturer, name="registerlecturer"),
    path("registeradmin/", views.registeradmin, name="registeradmin"),
    path("admindashboard/", views.admindashboard, name="admindashboard"),
    path("registration/", views.registration, name="registration"),
    path("adminfaculty/", views.adminfaculty, name="adminfaculty"),
    path("admindepartment/", views.admindepartment, name="admindepartment"),
    path("admincourse/", views.admincourse, name="admincourse"),
    path("adminresult/", views.adminresult, name="adminresult"),
    path("newdepartment/", views.newdepartment, name="newdepartment"),
    path("newcourse/", views.newcourse, name="newcourse"),
    path("newfaculty/", views.newfaculty, name="newfaculty"),
    path("viewdepartment/", views.viewdepartment, name="viewdepartment"),
    path("viewcourse/", views.viewcourse, name="viewcourse"),
    path("viewresult/", views.viewresult, name="viewresult"),
    path("result/<str:pk>/", views.result, name="result"),
    path("studentresult/", views.studentresult, name="studentresult"),
    path("viewfaculty/", views.viewfaculty, name="viewfaculty"),
    path("deletefaculty/<str:pk>/", views.deletefaculty, name="deletefaculty"),
    path("profiledepartment/<str:pk>/", views.profiledepartment, name="profiledepartment"),
    path("profilecourse/<str:pk>/", views.profilecourse, name="profilecourse"),
    path("profileresult/<str:pk>/", views.profileresult, name="profileresult"),
    path("profilefaculty/<str:pk>/", views.profilefaculty, name="profilefaculty"),
    path('logout/', LogoutView.as_view(template_name= "permission/logout.html"),name='logout'),
    path("changepassword/", views.changepassword, name="changepassword"),
    
    
    
    
    path("lecturerdashboard/", views.lecturerdashboard, name="lecturerdashboard"),
    path("admin_lecturer/", views.admin_lecturer, name="admin_lecturer"),
    path("profilelecturer/<str:pk>/", views.profilelecturer, name="profilelecturer"),
    path("lecturercourse/", views.lecturercourse, name="lecturercourse"),
    path("lecturercourseprofile/<str:pk>/", views.lecturercourseprofile, name="lecturercourseprofile"),
    path("addresult/", views.addresult, name="addresult"),
    path("updateresult/<str:pk>/", views.updateresult, name="updateresult"),
    path("lecturerviewresult/", views.lecturerviewresult, name="lecturerviewresult"),
    path("lecturerprofile/", views.lecturerprofile, name="lecturerprofile"),
    path("lecturerchangepassword/", views.lecturerchangepassword, name="lecturerchangepassword"),
    
    
    
    
    
    
    
   
    path("admin_student/", views.admin_student, name="admin_student"),
    path("newstudent/", views.newstudent, name="newstudent"),
    path("studentprofile/", views.studentprofile, name="studentprofile"),
    path("profilestudent/<str:pk>/", views.profilestudent, name="profilestudent"),
    
    
    
]