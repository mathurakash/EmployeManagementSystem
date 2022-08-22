from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name='employee'

urlpatterns = [
    
    path('',views.index,name="index"),
    path('register/',views.EmployeeSignup,name="register"),
    path('logout/<int:pk>',views.logout,name="logout"),


    path('dashboard/',views.dashboard,name="dashboard"),
    path('dashboard/profile/<int:pk>',views.profile,name="profile"),


    path('attendance/',views.attendance,name="attendance"),


    path('assign_project/',views.projectdetail,name="projectdetail"),
    path('delete_project/<int:pk>/',views.delete_project,name="delete_project"),
    path('assign_project_to_me/',views.assign_project_to_me,name="assign_project_to_me"),


    path('create_project_report/',views.create_project_report,name="create_project_report"),
    path('project_report_list/',views.project_report_list,name="project_report_list"),
    path('to_do/',views.to_do,name="to_do"),
    path('delete_task/<int:pk>/',views.delete_task,name="delete_task"),
    path('update_task/<int:pk>/',views.update_task,name="update_task"),


    path('generate_leave/',views.generate_leave,name="generate_leave"),
    path('leave_list/',views.leave_list,name="leave_list"),
    path('leave_approval/',views.leave_approval,name="leave_approval"),
    path('accept/<int:pk>/',views.acceptleave,name="acceptleave"),
    path('reject/<int:pk>/',views.rejectleave,name="rejectleave"),


    path('image_section/',views.image_upload,name="image_upload"),

    path('generate_salary_slip/',views.salary_slip,name="generate_salary_slip"),
    
    path('add_salary_details/',views.add_salary_details,name="add_salary_details"),


    path('break_timings/',views.break_timings,name="break_timings"),

    path('technology_stack/',views.technology_stack,name="technology_stack"),

    path('all_employees/',views.all_employees,name="all_employees"),
    path('delete_employee/<int:pk>/',views.delete_employee,name="delete_employee"),
    path('update_employee/<int:pk>/',views.update_employee,name="update_employee"),
    
    path('test_window/',views.test_window,name="test_window"),
    

    path('schedule_quiz/',views.schedule_quiz,name="schedule_quiz"),
    path('delete_quiz_schedule/<int:pk>/',views.delete_quiz_schedule,name="delete_quiz_schedule"),
    path('update_quiz_schedule/<int:pk>/',views.update_quiz_schedule,name="update_quiz_schedule"),
    path('add_questions/',views.add_questions,name="add_questions"),
    path('test_start/<int:pk>/',views.test_start,name="test_start"),

    path('action_page/<int:pk>/',views.action_page,name="action_page"),

    path('my_results/<int:pk>/',views.my_results,name="my_results"),

    path('all_results/',views.all_results,name="all_results"),
    path('test', views.TestView.as_view()),
    path('download_file',views.download_file,name="download_file")

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)