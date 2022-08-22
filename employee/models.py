from datetime import datetime
from django.db import models
from jsonfield import JSONField
from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

################ Employee #####################

empstatus =(
    ("Employee", "Employee"),
    ("Admin", "Admin"),
    ("HR", "HR"),
)
 
leavestatus=(
    ("Pending","Pending"),
    ("Accepted","Accepted"),
    ("Rejected","Rejected"),
)

class Employee(models.Model):
    fname=models.CharField(max_length=50)
    lname=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    joiningdate=models.DateField()
    dob=models.DateField()
    phone=models.IntegerField()
    image = models.ImageField(upload_to='media/')
    workeniversary=models.IntegerField(default=0)
    increment=models.CharField(max_length=10,default="False")
    emp_status= models.CharField(max_length = 20,choices = empstatus,default = 'Employee')
    def __str__(self):
        return self.fname+' '+self.lname

################# MONTHLY RATINGS #############################
# class MonthlyRatings(models.Model):
#     employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
#     date=models.DateField()
#     ratings=models.IntegerField()
#     def __str__(self):
#         return self.employee.fname

##################### Login Details ########################
class LoginDetails(models.Model):
    employee=models.CharField(max_length=50)
    date=models.DateField(auto_now=True)
    loginfrom=models.CharField(max_length=50)
    logtime=models.JSONField(blank=True,null=True)
    outtime=models.JSONField(blank=True, null=True,default=list)

    def __str__(self):
        return self.employee


############## SALARY DETAILS #####################

class SaleryDetails(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,unique=True)
    basic=models.IntegerField()
    hra=models.IntegerField()
    ta=models.IntegerField()
    sa=models.IntegerField()
    totalsalary=models.IntegerField()
    def __str__(self):
        return self.employee.email

################ Events ##############################
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


############# Leave Management #######################
class LeaveManagement(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    reason=models.CharField(max_length=250)
    fromdate=models.DateField(blank=True)
    todate=models.DateField(blank=True)
    status=models.CharField(max_length = 20,choices = leavestatus,default = 'Pending')
    rejectionreason=models.CharField(max_length=250,null=True)
    def __str__(self):
        return self.employee.fname


############### Project Details ######################
class ProjectDetails(models.Model):
    name=models.CharField(max_length=250,unique=True)
    cname=models.CharField(max_length=250)
    starttime=models.DateField(blank=True)
    endtime=models.DateField(blank=True)
    assign_to=models.ForeignKey(Employee,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

############## Project Reports #######################
class TodayReport(models.Model):
    pname=models.ForeignKey(ProjectDetails,on_delete=models.CASCADE)
    ename=models.ForeignKey(Employee,on_delete=models.CASCADE)
    tdate=models.CharField(max_length=10)
    workon=RichTextField(blank=True,null=True)

############## TODAYS TO DO TASK ######################
class Todo(models.Model):
    emp=models.ForeignKey(Employee,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    task=models.CharField(max_length=150)
    status=models.CharField(max_length=10)
    



############### FUN IMAGES ############################
class FileUpload(models.Model):
    fileurl=models.TextField(default=None)

############### Quiz schedule #########################
class QuizSchedule(models.Model):
    quiz_by=models.ForeignKey(Employee,on_delete=models.CASCADE)
    starttime=models.DateTimeField()
    endtime=models.DateTimeField()
    subject=models.CharField(max_length=250)
    def __str__(self):
        return self.subject


############## Quiz Questions ##########################
class Questions(models.Model):
    quiz=models.ForeignKey(QuizSchedule,on_delete=models.CASCADE)
    question=RichTextField(blank=True,null=True)
    options=models.JSONField(blank=True, null=True,default=list)
    correct_option=models.CharField(max_length=250)
    def __str__(self):
        return self.question


############# User Response ##############################
class UserResponse(models.Model):
    username=models.ForeignKey(Employee,on_delete=models.CASCADE)
    subject=models.CharField(max_length=50)
    datetime=models.DateTimeField()
    userresponse=models.JSONField(blank=True, null=True,default=list)
    def __str__(self):
        return self.username.fname


########### RESULT TABLE #################################
class Result(models.Model):
    emp=models.ForeignKey(Employee,on_delete=models.CASCADE)
    userresponse=models.ForeignKey(UserResponse,on_delete=models.CASCADE)
    correct=models.IntegerField()
    incorrect=models.IntegerField()
    percentage=models.IntegerField()
    def __str__(self):
        return self.emp.fname



class TestFile(models.Model):
    name = models.CharField(max_length=10)
    file = models.FileField()
    def __str__(self):
        return self.name