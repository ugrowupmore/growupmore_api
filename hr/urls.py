from django.urls import path, include
from rest_framework.routers import DefaultRouter
from hr.views import (
    BranchViewSet,
    BranchDepartmentViewSet,
    BranchDocumentViewSet,
    BranchPhotoViewSet,
    EmployeeViewSet,
    EmployeeContactViewSet,
    EmployeeDocumentViewSet,
    EmployeeBanksViewSet,
)

# Registering the ViewSets with the router
router = DefaultRouter()
router.register(r'branches', BranchViewSet, basename='branch')
router.register(r'branch-departments', BranchDepartmentViewSet, basename='branch-department')
router.register(r'branch-documents', BranchDocumentViewSet, basename='branch-document')
router.register(r'branch-photos', BranchPhotoViewSet, basename='branch-photo')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'employee-contacts', EmployeeContactViewSet, basename='employee-contact')
router.register(r'employee-documents', EmployeeDocumentViewSet, basename='employee-document')
router.register(r'employee-banks', EmployeeBanksViewSet, basename='employee-bank')


# Including router URLs in urlpatterns
urlpatterns = [
    path('', include(router.urls)),
]
