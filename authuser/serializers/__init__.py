# authuser/serializers/__init__.py

from .student import StudentSerializer, StudentProfileSerializer
from .employee import EmployeeSerializer, EmployeeProfileSerializer
from .instructor import InstructorSerializer, InstructorProfileSerializer
from .institute import InstituteSerializer, InstituteProfileSerializer

__all__ = [
    'StudentSerializer',
    'StudentProfileSerializer',
    'EmployeeSerializer',
    'EmployeeProfileSerializer',
    'InstructorSerializer',
    'InstructorProfileSerializer',
    'InstituteSerializer',
    'InstituteProfileSerializer',
]
