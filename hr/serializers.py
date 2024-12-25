
from rest_framework import serializers

from authuser.models.employee import Employee
from hr.models.branch import Branch
from hr.models.branch_department import BranchDepartment
from hr.models.branch_document import BranchDocument
from hr.models.branch_photo import BranchPhoto
    
from hr.models.employee_banks import EmployeeBanks
from hr.models.employee_contact import EmployeeContact
from hr.models.employee_document import EmployeeDocument

class BranchSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(max_length=200, default="na.png", required=False)    
    branch_type_name = serializers.CharField(source='branch_type.type', read_only=True)
    manager_name = serializers.CharField(source='manager.first_name', read_only=True)
    country_name = serializers.CharField(source='country.name', read_only=True)
    state_name = serializers.CharField(source='state.name', read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True)
    reports_to_name = serializers.CharField(source='reports_to.first_name', read_only=True)

    class Meta:
        model = Branch
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')


class BranchDepartmentSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    country_name = serializers.CharField(source='country.name', read_only=True)
    state_name = serializers.CharField(source='state.name', read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True)
    manager_name = serializers.CharField(source='manager.first_name', read_only=True)

    class Meta:
        model = BranchDepartment
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')


class BranchDocumentSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    document_type_name = serializers.CharField(source='document_type.type', read_only=True)
    document_name = serializers.CharField(source='document.name', read_only=True)
    issue_country_name = serializers.CharField(source='issue_country.name', read_only=True)
    issue_state_name = serializers.CharField(source='issue_state.name', read_only=True)
    issue_city_name = serializers.CharField(source='issue_city.name', read_only=True)

    class Meta:
        model = BranchDocument
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')


class BranchPhotoSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=200, default="na.png", required=False)    
    branch_name = serializers.CharField(source='branch.name', read_only=True)

    class Meta:
        model = BranchPhoto
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')


class EmployeeDetailSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(max_length=200, default="na.png", required=False)
    branch_name = serializers.CharField(source='profile.branch.name', read_only=True)
    nationality_name = serializers.CharField(source='profile.nationality.name', read_only=True)
    country_name = serializers.CharField(source='profile.country.name', read_only=True)
    state_name = serializers.CharField(source='profile.state.name', read_only=True)
    city_name = serializers.CharField(source='profile.city.name', read_only=True)
    department_name = serializers.CharField(source='profile.department.name', read_only=True)
    designation_name = serializers.CharField(source='profile.designation.name', read_only=True)
    manager_name = serializers.CharField(source='profile.manager.first_name', read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')


class EmployeeContactSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.first_name', read_only=True)

    class Meta:
        model = EmployeeContact
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')  


class EmployeeDocumentSerializer(serializers.ModelSerializer):
    document_image = serializers.ImageField(max_length=200, default="na.png", required=False)
    employee_name = serializers.CharField(source='employee.first_name', read_only=True)
    document_type_name = serializers.CharField(source='document_type.type', read_only=True)
    document_name = serializers.CharField(source='document.name', read_only=True)
    issue_country_name = serializers.CharField(source='issue_country.name', read_only=True)
    issue_state_name = serializers.CharField(source='issue_state.name', read_only=True)
    issue_city_name = serializers.CharField(source='issue_city.name', read_only=True)

    class Meta:
        model = EmployeeDocument
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')
 

class EmployeeBanksSerializer(serializers.ModelSerializer):    
    employee_name = serializers.CharField(source='employee.first_name', read_only=True)
    bank_name = serializers.CharField(source='bank.name', read_only=True)
    bank_country_name = serializers.CharField(source='bank_country.name', read_only=True)

    class Meta:
        model = EmployeeBanks
        fields = '__all__'
        read_only_fields = ('id', 'updated_by', 'create_date', 'last_update_date')