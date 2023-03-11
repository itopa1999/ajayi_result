from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Faculty(models.Model):
    name=models.CharField(max_length=50, null=True, blank=True)
    hof=models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class Department(models.Model):
    name=models.CharField(max_length=50, null=True, blank=True)
    faculty=models.ForeignKey(Faculty, on_delete=models.CASCADE)
    hod=models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class Lecturer(models.Model):
    user= models.OneToOneField(User, null=True, blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    staff_ID = models.CharField(max_length=200,null=True)
    faculty = models.ForeignKey(Faculty, null=True, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, null=True, on_delete=models.CASCADE)
    phone_no = models.IntegerField(blank=True, null=True)
    email = models.EmailField(max_length=200,  blank=True,null=True)
    username=models.CharField(max_length=200, blank=True,null=True,)
    
    def __str__(self):
        return self.name

class Course(models.Model):
    SEMESTER =(
        ('ND1 first Semester', 'ND1 first Semester'),('ND1 second Semester', 'ND1 second Semester'),
        ('ND2 first Semester', 'ND2 first Semester'),('ND2 second Semester', 'ND2 second Semester'),
        ('HND1 first Semester', 'HND1 first Semester'),('HND1 second Semester', 'HND1 second Semester'),
        ('HND2 first Semester', 'HND2 first Semester'),('HND2 second Semester', 'HND2 second Semester')
    )
    name=models.CharField(max_length=50, null=True, blank=True)
    course_unit=models.IntegerField(null=True, blank=True)
    semester=models.CharField(max_length=200, blank=True,null=True, choices=SEMESTER)
    department=models.ForeignKey(Department, on_delete=models.CASCADE)
    faculty=models.ForeignKey(Faculty, on_delete=models.CASCADE)
    lecturer=models.ForeignKey(Lecturer,null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name


class Student(models.Model):
    LEVEL=(
        ('ND', 'ND'),('HND','HND'),
    )
    PROGRAM=(
        ('FULL-TIME','FULL-TIME'),('PART-TIME','PART-TIME')
    )
    name=models.CharField(max_length=50, null=True, blank=True)
    matric_no=models.CharField(max_length=50, null=True, blank=True)
    email=models.EmailField(max_length=50, null=True, blank=True)
    level=models.CharField(max_length=50, null=True, blank=True, choices=LEVEL)
    program=models.CharField(max_length=50, null=True, blank=True, choices=PROGRAM)
    department=models.ForeignKey(Department, on_delete=models.CASCADE)
    faculty=models.ForeignKey(Faculty, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
   
class Result(models.Model):
    student= models.ForeignKey(Student,blank=True,null=True, on_delete=models.CASCADE) 
    course= models.ForeignKey(Course,blank=True,null=True, on_delete=models.CASCADE)
    cu=models.IntegerField(blank=True,null=True)
    exam_score=models.IntegerField(blank=True,null=True)
    test_score=models.IntegerField(blank=True,null=True)
    attendant_score=models.IntegerField(blank=True,null=True)
    grade= models.CharField(max_length=200, blank=True,null=True)  
    qp=models.CharField(max_length=3,blank=True,null=True)
    lecturer=models.ForeignKey(Lecturer,null=True, blank=True,on_delete=models.CASCADE)
    def save(self):
        total_score=(self.exam_score + self.test_score + self.attendant_score)
        if total_score >=75:
            self.qp =self.cu *4.00
            self.grade =("A")
        elif total_score <=74 and total_score >=70 :
            self.qp =self.cu *3.5
            self.grade =("AB")
        elif total_score <=69 and total_score >=65 :
            self.qp =self.cu *3.25
            self.grade =("B")
        elif total_score <=64 and total_score >=60 :
            self.qp =self.cu *3.00
            self.grade =("BC")
        elif total_score <=59 and total_score >=55 :
            self.qp =self.cu *2.75
            self.grade =("C")
        elif total_score <=54 and total_score >=50 :
            self.qp =self.cu *2.50
            self.grade =("CD")
        elif total_score <=49 and total_score >=45 :
            self.qp =self.cu *2.25
            self.grade =("D")
        elif total_score <=44 and total_score >=40 :
            self.qp =self.cu *2.00
            self.grade =("E")
        else:
            self.qp =self.cu *0
            self.grade =("F")
        return super(Result, self).save()
    
    def __str__(self):
        return f"{self.student}"


