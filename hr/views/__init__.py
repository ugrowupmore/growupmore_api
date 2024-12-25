from .branch_department import BranchDepartmentViewSet
from .branch_document import BranchDocumentViewSet
from .branch_photo import BranchPhotoViewSet
from .branch import BranchViewSet
from .employee_bank import EmployeeBanksViewSet
from .employee_contact import EmployeeContactViewSet
from .employee_document import EmployeeDocumentViewSet
from .employee_profile import EmployeeViewSet

__all__ = [
    "BranchDepartmentViewSet",
    "BranchDocumentViewSet",
    "BranchPhotoViewSet",
    "BranchViewSet",
    "EmployeeBanksViewSet",
    "EmployeeContactViewSet",
    "EmployeeDocumentViewSet",
    "EmployeeViewSet",
]