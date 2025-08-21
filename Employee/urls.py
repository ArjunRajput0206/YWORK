from django.urls import path
from .views import create_department,create_employee,set_base_salary,update_leave,calculate_payable_salary,high_earners,high_earners_month

urlpatterns = [
    path("departments/", create_department, name="create_department"),
    path("employees/", create_employee, name="create_employee"),
    path("employees/<int:emp_id>/set_salary/", set_base_salary, name="set_salary"),
    path("employees/<int:emp_id>/leaves/", update_leave, name="update_leave"),
    path("employees/<int:emp_id>/payable_salary/", calculate_payable_salary, name="calculate_payable_salary"),
    path("departments/<int:dept_id>/high_earners/", high_earners, name="high_earners"),
    path("high_earners/<int:month>/<int:year>/", high_earners_month, name="high_earners_month"),
]
