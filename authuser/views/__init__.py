from .employee import ( 
    EmployeeRegisterView, EmployeeActivateView, EmployeeLoginView, EmployeeLogoutView, 
    EmployeeChangePasswordView, EmployeeForgotPasswordView, EmployeePasswordResetView, EmployeeProfileView )

from .student import ( 
    StudentRegisterView, StudentActivateView, StudentLoginView, StudentLogoutView, 
    StudentChangePasswordView, StudentForgotPasswordView, StudentPasswordResetView, StudentProfileView )

from .institute import ( 
    InstituteRegisterView, InstituteActivateView, InstituteLoginView, InstituteLogoutView, 
    InstituteChangePasswordView, InstituteForgotPasswordView, InstitutePasswordResetView, InstituteProfileView )

from .instructor import ( 
    InstructorRegisterView, InstructorActivateView, InstructorLoginView, InstructorLogoutView, 
    InstructorChangePasswordView, InstructorForgotPasswordView, InstructorPasswordResetView, InstructorProfileView )

__all__ = [
    EmployeeRegisterView, EmployeeActivateView, EmployeeLoginView, EmployeeLogoutView, 
    EmployeeChangePasswordView, EmployeeForgotPasswordView, EmployeePasswordResetView, EmployeeProfileView,
    StudentRegisterView, StudentActivateView, StudentLoginView, StudentLogoutView, 
    StudentChangePasswordView, StudentForgotPasswordView, StudentPasswordResetView, StudentProfileView,
    InstituteRegisterView, InstituteActivateView, InstituteLoginView, InstituteLogoutView, 
    InstituteChangePasswordView, InstituteForgotPasswordView, InstitutePasswordResetView, InstituteProfileView,
    InstructorRegisterView, InstructorActivateView, InstructorLoginView, InstructorLogoutView, 
    InstructorChangePasswordView, InstructorForgotPasswordView, InstructorPasswordResetView, InstructorProfileView
]