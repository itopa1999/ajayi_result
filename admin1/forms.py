from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.forms import ModelForm
from django.forms.widgets import NumberInput
from django.contrib.auth.models import User
from .models import *



class UserForm1(UserCreationForm):
    class Meta:
        model = User
        fields = ['last_name','email','first_name','username','password1', 'password2']
        
        
        
class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','email','password1', 'password2']
        


class StudentForm(forms.ModelForm):
    
    departmentID=forms.ModelChoiceField(queryset=Department.objects.all(),empty_label="Choose Department", to_field_name="id")
    facultyID=forms.ModelChoiceField(queryset=Faculty.objects.all(),empty_label="Choose Faculty", to_field_name="id")
    class Meta:
        model = Student
        fields = '__all__'
        exclude=['department','faculty']
        
        
class StudentForm1(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        
        
class LecturerForm(forms.ModelForm):
    class Meta:
        model = Lecturer
        fields = '__all__'
        exclude=['user','username']
        
        
class ResultForm(forms.ModelForm):
    studentID=forms.ModelChoiceField(queryset=Student.objects.all(),empty_label="Choose Student", to_field_name="id")
    courseID=forms.ModelChoiceField(queryset=Course.objects.all(),empty_label="Choose Course", to_field_name="id")
    class Meta:
        model = Result
        fields = '__all__'
        exclude=['student','course','grade','qp']
        

class ResultForm1(forms.ModelForm):
    class Meta:
        model = Result
        fields = '__all__'
        exclude=['grade','qp']
        

class FacultyForm(ModelForm):
    class Meta:
        model = Faculty
        fields = '__all__'
        
class DepartmentForm(ModelForm):
    facultyID=forms.ModelChoiceField(queryset=Faculty.objects.all(),empty_label="Choose Faculty", to_field_name="id")
    class Meta:
        model = Department
        fields = '__all__'
        exclude=['faculty']
        
class DepartmentForm1(ModelForm):
    class Meta:
        model = Department
        fields = '__all__'    
        
        
        
class CourseForm(ModelForm):
    departmentID=forms.ModelChoiceField(queryset=Department.objects.all(),empty_label="Choose Department", to_field_name="id")
    facultyID=forms.ModelChoiceField(queryset=Faculty.objects.all(),empty_label="Choose Faculty", to_field_name="id")
    lecturerID=forms.ModelChoiceField(queryset=Lecturer.objects.all(),empty_label="Choose Lecturer", to_field_name="id")

    class Meta:
        model = Course
        fields = '__all__'
        exclude=['department','faculty','lecturer']
        
        
class CourseForm1(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        
        
class PasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = '__all__'