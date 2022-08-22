from django.contrib import admin
from .models import Employee,LoginDetails,ProjectDetails,Todo
from .models import TodayReport,FileUpload,SaleryDetails,LeaveManagement
from .models import QuizSchedule,Questions,UserResponse,Result
# Register your models here.

admin.site.register(Employee)
admin.site.register(LoginDetails)
admin.site.register(ProjectDetails)
admin.site.register(TodayReport)
admin.site.register(FileUpload)
admin.site.register(SaleryDetails)
admin.site.register(Todo)
admin.site.register(LeaveManagement)
admin.site.register(QuizSchedule)
admin.site.register(Questions)
admin.site.register(UserResponse)
admin.site.register(Result)
