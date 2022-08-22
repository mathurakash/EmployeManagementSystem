from .models import Employee,ProjectDetails, Questions, QuizSchedule,TodayReport,SaleryDetails,Todo,LeaveManagement
from django import forms
from django.contrib.auth.hashers import check_password


class DateInput(forms.DateInput):
    input_type = 'date'

class DateTimeInput(forms.DateTimeInput):
    input_type='datetime-local'


class Employee_Register(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput({ "placeholder": "Enter Password"}))
    retype_password=forms.CharField(widget=forms.PasswordInput({ "placeholder": "Confirm Password"}))
    class Meta:
        model=Employee
        fields = ['fname','lname','email','joiningdate','dob','phone','image']
        widgets = {
            'fname':forms.TextInput({ "placeholder": "Enter First Name"}),
            'lname':forms.TextInput({ "placeholder": "Enter Last Name"}),
            'email':forms.TextInput({ "placeholder": "Enter Email Address"}),
            'phone':forms.TextInput({ "placeholder": "Enter Phone Number"}),
            'joiningdate':DateInput(),
            'dob': DateInput(),
        } 

    def clean(self):
        super().clean()
        p=self.cleaned_data.get('password')
        p1=self.cleaned_data.get('retype_password')
        if p!=p1 or len(p)<6:
            raise forms.ValidationError("Error password : Both Password did not match...")

class UpdateEmployee(forms.ModelForm):
    class Meta:
        model=Employee
        fields = ['fname','lname','email','joiningdate','dob','phone','image','emp_status']
        widgets = {
            'fname':forms.TextInput({ "placeholder": "Enter First Name"}),
            'lname':forms.TextInput({ "placeholder": "Enter Last Name"}),
            'email':forms.TextInput({ "placeholder": "Enter Email Address"}),
            'phone':forms.TextInput({ "placeholder": "Enter Phone Number"}),
            'joiningdate':DateInput(),
            'dob': DateInput(),
        }
class Profile(forms.ModelForm):
    class Meta:
        model=Employee
        fields = ['fname','lname','email','dob','phone','image']    
        widgets = {
            'dob': DateInput(),
        } 

class Employeelogin(forms.Form):
    email=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        e=self.cleaned_data.get("email")
        p=self.cleaned_data.get("password")
        try:
            sel=Employee.objects.get(email=e)
        except:
            raise forms.ValidationError("User Does Not Exits")
        else:
            if not check_password(p,sel.password):
                raise forms.ValidationError("Password does not match")

            



class Project(forms.ModelForm):
    class Meta:
        model=ProjectDetails
        fields = ['name','cname','starttime','endtime','assign_to'] 
        widgets = {
            'name':forms.TextInput({ "placeholder": "Enter Project Name"}),
            'cname':forms.TextInput({ "placeholder": "Enter Company Name"}),
            'starttime': DateInput(),
            'endtime': DateInput(),
        } 


class TodayReportForm(forms.ModelForm):
    class Meta:
        model=TodayReport
        fields = ['tdate','workon']
        widgets = {
            'tdate': DateInput(),
        } 

class ToDOForm(forms.ModelForm):
    class Meta:
        model=Todo
        fields = ['task']
        widgets = {
            'task':forms.TextInput({ "placeholder": "Enter Task Name"}),
            
        } 



class SalaryForm(forms.ModelForm):
    class Meta:
        model=SaleryDetails
        fields = ['employee','basic','hra','ta','sa','totalsalary']
        widgets = {
            'basic':forms.TextInput({ "placeholder": "Enter Basic Salary"}),
            'hra':forms.TextInput({ "placeholder": "Enter House Rental Allowence"}),
            'ta':forms.TextInput({ "placeholder": "Enter Travelling Allowence"}),
            'sa':forms.TextInput({ "placeholder": "Enter Special Allowence"}),
            'totalsalary':forms.TextInput({ "placeholder": "Enter Total Salary"}),
        } 


class LeaveManagementForm(forms.ModelForm):
    class Meta:
        model=LeaveManagement
        fields = ['reason','fromdate','todate']
        widgets = {
            'reason':forms.Textarea({ "placeholder": "Enter Leave Reason"}),
            'fromdate':DateInput(),
            'todate':DateInput(),
        }


# class MonthlyRatingsForm(forms.ModelForm):
#     class Meta:
#         model=MonthlyRatings
#         fields = ['date','ratings']
#         widgets={
#             'date':DateInput(),
#             'ratings':forms.Textarea({ "placeholder": "Enter raings b/w 1-10"}),
#         }


################# QUIZ SCHEDULE ##################
class QuizScheduleForm(forms.ModelForm):
    class Meta:
        model=QuizSchedule
        fields=['starttime','endtime','subject']
        widgets={
            'starttime':DateTimeInput(),
            'endtime':DateTimeInput(),
            'subject':forms.TextInput({ "placeholder": "Enter Quiz Subject"}),
        }
class UpdateQuizScheduleForm(forms.ModelForm):
    class Meta:
        model=QuizSchedule
        fields="__all__"
        widgets={
            'starttime':DateTimeInput(),
            'endtime':DateTimeInput(),
            'subject':forms.TextInput({ "placeholder": "Enter Quiz Subject"}),
        }

class QuestionsForm(forms.ModelForm):
    A = forms.CharField(label='Option A', widget=forms.TextInput(attrs={ "placeholder": "Enter Option A"}))
    B = forms.CharField(label='Option B', widget=forms.TextInput(attrs={ "placeholder": "Enter Option B"}))
    C = forms.CharField(label='Option C', widget=forms.TextInput(attrs={ "placeholder": "Enter Option C"}))
    D = forms.CharField(label='Option D', widget=forms.TextInput(attrs={ "placeholder": "Enter Option D"}))
    class Meta:
        model=Questions
        fields=['quiz','question','correct_option']
        widgets={
            
            'correct_option':forms.TextInput({ "placeholder": "Enter correct answer"}),

        }

