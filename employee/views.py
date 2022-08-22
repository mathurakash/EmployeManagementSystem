import mimetypes
from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse
from .myforms import (
Employee_Register,Employeelogin,Profile,Project, 
QuestionsForm,UpdateQuizScheduleForm,TodayReportForm,ToDOForm,SalaryForm,
LeaveManagementForm, UpdateEmployee,QuizScheduleForm)
from .models import (
Employee, LeaveManagement,LoginDetails,ProjectDetails, 
Questions, SaleryDetails,TodayReport,Todo,FileUpload,LeaveManagement,QuizSchedule, 
UserResponse,Result)
from django.contrib.auth.hashers import make_password
from datetime import datetime, date
from calendar import HTMLCalendar
from django.core.files.storage import FileSystemStorage
from .models import FileUpload
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from dateutil import relativedelta
import os
# Create your views here.


############# CALENDER CODE #######################################
def calculator():
    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    cal=HTMLCalendar().formatmonth(currentYear,currentMonth,currentDay) 
    return cal
############# LOGIN #############################################
def index(request):
    f=Employeelogin(request.POST or None)
    if f.is_valid():
        
        e = f.cleaned_data.get("email")
        obj = Employee.objects.get(email=e)
        request.session['user_log']={'id':obj.id,'fname':obj.fname,'lname':obj.lname,'email':obj.email}
        
        try:
            user_data=LoginDetails.objects.get(employee=e)

            for key ,value_list in user_data.logtime[-1].items():
                if key == str(date.today()):
                    value_list.append(str(datetime.now().time()))
                    user_data.save()
                else:
                    user=LoginDetails.objects.get(employee=e)
                    dict_for_datetime={}
                    list_for_time=[]
                    date_today=str(date.today())
                    time_now= str(datetime.now().time())
                    list_for_time.append(time_now)
                    dict_for_datetime[date_today]=list_for_time
                    user_data.logtime.append(dict_for_datetime)
                    user_data.save()
                
        except:
            l=LoginDetails()
            l.employee=e
            l.logtime=list()
            l.save()
            user=LoginDetails.objects.get(employee=e)
            dict_for_datetime={}
            list_for_time=[]
            date_today=str(date.today())
            time_now= str(datetime.now().time())
            list_for_time.append(time_now)
            dict_for_datetime[date_today]=list_for_time
            user.logtime.append(dict_for_datetime)
            user.save()

        return redirect("employee:dashboard")
    return render(request,'employee/index.html',{'form':f})    



########### REGISTER ############################################
def EmployeeSignup(request):
    if request.method=="GET":
        f=Employee_Register()
        return render(request,'employee/register.html',{'form':f})
    else:
        f=Employee_Register(request.POST ,request.FILES)
        if f.is_valid():
            sel=f.save(commit=False)    
            p=f.cleaned_data.get('password')
            encp = make_password(p)
            sel.password=encp
            sel.save()
            user=User()
            user.username=request.POST.get('username')
            user.password=make_password(request.POST.get('password'))
            user.save()
            return redirect("employee:index")
    return render(request,'employee/register.html',{'form':f})




######################### LOGOUT #########################################
def logout(request,pk):
    
    user=LoginDetails.objects.get(employee=request.session['user_log']['email'])
    
    if not user.outtime:
        list_for_time=[]
        dict_for_all_data={}
        date_today=str(date.today())
        time_now= str(datetime.now().time())
        list_for_time.append(time_now)
        dict_for_all_data[date_today]=list_for_time
        user.outtime.append(dict_for_all_data)
        user.save()
    else:
       
        for key ,value_list in  user.outtime[-1].items():
            if str(key) == str(date.today()):
                value_list.append(str(datetime.now().time()))
                user.save()
            else:
                user=LoginDetails.objects.get(employee=request.session['user_log']['email'])
                dict_for_datetime={}
                list_for_time=[]
                date_today=str(date.today())
                time_now= str(datetime.now().time())
                list_for_time.append(time_now)
                dict_for_datetime[date_today]=list_for_time
                user.outtime.append(dict_for_datetime)
                user.save()
               
    request.session.pop("user_log")
    return redirect("employee:index") 

########################### DASHBOARD ##########################################
def dashboard(request):
    if request.session.get('user_log'):
        cal=calculator()
        data=LoginDetails.objects.get(employee=request.session["user_log"]['email'])
        tym=str(date.today().strftime("%m"))
        nym=str((date.today()+relativedelta.relativedelta(months=1)).strftime("%m"))
        thismonthbirthday=Employee.objects.filter(dob__month=tym).order_by('dob')
        nextmonthbirthday=Employee.objects.filter(dob__month=nym).order_by('dob')
        todaydate=date.today()
        tm=str(date.today().strftime("%m"))
        nmd=str((date.today()+relativedelta.relativedelta(months=1)).strftime("%m"))
        thismonthaniversary=Employee.objects.filter(joiningdate__month=tm).order_by('joiningdate')
        for i in thismonthaniversary:
        
            if i.joiningdate.month == todaydate.month and i.joiningdate.day == todaydate.day:
                
                if i.increment=="False":
                    i.workeniversary+=1
                    i.increment='True'
                    i.save()
        nextmonthaniversary=Employee.objects.filter(joiningdate__month=nmd).order_by('joiningdate')    
        for j in nextmonthaniversary:
            j.increment='False'
            j.save()
        
        todaydate=date.today()
        emp=Employee.objects.get(id=request.session["user_log"]['id'])
        for i in data.logtime :
            if str(date.today()) in i:
                login_date=date.today()
                login_time=i[str(date.today())]
        fixed_time="11:00:00:00"
        context_data={
                        'calender':cal,
                        'login_date':login_date,
                        'login_time':login_time,
                        'img':emp,
                        'thismonthbirthday':thismonthbirthday,
                        'nextmonthbirthday':nextmonthbirthday,
                        'todaydate':todaydate,
                        'thismonthaniversary':thismonthaniversary,
                        'nextmonthaniversary':nextmonthaniversary
                    }
        return render(request,'employee/dashboard.html',context_data)
    else:
        return redirect('employee:index')

###################### PROFILE ########################################
def profile(request,pk):
    if request.session.get('user_log'):
        if request.method=="GET":
            emp=Employee.objects.get(pk=pk)
            f=Profile(instance=emp)
            emp=Employee.objects.get(id=request.session["user_log"]['id'])
            context_data={
                            'form':f,
                            'emp':emp,
                            'img':emp
                        }
            return render(request,'employee/profile.html',context_data)
        else:
            emp=Employee.objects.get(pk=pk)
            f=Profile(request.POST,request.FILES,instance=emp)
            if f.is_valid():
                f.save()
            return redirect("employee:dashboard")
    else:
        return redirect('employee:index')
 
    
############################### ATTENDANCE ##########################################
def attendance(request):
    if request.session.get('user_log'):
        cal=calculator()
        email=request.session['user_log']['email']
        print(email)
        data=LoginDetails.objects.get(employee=email)
        for i in data.logtime :
            if str(date.today()) in i:
                login_date=date.today()
                login_time=i[str(date.today())]
        final_logindata=data.logtime  
        final_logoutdata=data.outtime
        fixed_time="11:00:00:00"
        newdate=date.today()
        tdm=str(date.today().strftime("%Y-%m"))
        emp=Employee.objects.get(id=request.session["user_log"]['id'])
        context_data={
                        'cal':cal,
                        'tdm':tdm,
                        'fixed_time':fixed_time,
                        'final_data':final_logindata,
                        'final_logoutdata':final_logoutdata,
                        'login_date':login_date,
                        'login_time':login_time,
                        'img':emp
                    }
        return render(request,'employee/attendance.html',context_data)
    else:
        return redirect('employee:index')

############################ PROJECT ASSIGN ##########################################
def projectdetail(request):
    if request.session.get('user_log'):
        if request.method=="GET":
            f=Project()
            cal=calculator()
            emp=Employee.objects.get(id=request.session['user_log']['id'])
            data=ProjectDetails.objects.all()
            context_data={
                            'form':f,
                            'data':data,
                            'cal':cal,
                            'img':emp
                        }
            return render(request,'employee/projectassign.html',context_data)
        else:
            f=Project(request.POST)
            if f.is_valid():
                f.save()
            return redirect("employee:projectdetail")
    else:
        return redirect('employee:index')
######################### DELETE PROJECT ###############################################
def delete_project(request,pk):
    if request.session.get('user_log'):
        project=ProjectDetails.objects.get(id=pk)
        project.delete()
        return redirect("employee:projectdetail")
    else:
        return redirect('employee:index')

############################ PROJECT ASSIGN TO ME #####################################
def assign_project_to_me(request):
    if request.session.get('user_log'):
        emp=Employee.objects.get(id=request.session['user_log']['id'])
        data=ProjectDetails.objects.filter(assign_to=emp)
        cal=calculator()
        context_data={
                        'data':data,
                        'cal':cal,
                        'img':emp
                    }
        return render(request,'employee/assign_project_to_me.html',context_data)
    else:
        return redirect('employee:index')

########################## PROJECT REPORT ##############################################
def create_project_report(request):
    if request.session.get('user_log'):
        if request.method=="GET":
            emp=Employee.objects.get(id=request.session['user_log']['id'])
            data=ProjectDetails.objects.filter(assign_to=emp)
            f=TodayReportForm()
            context_data={
                            'form':f,
                            'data':data,
                            'img':emp
                        }
            return render(request,'employee/create_project_report.html',context_data)
        else:
            f=TodayReportForm(request.POST)
            if f.is_valid():
                object = f.save(commit=False)
                project=ProjectDetails.objects.filter(name=request.POST.get('project')).first()
                object.pname=project
                emp=Employee.objects.get(id=request.session['user_log']['id'])
                object.ename=emp
                object.save()
            return redirect("employee:create_project_report")
    else:
        return redirect('employee:index')
###################### PROJECT REPORT LIST ##########################################
def project_report_list(request):
    if request.session.get("user_log"):
        emp=Employee.objects.get(id=request.session['user_log']['id'])
        project=TodayReport.objects.filter(ename=emp)
        return render(request,'employee/project_report_list.html',{'data':project,'img':emp})
    else:
        return redirect('employee:index')

#################### TO DO LIST ##############################################
def to_do(request):
    if request.session.get('user_log'):
        if request.method=="GET":
            f=ToDOForm()
            emp1=Employee.objects.get(id=request.session['user_log']['id'])
            task=Todo.objects.filter(emp=emp1,date=date.today())
            context_data={
                            'tasks':task,
                            'form':f,
                            'img':emp1
                        }
            return render(request,'employee/to_do.html',context_data)
        else:
            f=ToDOForm(request.POST)
            if f.is_valid():
                object = f.save(commit=False)
                emp=Employee.objects.get(id=request.session['user_log']['id'])
                object.emp=emp
                object.date=date.today()
                object.status='PENDING'
                object.save()
            return redirect('employee:to_do')
    else:
        return redirect('employee:index')
################### DELETE TASK ################################################
def delete_task(request,pk):
    if request.session.get('user_log'):
        task=Todo.objects.get(id=pk)
        task.delete()
        return redirect('employee:to_do')
    else:
        return redirect('employee:index')
################# UPDATE TASK #################################################
def update_task(request,pk):
    if request.session.get('user_log'):
        task=Todo.objects.get(id=pk)
        task.status="COMPLETED"
        task.save()
        return redirect('employee:to_do')
    else:
        return redirect('employee:index')
#################### SHOW FUN IMAGE ##################################################

def image_upload(request):
    if request.session.get('user_log'):
        if request.method=="POST":
            files = request.FILES.getlist('document')
            a=[]
            if files:
                for file in files:
                    fs = FileSystemStorage()
                    filename = fs.save(file.name, file)
                    file_url = fs.url(filename)
                    a.append(file_url)
                
                fileurl=FileUpload(fileurl=a)
                messages.success(request,'images uploaded successfully.....')
                fileurl.save()
            
            return HttpResponseRedirect('/')
        else:
            images=FileUpload.objects.all()
            datadict={}
            for i in images:
                newid=i.id
                newfile=((i.fileurl).lstrip('[')).rstrip(']')
                a=((newfile.replace("'","")).replace(" ","")).split(",")
                for j in a:
                        datadict[j[7:]]=newid
                print(datadict)
            emp=Employee.objects.get(id=request.session["user_log"]['id'])
            context_data={
                            'images':images,
                            'data':datadict,
                            'img':emp
                        }
            return render(request,'employee/fun_images.html',context_data)
    else:
        return redirect('employee:index')
################ Generate SALARY SLIP #############################
def salary_slip(request):
    if request.session.get('user_log'):
        if request.method=="POST":
            month=request.POST.get('month')
            emp=Employee.objects.get(id=request.session['user_log']['id'])
            salary=salary=SaleryDetails.objects.get(employee=emp)
            context_data={
                            'month':month,
                            'emp':emp,
                            'salary':salary,
                            'img':emp
                        }
            return render(request,'employee/generate_salary_slip.html',context_data)   
        else:
            return render(request,'employee/generate_salary_slip.html')
    else:
        return redirect('employee:index')

################ Add SALARY Details #############################
def add_salary_details(request):
    if request.session.get('user_log'):
        if request.method=="GET":
            f=SalaryForm()
            salary=SaleryDetails.objects.all()
            emp=Employee.objects.get(id=request.session["user_log"]['id'])
            context_data={
                            'form':f,
                            'salary':salary,
                            'img':emp
                        }
            return render(request,'employee/add_salary_details.html',context_data)
        else:
            f=SalaryForm(request.POST)
            if f.is_valid():
                f.save()
            return redirect("employee:add_salary_details")
    else:
        return redirect('employee:index')

##################################################################
############### Leave Management Start ###########################
##################################################################
def generate_leave(request):
    if request.session.get('user_log'):
        if request.method=="GET":
            f=LeaveManagementForm()
            emp=Employee.objects.get(id=request.session["user_log"]['id'])
            return render(request,'employee/generate_leave.html',{'form':f,'img':emp})
        else:
            f=LeaveManagementForm(request.POST)
            if f.is_valid():
                object = f.save(commit=False)
                emp=Employee.objects.get(id=request.session['user_log']['id'])
                object.employee=emp
                object.save()
                return redirect("employee:generate_leave")
    else:
        return redirect('employee:index')

def leave_list(request):
    if request.session.get('user_log'):
        emp=Employee.objects.get(id=request.session["user_log"]['id'])
        leaves=LeaveManagement.objects.filter(employee=emp)
        return render(request,'employee/leave_list.html',{'leaves':leaves,'img':emp})
    else:
        return redirect('employee:index')


def leave_approval(request):
    if request.session.get('user_log'):
        if request.method=="GET":
            emp=Employee.objects.get(id=request.session["user_log"]['id'])
            leaves=LeaveManagement.objects.all()
            return render(request,'employee/leave_approval.html',{'leaves':leaves,'img':emp})
        else:
            leaves=LeaveManagement.objects.get(id=request.POST.get('leaveid'))
            leaves.rejectionreason=request.POST.get('textarea')
            leaves.status='Rejected'
            print(request.POST.get('textarea'),'======================')
            leaves.save()
            return redirect('employee:leave_list')
    else:
        return redirect('employee:index')

def acceptleave(request,pk):
    if request.session.get('user_log'):
        emp=Employee.objects.get(id=request.session["user_log"]['id'])
        leaves=LeaveManagement.objects.get(id=pk)
        leaves.status='Accepted'
        leaves.save()
        return redirect('employee:leave_approval')
    else:
        return redirect('employee:index')


def rejectleave(request,pk):
    if request.session.get('user_log'):
        emp=Employee.objects.get(id=request.session["user_log"]['id'])
        leaves=LeaveManagement.objects.get(id=pk)
        leaves.status='Rejected'
        leaves.save()
        return redirect('employee:leave_approval')
    else:
        return redirect('employee:index')

##################################################################
############### Leave Management End ###########################
##################################################################

def break_timings(request):
    if request.session.get('user_log'):
        emp=Employee.objects.get(id=request.session["user_log"]['id'])
        return render(request,'employee/break_timings.html',{'img':emp})
    else:
        return redirect('employee:index')
def technology_stack(request):
    if request.session.get('user_log'):
        emp=Employee.objects.get(id=request.session["user_log"]['id'])
        return render(request,'employee/technology_stack.html',{'img':emp})
    else:
        return redirect('employee:index')

##################### ALL EMPLOYEES DETAILS ###############################
def all_employees(request):
    if request.session.get('user_log'):
        emp=Employee.objects.get(id=request.session["user_log"]['id'])
        allemp=Employee.objects.all()
        return render(request,'employee/employees.html',{'allemp':allemp,'emp':emp,'img':emp})
    else:
        return redirect('employee:index')

def delete_employee(request,pk):
    if request.session.get('user_log'):
        emp=Employee.objects.get(id=pk)
        emp.delete()
        allemp=Employee.objects.all()
        return render(request,'employee/employees.html',{'allemp':allemp,'emp':emp,'img':emp})
    else:
        return redirect('employee:index')

def update_employee(request,pk):
    if request.session.get('user_log'):
        if request.method=="GET":
            emp=Employee.objects.get(id=pk)
            f=UpdateEmployee(instance=emp)
            emp=Employee.objects.get(id=request.session["user_log"]['id'])
            return render(request,'employee/update_employee.html',{'form':f,'img':emp})
        else:
            emp=Employee.objects.get(id=pk)
            f=UpdateEmployee(request.POST,request.FILES,instance=emp)
            if f.is_valid():
                f.save()
                emp=Employee.objects.get(id=request.session["user_log"]['id'])
                allemp=Employee.objects.all()
                return render(request,'employee/employees.html',{'allemp':allemp,'emp':emp,'img':emp})
    else:
        return redirect('employee:index')




######################### Dumy test ##############################


def schedule_quiz(request):
    if request.method=="GET":
        f=QuizScheduleForm()
        emp=Employee.objects.get(id=request.session['user_log']['id'])
        quizSchedules=QuizSchedule.objects.all()
        return render(request,'employee/schedule_quiz.html',{'form':f,'QuizSchedules':quizSchedules,'img':emp})
    else:
        emp=Employee.objects.get(id=request.session['user_log']['id'])
        f=QuizScheduleForm(request.POST)
        if f.is_valid():
            object = f.save(commit=False)
            object.quiz_by=emp
            object.save()
        f=QuizScheduleForm()
        quizSchedules=QuizSchedule.objects.all()
        return render(request,'employee/schedule_quiz.html',{'form':f,'QuizSchedules':quizSchedules,'img':emp})

def update_quiz_schedule(request,pk):   
    if request.method=="GET":
        emp=Employee.objects.get(id=request.session['user_log']['id'])
        quiz=QuizSchedule.objects.get(id=pk)
        print(quiz,'=::::::::::::::::::::::::::::::::::::::::')
        f=UpdateQuizScheduleForm(instance=quiz)
        return render(request,'employee/update_quizschedule_quiz.html',{'form':f,'img':emp})
    else:
        emp=Employee.objects.get(id=request.session['user_log']['id'])
        quiz=QuizSchedule.objects.get(id=pk)
        f=UpdateQuizScheduleForm(request.POST,instance=quiz)
        if f.is_valid():
            object = f.save(commit=False)
            object.quiz_by=emp
            object.save()
        f=QuizScheduleForm()
        return redirect('employee:schedule_quiz')


def delete_quiz_schedule(request,pk):
    quiz=QuizSchedule.objects.get(id=pk)
    quiz.delete()
    f=QuizScheduleForm()
    quizSchedules=QuizSchedule.objects.all()
    emp=Employee.objects.get(id=request.session['user_log']['id'])
    return redirect('employee:schedule_quiz')


def add_questions(request):
    if request.method=="GET":
        f=QuestionsForm()
        emp=Employee.objects.get(id=request.session['user_log']['id'])
        return render(request,'employee/add_questions.html',{'form':f,'img':emp})
    else:
        emp=Employee.objects.get(id=request.session['user_log']['id'])
        f=QuestionsForm(request.POST)
        if f.is_valid():
            object = f.save(commit=False)
            object.quiz_by=emp
            object.options.append(request.POST.get('A'))
            object.options.append(request.POST.get('B'))
            object.options.append(request.POST.get('C'))
            object.options.append(request.POST.get('D'))
            object.save()
        f=QuizScheduleForm()
    return render(request,'employee/schedule_quiz.html',{'form':f,'img':emp})

def test_window(request):

    emp=Employee.objects.get(id=request.session['user_log']['id'])
    results=UserResponse.objects.filter(username=emp)
    todaydate=date.today()
    todaytime=datetime.now()
    quizSchedules=QuizSchedule.objects.filter(starttime__date = todaydate)
    return render(request,'employee/test_window.html',{'todaytime':todaytime,'quizSchedules':quizSchedules,'results':results,'img':emp})

def test_start(request,pk):
    if request.method=="GET":
        quiz=QuizSchedule.objects.get(id=pk)
        try:
            useresponse=UserResponse.objects.get(username=request.session['user_log']['id'],subject=quiz.subject)
            return redirect('employee:test_window')
        except:

            quiz=QuizSchedule.objects.get(id=pk)
            endtime=quiz.endtime
            subject=quiz.subject
            questions=Questions.objects.filter(quiz=quiz)
            presentdatetime=datetime.now()
            return render(request,'employee/test_start.html',{'questions':questions,'endtime':endtime,'datetime':presentdatetime,'subject':subject})
    else:
        quiz=QuizSchedule.objects.get(id=pk)
        questions=Questions.objects.filter(quiz=quiz)
        uresponse=UserResponse()
        emp=Employee.objects.get(id=request.session["user_log"]['id'])
        uresponse.username=emp
        uresponse.datetime=datetime.now()
        
        for i in questions:
            # print(i.id,'===========================')
            response_list=[]
            response_list.append(i.question)
            response_list.append(i.correct_option)
            response_list.append(request.POST.get('question'+str(i.id)))
            if i.correct_option == request.POST.get('question'+str(i.id)):
                response_list.append("correct")
            else:
                response_list.append("incorrect")
            uresponse.userresponse.append(response_list)
        uresponse.subject=quiz.subject
        uresponse.save()
        quizSchedules=QuizSchedule.objects.all()
        return redirect('employee:test_window')

def action_page(request,pk):
    emp=Employee.objects.get(id=request.session['user_log']['id'])
    result=UserResponse.objects.get(id=pk)
    correct=0
    questions=0
    for i in result.userresponse:
        questions+=1
        if i[3]=="correct":
            correct+=1
    percentage=round((correct/questions)*100,2)
    incorrect=questions-correct
    finalresult=Result()
    finalresult.emp=emp
    finalresult.userresponse=result
    finalresult.correct=correct
    finalresult.incorrect=incorrect
    finalresult.percentage=percentage
    finalresult.save()
    return render(request,'employee/action_page.html',{'result':result,'correct':correct,'questions':questions,'percentage':percentage,'incorrect':incorrect,'img':emp})



def my_results(request,pk):
    emp=Employee.objects.get(id=pk)
    result=Result.objects.filter(emp=emp)
    return render(request,'employee/my_results.html',{'result':result,'img':emp})

def all_results(request):
    emp=Employee.objects.get(id=request.session['user_log']['id'])
    result=Result.objects.all()
    return render(request,'employee/all_results.html',{'result':result,'img':emp})





from .models import TestFile
from rest_framework.response import Response
from rest_framework import generics
from .serializers import TestSerializer
class TestView(generics.CreateAPIView):
    queryset = TestFile.objects.all()
    serializer_class = TestSerializer
    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file", None)
        if file is not None:
            file = TestFile.objects.create(
                name = "A",
                file = file
            )
        return Response({"mssg": "File is uploaded"})


# def download_file(request):
#     # Define Django project base directory
#     BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     # Define text file name
#     # filename = 'test.txt'
#     file = TestFile.objects.get(name="A").file
#     # Define the full file path
#     filepath = BASE_DIR + '/media/' + file.name
#     # Open the file for reading content
#     path = open("parh", 'rb')
#     # Set the mime type
#     mime_type, _ = mimetypes.guess_type(filepath)
#     # Set the return value of the HttpResponse
#     # str = unicode(str, errors='ignore')
#     response = HttpResponse(path, content_type=mime_type)
#     # Set the HTTP header for sending to browser
#     response['Content-Disposition'] = "attachment; filename=%s" % file.name
#     # Return the response value
#     return response


from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
def download_file(request): 
    drawing = svg2rlg("/home/baliram/Desktop/Bluthink Akash/BlueThinkClone/EMP/0708c1b4-5d9d-5b40-9ff4-0e87c26454e6.svg")
    # scaleFactor = 1./0.3527
    # drawing.width *= scaleFactor
    # drawing.height *= scaleFactor
    # drawing.scale(scaleFactor, scaleFactor)
    renderPDF.drawToFile(drawing, "file.pdf")