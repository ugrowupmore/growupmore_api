# authuser/urls.py

from django.urls import path
from .views.student import (
    StudentRegisterView, StudentActivateView, StudentLoginView, StudentLogoutView,
    StudentChangePasswordView, StudentForgotPasswordView, StudentPasswordResetView,
    StudentProfileView
)
from .views.employee import (
    EmployeeRegisterView, EmployeeActivateView, EmployeeLoginView, EmployeeLogoutView,
    EmployeeChangePasswordView, EmployeeForgotPasswordView, EmployeePasswordResetView,
    EmployeeProfileView
)
from .views.instructor import (
    InstructorRegisterView, InstructorActivateView, InstructorLoginView, InstructorLogoutView,
    InstructorChangePasswordView, InstructorForgotPasswordView, InstructorPasswordResetView,
    InstructorProfileView
)
from .views.institute import (
    InstituteRegisterView, InstituteActivateView, InstituteLoginView, InstituteLogoutView,
    InstituteChangePasswordView, InstituteForgotPasswordView, InstitutePasswordResetView,
    InstituteProfileView
)
from .views.base import TestCaptchaView

urlpatterns = [
    # Student URLs
    path('student/register/', StudentRegisterView.as_view(), name='student-register'),
    path('student/activate/<str:token>/', StudentActivateView.as_view(), name='student-activate'),
    path('student/login/', StudentLoginView.as_view(), name='student-login'),
    path('student/logout/', StudentLogoutView.as_view(), name='student-logout'),
    path('student/change-password/', StudentChangePasswordView.as_view(), name='student-change-password'),
    path('student/forgot-password/', StudentForgotPasswordView.as_view(), name='student-forgot-password'),
    path('student/reset-password/<str:token>/', StudentPasswordResetView.as_view(), name='student-password-reset'),
    path('student/profile/', StudentProfileView.as_view(), name='student-profile'),

    # Employee URLs
    path('employee/register/', EmployeeRegisterView.as_view(), name='employee-register'),
    path('employee/activate/<str:token>/', EmployeeActivateView.as_view(), name='employee-activate'),
    path('employee/login/', EmployeeLoginView.as_view(), name='employee-login'),
    path('employee/logout/', EmployeeLogoutView.as_view(), name='employee-logout'),
    path('employee/change-password/', EmployeeChangePasswordView.as_view(), name='employee-change-password'),
    path('employee/forgot-password/', EmployeeForgotPasswordView.as_view(), name='employee-forgot-password'),
    path('employee/reset-password/<str:token>/', EmployeePasswordResetView.as_view(), name='employee-password-reset'),
    path('employee/profile/', EmployeeProfileView.as_view(), name='employee-profile'),

    # Instructor URLs
    path('instructor/register/', InstructorRegisterView.as_view(), name='instructor-register'),
    path('instructor/activate/<str:token>/', InstructorActivateView.as_view(), name='instructor-activate'),
    path('instructor/login/', InstructorLoginView.as_view(), name='instructor-login'),
    path('instructor/logout/', InstructorLogoutView.as_view(), name='instructor-logout'),
    path('instructor/change-password/', InstructorChangePasswordView.as_view(), name='instructor-change-password'),
    path('instructor/forgot-password/', InstructorForgotPasswordView.as_view(), name='instructor-forgot-password'),
    path('instructor/reset-password/<str:token>/', InstructorPasswordResetView.as_view(), name='instructor-password-reset'),
    path('instructor/profile/', InstructorProfileView.as_view(), name='instructor-profile'),

    # Institute URLs
    path('institute/register/', InstituteRegisterView.as_view(), name='institute-register'),
    path('institute/activate/<str:token>/', InstituteActivateView.as_view(), name='institute-activate'),
    path('institute/login/', InstituteLoginView.as_view(), name='institute-login'),
    path('institute/logout/', InstituteLogoutView.as_view(), name='institute-logout'),
    path('institute/change-password/', InstituteChangePasswordView.as_view(), name='institute-change-password'),
    path('institute/forgot-password/', InstituteForgotPasswordView.as_view(), name='institute-forgot-password'),
    path('institute/reset-password/<str:token>/', InstitutePasswordResetView.as_view(), name='institute-password-reset'),
    path('institute/profile/', InstituteProfileView.as_view(), name='institute-profile'),

    # Test reCAPTCHA Endpoint
    path('test-captcha/', TestCaptchaView.as_view(), name='test-captcha'),
]
