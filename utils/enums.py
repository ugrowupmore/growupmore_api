# utils/enums.py

from django.db import models
from django.utils.translation import gettext_lazy as _

# Status Type Enum
class StatusType(models.TextChoices):
    DRAFT = 'draft', _('Draft')
    REVIEW = 'review', _('Review')
    PUBLISHED = 'published', _('Published')

# Designation Level Enum
class DesignationLevel(models.TextChoices):
    ENTRY = 'entry', _('Entry')
    JUNIOR = 'junior', _('Junior')
    MID = 'mid', _('Mid')
    SENIOR = 'senior', _('Senior')
    EXECUTIVE = 'exe', _('Executive')
    LEAD = 'lead', _('Lead')
    OTHER = 'other', _('Other')

# Employee Type Enum
class EmployeeType(models.TextChoices):
    FULL = 'full', _('Full-time')
    PART = 'part', _('Part-time')
    CONTRACT = 'contract', _('Contract')

# Employee Badge Enum
class EmployeeBadge(models.TextChoices):
    SILVER = 'silver', _('Silver')
    GOLD = 'gold', _('Gold')
    DIAMOND = 'diamond', _('Diamond')

# National ID Type Enum
class NationalIDType(models.TextChoices):
    SSN = 'SSN', _('Social Security Number (SSN)')
    NIN = 'NIN', _('National Insurance Number (NIN)')
    AADHAR = 'Aadhar', _('Aadhar')
    PAN = 'PAN', _('PAN')

# Contact Types Enum
class ContactType(models.TextChoices):
    PERSONAL = 'personal', _('Personal')
    WORK = 'work', _('Work')
    EMERGENCY = 'emergency', _('Emergency')    

class Relationship(models.TextChoices):
    SELF = 'self', _('Self')
    FRIEND = 'friend', _('Friend')
    FATHER = 'father', _('Father')
    MOTHER = 'mother', _('Mother')
    SIBLING = 'sibling', _('Sibling')
    COUSIN = 'cousin', _('Cousin')
    NEIGHBOUR = 'neighbour', _('Neighbour')
    GURDIAN = 'gurdian', _('Gurdian')

class CourseLevel(models.TextChoices):
    BEGINNERS = 'beginners', 'Beginners'
    INTERMEDIATE = 'intermediate', 'Intermediate'
    ADVANCED = 'advanced', 'Advanced'
    PROFESSIONAL = 'professional', 'Professional'
    Master = 'master', 'Master'
    Genius = 'genius', 'Genius'

class Priority(models.TextChoices):
    HIGH = 'high', 'High'
    MEDIUM = 'medium', 'Medium'
    LOW = 'low', 'Low'