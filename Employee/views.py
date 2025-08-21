from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import Department, Employee, Leave
from .serializer import DepartmentSerializer, EmployeeSerializer, LeaveSerializer



@api_view(["POST"])
def create_department(request):
    serializer = DepartmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(["POST"])
def create_employee(request):
    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)



@api_view(["POST"])
def set_base_salary(request, emp_id):
    try:
        employee = Employee.objects.get(id=emp_id)
        salary = request.data.get("base_salary")
        employee.base_salary = salary
        employee.save()
        return Response({"message": f"Salary updated to {salary}"})
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=404)


# 4. UPDATE - Increase Leave Count
@api_view(["PUT"])
def update_leave(request, emp_id):
    month = request.data.get("month")
    year = request.data.get("year")
    extra_leaves = int(request.data.get("leave_count", 0))

    leave, created = Leave.objects.get_or_create(
        employee_id=emp_id, month=month, year=year,
        defaults={"leave_count": extra_leaves}
    )
    if not created:
        leave.leave_count += extra_leaves
        leave.save()

    return Response(LeaveSerializer(leave).data)


@api_view(["POST"])
def calculate_payable_salary(request, emp_id):
    month = request.data.get("month")
    year = request.data.get("year")

    try:
        employee = Employee.objects.get(id=emp_id)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=404)

    leave = Leave.objects.filter(employee=employee, month=month, year=year).first()
    leave_count = leave.leave_count if leave else 0

    deduction = (employee.base_salary / 25) * leave_count
    payable = employee.base_salary - deduction

    return Response({
        "employee": employee.name,
        "month": month,
        "year": year,
        "base_salary": employee.base_salary,
        "leave_count": leave_count,
        "payable_salary": payable
    })


@api_view(["GET"])
def high_earners(request, dept_id):
    employees = Employee.objects.filter(department_id=dept_id)
    top_salaries = employees.values_list("base_salary", flat=True).distinct().order_by("-base_salary")[:3]
    high_earners = employees.filter(base_salary__in=top_salaries)

    return Response(EmployeeSerializer(high_earners, many=True).data)



@api_view(["GET"])
def high_earners_month(request, month, year):
    employees = Employee.objects.all()
    emp_salaries = []

    for emp in employees:
        leave = Leave.objects.filter(employee=emp, month=month, year=year).first()
        leave_count = leave.leave_count if leave else 0
        deduction = (emp.base_salary / 25) * leave_count
        payable = emp.base_salary - deduction
        emp_salaries.append((emp, payable))

  
    emp_salaries.sort(key=lambda x: x[1], reverse=True)
    top_salaries = list({payable for _, payable in emp_salaries})[:3]

    result = [
        {"id": emp.id, "name": emp.name, "department": emp.department.name, "payable_salary": payable}
        for emp, payable in emp_salaries if payable in top_salaries
    ]

    return Response(result)
