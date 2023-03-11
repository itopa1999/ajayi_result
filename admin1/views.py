from django.shortcuts import render, redirect,reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator,EmptyPage
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,AdminPasswordChangeForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from django.core.exceptions import *
from django.contrib.auth.decorators import login_required,user_passes_test
from .decorators import allowed_users,allowed_users1
from django.contrib.auth.models import Group
from .models import *
from .forms import UserForm1,UserForm,StudentForm,StudentForm1,FacultyForm,DepartmentForm,DepartmentForm1,CourseForm,CourseForm1,LecturerForm,ResultForm,ResultForm1
from .forms import PasswordChangeForm
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import User

# Create your views here.


@login_required(login_url='login_user')
@allowed_users(allowed_roles=['superadmin'])
def registerlecturer(request):
    form = UserForm1()
    if request.method =='POST':
        form = UserForm1(request.POST)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if User.objects.filter(username=username):
            messages.error(request, "Username already exists")
            return redirect('registerlecturer')
        
        if User.objects.filter(email=email):
            messages.error(request, "Email already exists")
            return redirect('registerlecturer')
        
        if password1 != password2:
            messages.error(request, "password dismatch")
            return redirect('registerlecturer')
        
        if form.is_valid():
            user= form.save()
            username = form.cleaned_data.get('username')
            group= Group.objects.get(name='lecturer')
            user.groups.add(group)
        
            Lecturer.objects.create(
                user=user,
                name=first_name,
                staff_ID=last_name,
                email=email,
                username=user.username,
                
        )     
            messages.success(request, 'user has been created for ' + username)
            return redirect('registration')
    context = {'form':form}
    return render(request, 'permission/registerlecturer.html', context)


@login_required(login_url='login_user')
@allowed_users(allowed_roles=['superadmin'])
def registeradmin(request):
    form = UserForm()
    if request.method =='POST':
        form = UserForm(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if User.objects.filter(username=username):
            messages.error(request, "Username already exists")
            return redirect('registeradmin')
        
        if User.objects.filter(email=email):
            messages.error(request, "Email already exists")
            return redirect('registeradmin')
        
        
        if password1 != password2:
            messages.error(request, "Incorrect password")
            return redirect('registeradmin')
        if form.is_valid():
            user= form.save()
            username = form.cleaned_data.get('username')
            group= Group.objects.get(name='admin1')
            user.groups.add(group)  
            messages.success(request, 'user has been created for ' + username)
            return redirect('registration')
    context = {'form':form}
    return render(request, 'permission/registeradmin.html', context)



def is_admin1(user):
    return user.groups.filter(name='admin1').exists()

def is_lecturer(user):
    return user.groups.filter(name='lecturer').exists()

def is_superadmin(user):
    return user.groups.filter(name='superadmin').exists()


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
        if is_admin1(request.user):      
            return redirect('admindashboard')
        if is_superadmin(request.user):      
            return redirect('admindashboard')
        
        if is_lecturer(request.user):      
            return redirect('lecturerdashboard')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('/')

    return render(request, "permission/loginpage.html")


@login_required(login_url='login_user')
@allowed_users(allowed_roles=['superadmin','admin1'])
def admindashboard(request):
    stu=Student.objects.all().count()
    lec=Lecturer.objects.all().count()
    context={'stu':stu,'lec':lec}
    return render(request,'admin1/admindashboard.html', context)


@login_required(login_url='login_user')
@allowed_users(allowed_roles=['superadmin'])
def registration(request):
    
    return render(request,'permission/registration.html')


@login_required(login_url='login_user')
@allowed_users1(allowed_roles=['lecturer'])
def lecturerdashboard(request):
    stu=Student.objects.all().count()
    context={'stu':stu}
    return render(request,'lecturer/lecturerdashboard.html', context)


@login_required(login_url='login_user')
@allowed_users1(allowed_roles=['lecturer'])
def lecturercourse(request):
    cou=Course.objects.filter(lecturer=Lecturer.objects.get(user_id=request.user.id))
    context={'cou':cou}
    return render(request,'lecturer/lecturercourse.html', context)


@login_required(login_url='login_user')
@allowed_users1(allowed_roles=['lecturer'])
def lecturercourseprofile(request,pk):
    cou=Course.objects.get(id=pk)
    context={'cou':cou}
    return render(request,'lecturer/lecturercourseprofile.html', context)



@login_required(login_url='login_user')
@allowed_users1(allowed_roles=['lecturer'])
def lecturerprofile(request):
    user=Lecturer.objects.filter(user_id=request.user.id)
    lecturer=Lecturer.objects.get(user_id=request.user.id)
    view1=user[0].name
    view2=user[0].staff_ID
    view3=user[0].faculty
    view4=user[0].department
    view5=user[0].phone_no
    view6=user[0].email
    cou=Course.objects.filter(lecturer=lecturer)
    context={'view1':view1,'view2':view2,'view3':view3,'view4':view4,
             'view5':view5,'view6':view6,'cou':cou,}
    return render(request,'lecturer/lecturerprofile.html', context)


@login_required(login_url='login_user')
@allowed_users1(allowed_roles=['lecturer'])
def addresult(request):
    lec=Lecturer.objects.get(user_id=request.user.id)
    form = ResultForm()
    if request.method == 'POST':
       form = ResultForm(request.POST)
       if form.is_valid():
           stu=form.save(commit=False)
           student=Student.objects.get(id=request.POST.get('studentID'))
           course=Course.objects.get(id=request.POST.get('courseID'))
           stu.student=student
           stu.course=course
           stu.lecturer=lec
           stu.save()
           messages.success(request, 'Result has been submitted to the admin')
           return redirect('addresult')
    context={'form':form}
    return render(request,'lecturer/addresult.html', context)


@login_required(login_url='login_user')
@allowed_users1(allowed_roles=['lecturer'])
def lecturerviewresult(request):
    lecturer=Lecturer.objects.get(user_id=request.user.id)
    res=Result.objects.filter(lecturer=lecturer)
    if request.method == "POST":
        res.delete()
        messages.success(request, 'Result has been deleted Successfully')
        return redirect('lecturerviewresult')
    context={'res':res}
    return render(request,'lecturer/lecturerviewresult.html', context)


@login_required(login_url='login_user')
@allowed_users1(allowed_roles=['lecturer'])
def updateresult(request,pk):
    res=Result.objects.get(id=pk)
    form = ResultForm1(instance=res)
    if request.method == 'POST':
       form =  ResultForm1(request.POST,instance=res)
       if form.is_valid():
           form.save()
           messages.success(request, 'Result has been updated Successfully')
           return redirect('lecturerviewresult',)
    context={'res':res,'form':form}
    return render(request,'lecturer/updateresult.html', context)


@login_required(login_url='login_user')
@allowed_users(allowed_roles=['superadmin','admin1'])
def admin_lecturer(request):
    lec=Lecturer.objects.all()
    context={'lec':lec}
    return render(request,'admin1/admin_lecturer.html', context)


@login_required(login_url='login_user')
@allowed_users(allowed_roles=['superadmin','admin1'])
def profilelecturer(request,pk):
    lec=Lecturer.objects.get(id=pk)
    form = LecturerForm(instance=lec)
    if request.method == 'POST':
       form =  LecturerForm(request.POST,instance=lec)
       if form.is_valid():
           form.save()
           messages.success(request, 'Lecturer has been updated Successfully')
           return redirect('profilelecturer', lec.id)
       if request.method == "POST":
           user=User.objects.get(id=lec.user_id)
           user.delete()
           lec.delete()
           messages.success(request, 'Lecturer has been deleted Successfully')
           return redirect('admin_lecturer')
    context= {'lec':lec,'item':lec,'form':form}
    return render(request,'admin1/profilelecturer.html', context)







@login_required(login_url='login_user')
@allowed_users(allowed_roles=['superadmin','admin1'])
def admin_student(request):
    context={}
    return render(request,'admin1/admin_student.html', context)


@login_required(login_url='login_user')
@allowed_users(allowed_roles=['superadmin','admin1'])
def newstudent(request):
    form = StudentForm()
    if request.method == 'POST':
       form = StudentForm(request.POST)
       if form.is_valid():
           student=form.save(commit=False)
           department=Department.objects.get(id=request.POST.get('departmentID'))
           faculty=Faculty.objects.get(id=request.POST.get('facultyID'))
           student.department=department
           student.faculty=faculty
           student.save()
           messages.success(request, 'Student has been created')
           return redirect('admin_student')
    context = {'form':form}
    return render(request,'admin1/newstudent.html', context)


@login_required(login_url='login_user')
@allowed_users(allowed_roles=['superadmin','admin1'])
def studentprofile(request):
    stu=Student.objects.all()
    context={'stu':stu}
    return render(request,'admin1/studentprofile.html', context)


@login_required(login_url='login_user')
@allowed_users(allowed_roles=['superadmin','admin1'])
def profilestudent(request,pk):
    stu=Student.objects.get(id=pk)
    form = StudentForm1(instance=stu)
    if request.method == 'POST':
       form =  StudentForm1(request.POST,instance=stu)
       if form.is_valid():
           form.save()
           messages.success(request, 'Student has been updated Successfully')
           return redirect('profilestudent', stu.id)
       if request.method == "POST":
           stu.delete()
           messages.success(request, 'Student has been deleted Successfully')
           return redirect('studentprofile')
    context= {'stu':stu,'item':stu,'form':form}
    return render(request,'admin1/profilestudent.html', context)








@login_required(login_url='login_user')
@allowed_users(allowed_roles=['superadmin','admin1'])
def adminfaculty(request):
    context={}
    return render(request,'admin1/adminfaculty.html', context)

@login_required(login_url='login_user')
@allowed_users(allowed_roles=['superadmin','admin1'])
def newfaculty(request):
    form = FacultyForm()
    if request.method == 'POST':
       form =  FacultyForm(request.POST)
       if form.is_valid():
           form.save()
           messages.success(request, 'Faculty has been Added')
           return redirect('adminfaculty')
    context={'form':form}
    return render(request,'admin1/newfaculty.html', context)


@login_required(login_url='login_user')
@allowed_users(allowed_roles=['superadmin','admin1'])
def viewfaculty(request):
    fac=Faculty.objects.all()
    context={'fac':fac}
    return render(request,'admin1/viewfaculty.html', context)


@login_required(login_url='login_user')
@allowed_users(allowed_roles=['superadmin','admin1'])
def profilefaculty(request,pk):
    fac=Faculty.objects.get(id=pk)
    dep=Department.objects.filter(faculty=pk)
    depcount=dep.count()
    stucount=Student.objects.filter(faculty=pk).count()
    stucount1=Student.objects.filter(faculty=pk)
    nd=stucount1.filter(level='ND').count()
    hnd=stucount1.filter(level='HND').count()
    facu = Faculty.objects.get(id=pk)
    form = FacultyForm(instance=facu)
    if request.method == 'POST':
       form =  FacultyForm(request.POST,instance=facu)
       if form.is_valid():
           form.save()
           messages.success(request, 'updated  successfully')
           return redirect('profilefaculty', fac.id)
    context = {'form':form,'fac':fac, 'dep':dep, 'depcount':depcount, 
              'stucount':stucount,'item':fac,'form':form,
             'facu':facu,'nd':nd,'hnd':hnd,}
    return render(request,'admin1/profilefaculty.html', context)


@login_required(login_url='login_user')
@allowed_users(allowed_roles=['superadmin','admin1'])
def deletefaculty(request,pk):
    fac=Faculty.objects.get(id=pk)
    fac.delete()
    messages.success(request, 'Deleted  successfully')
    return redirect('viewfaculty')
    




@login_required(login_url='login_user')
@allowed_users(allowed_roles=['superadmin','admin1'])
def admindepartment(request):
    context={}
    return render(request,'admin1/admindepartment.html', context)



@login_required(login_url='login_user')
@allowed_users(allowed_roles=['superadmin','admin1'])
def newdepartment(request):
    form = DepartmentForm()
    if request.method == 'POST':
       form =  DepartmentForm(request.POST)
       if form.is_valid():
           student=form.save(commit=False)
           faculty=Faculty.objects.get(id=request.POST.get('facultyID'))
           student.faculty=faculty
           student.save()
           messages.success(request, 'Department has been Added')
           return redirect('admindepartment')
    context={'form':form}
    return render(request,'admin1/newdepartment.html', context)


@login_required(login_url='login_user')
@allowed_users(allowed_roles=['superadmin','admin1'])
def viewdepartment(request):
    dep=Department.objects.all()
    context={'dep':dep}
    return render(request,'admin1/viewdepartment.html', context)


@login_required(login_url='login_user')
@allowed_users(allowed_roles=['superadmin','admin1'])
def profiledepartment(request,pk):
    dep=Department.objects.get(id=pk)
    depu = Department.objects.get(id=pk)
    countstu=Student.objects.filter(department=pk).count()
    stu=Student.objects.filter(department=pk)
    hnd= stu.filter(level='HND').count()
    nd= stu.filter(level='ND').count()
    form = DepartmentForm1(instance=depu)
    if request.method == 'POST':
       form =  DepartmentForm1(request.POST,instance=depu)
       if form.is_valid():
           form.save()
           messages.success(request, 'Updated Successfully')
           return redirect('profiledepartment', depu.id)
       if request.method == "POST":
           dep.delete()
           messages.success(request, 'Deleted Successfully')
           return redirect('viewdepartment')
    context= {'dep':dep,'item':dep,'form':form,'depu':depu,
              'countstu':countstu,'hnd':hnd,'nd':nd}
    return render(request,'admin1/profiledepartment.html', context)




@login_required(login_url='login_user')
@allowed_users(allowed_roles=['superadmin','admin1'])
def admincourse(request):
    context={}
    return render(request,'admin1/admincourse.html', context)


@login_required(login_url='login_user')
@allowed_users(allowed_roles=['superadmin','admin1'])
def newcourse(request):
    form = CourseForm()
    if request.method == 'POST':
       form =  CourseForm(request.POST)
       if form.is_valid():
           course=form.save(commit=False)
           department=Department.objects.get(id=request.POST.get('departmentID'))
           faculty=Faculty.objects.get(id=request.POST.get('facultyID'))
           lecturer=Lecturer.objects.get(id=request.POST.get('lecturerID'))
           course.department=department
           course.faculty=faculty
           course.lecturer=lecturer
           course.save()
           messages.success(request, 'Course has been Added')
           return redirect('admincourse')
    context={'form':form}
    return render(request,'admin1/newcourse.html', context)


@login_required(login_url='login_user')
@allowed_users(allowed_roles=['superadmin','admin1'])
def viewcourse(request):
    cou=Course.objects.all()
    context={'cou':cou}
    return render(request,'admin1/viewcourse.html', context)




@login_required(login_url='login_user')
@allowed_users(allowed_roles=['superadmin','admin1'])
def profilecourse(request,pk):
    cou=Course.objects.get(id=pk)
    form = CourseForm1(instance=cou)
    if request.method == 'POST':
       form =  CourseForm1(request.POST,instance=cou)
       if form.is_valid():
           form.save()
           messages.success(request, 'Updated Successfully')
           return redirect('profilecourse', cou.id)
       if request.method == "POST":
           cou.delete()
           messages.success(request, 'Deleted Successfully')
           return redirect('viewcourse')
    context={'cou':cou,'form':form,'item':cou,}
    return render(request,'admin1/profilecourse.html', context)


@login_required(login_url='login_user')
@allowed_users(allowed_roles=['superadmin','admin1'])
def updatecourse(request,pk):
    context={}
    return render(request,'admin1/profilecourse.html', cont)
    
    





@login_required(login_url='login_user')
@allowed_users(allowed_roles=['superadmin','admin1'])
def adminresult(request):
    lec=Lecturer.objects.all()
    context={'lec':lec}
    return render(request,'admin1/adminresult.html', context)



@login_required(login_url='login_user')
@allowed_users(allowed_roles=['superadmin','admin1'])
def viewresult(request):
    lec=Lecturer.objects.all()
    context={'lec':lec}
    return render(request,'admin1/adminresult.html', context)


@login_required(login_url='login_user')
@allowed_users(allowed_roles=['superadmin','admin1'])
def studentresult(request):
    stu=Student.objects.all()
    context={'stu':stu}
    return render(request,'admin1/studentresult.html', context)


@login_required(login_url='login_user')
@allowed_users(allowed_roles=['superadmin','admin1'])
def result(request, pk):
    stud=Student.objects.filter(id=pk)
    dep=stud[0].department
    stu=Student.objects.get(id=pk)
    ndstudent=Student.objects.filter(id=pk,level="ND")
    re=Result.objects.filter(student=pk)
    if ndstudent:
        res=re.filter(course__semester="ND1 first Semester",course__department=dep)
        res1=re.filter(course__semester="ND1 second Semester",course__department=dep)
        res2=re.filter(course__semester="ND2 first Semester",course__department=dep)
        res3=re.filter(course__semester="ND2 second Semester",course__department=dep)
        tit="ND1 FIRST SEMESTER"
        tit1="ND1 SECOND SEMESTER"
        tit2="ND2 FIRST SEMESTER"
        tit3="ND2 SECOND SEMESTER"
    else:
        res=re.filter(course__semester="HND1 first Semester",course__department=dep)
        res1=re.filter(course__semester="HND1 second Semester",course__department=dep)
        res2=re.filter(course__semester="HND2 first Semester",course__department=dep)
        res3=re.filter(course__semester="HND2 second Semester",course__department=dep)
        tit="HND1 FIRST SEMESTER"
        tit1="HND1 SECOND SEMESTER"
        tit2="HND2 FIRST SEMESTER"
        tit3="HND2 SECOND SEMESTER"
    qp=res.aggregate(Sum('qp'))['qp__sum']
    cu=res.aggregate(Sum('cu'))['cu__sum']
    qp1=res1.aggregate(Sum('qp'))['qp__sum']
    cu1=res1.aggregate(Sum('cu'))['cu__sum']
    qp2=res2.aggregate(Sum('qp'))['qp__sum']
    cu2=res2.aggregate(Sum('cu'))['cu__sum']
    qp3=res3.aggregate(Sum('qp'))['qp__sum']
    cu3=res3.aggregate(Sum('cu'))['cu__sum']
    if qp  is None and cu is None:
        gpaa=0
    else:
        gpaa=qp/cu
    if qp1  is None and cu1 is None:
        gpaa1=0
    else:
        gpaa1=qp1/cu1
    cgpa=(gpaa+gpaa1)/2
    if qp2  is None and cu2 is None:
        gpaa2=0
    else:
        gpaa2=qp2/cu2
    if qp3  is None and cu3 is None:
        gpaa3=0
    else:
        gpaa3=qp3/cu3
    cgpa1=(gpaa2+gpaa3)/2
    
    
    if gpaa >=3.50:
        grade=("DISTINCTION")
    elif gpaa <=3.49 and gpaa >=3.00:
        grade =("UPPER CREDIT")
    elif gpaa <=2.99 and gpaa >=2.50:
        grade =("LOWER CREDIT")
    elif gpaa <=2.49 and gpaa >=2.00:
        grade =("PASS")
    elif gpaa <=1.99 and gpaa >=0.01:
        grade =("FAIL")
    else:
        grade =''
        
        
    if gpaa1 >=3.50:
        grade1=("DISTINCTION")
    elif gpaa1 <=3.49 and gpaa1 >=3.00:
        grade1 =("UPPER CREDIT")
    elif gpaa1 <=2.99 and gpaa1 >=2.50:
        grade1 =("LOWER CREDIT")
    elif gpaa1 <=2.49 and gpaa1 >=2.00:
        grade1 =("PASS")
    elif gpaa1 <=1.99 and gpaa1 >=0.01:
        grade1 =("FAIL")
    else:
        grade1 =''
        
    if gpaa2 >=3.50:
        grade2=("DISTINCTION")
    elif gpaa2 <=3.49 and gpaa2 >=3.00:
        grade2 =("UPPER CREDIT")
    elif gpaa2 <=2.99 and gpaa2 >=2.50:
        grade2 =("LOWER CREDIT")
    elif gpaa2 <=2.49 and gpaa2 >=2.00:
        grade2 =("PASS")
    elif gpaa2 <=1.99 and gpaa2 >=0.01:
        grade2 =("FAIL")
    else:
        grade2 =''
        
    if gpaa3 >=3.50:
        grade3=("DISTINCTION")
    elif gpaa3 <=3.49 and gpaa3 >=3.00:
        grade3 =("UPPER CREDIT")
    elif gpaa3 <=2.99 and gpaa3 >=2.50:
        grade3 =("LOWER CREDIT")
    elif gpaa3 <=2.49 and gpaa3 >=2.00:
        grade3 =("PASS")
    elif gpaa3 <=1.99 and gpaa3 >=0.01:
        grade3 =("FAIL")
    else:
        grade3 =''
    context={'stu':stu,'res':res,'res1':res1,'res2':res2,'res3':res3,
             'tit':tit,'gpaa':gpaa,'gpaa1':gpaa1,'gpaa2':gpaa2,'gpaa3':gpaa3,
             'tit1':tit1,'tit2':tit2,'tit3':tit3,'grade':grade,
             'grade1':grade1,'grade2':grade2,'grade3':grade3,'cgpa':cgpa,'cgpa1':cgpa1}
    return render(request,'admin1/result.html', context)


@login_required(login_url='login_user')
@allowed_users(allowed_roles=['superadmin','admin1'])
def profileresult(request,pk):
    lec=Lecturer.objects.get(id=pk)
    res=Result.objects.filter(lecturer=lec)
    context={'res':res,'lec':lec}
    return render(request,'admin1/profileresult.html', context)

@login_required(login_url='login_user')
@allowed_users1(allowed_roles=['lecturer'])
def lecturerchangepassword(request):
    form = PasswordChangeForm(user=request.user, data=request.POST)
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')        
        if new_password1 != new_password2:
            messages.error(request, "new password and confrm password dismatch")
            return redirect('lecturerchangepassword')
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password has been changed successfully')
            return redirect('lecturerdashboard')
    context={'form':form}
    return render(request,'lecturer/lecturerchangepassword.html',context)



@login_required(login_url='login_user')
@allowed_users(allowed_roles=['superadmin','admin1'])
def changepassword(request):
    form = PasswordChangeForm(user=request.user, data=request.POST)
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')        
        if new_password1 != new_password2:
            messages.error(request, "new password and confrm password dismatch")
            return redirect('lecturerchangepassword')
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password has been changed successfully')
            return redirect('admindashboard')
    context={'form':form}
    return render(request,'admin1/changepassword.html',context)


