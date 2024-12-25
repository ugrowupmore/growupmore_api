# utils/authentication_wrappers.py

class GenericUserWrapper:
    """
    A wrapper to provide a consistent interface for different user types.
    """
    def __init__(self, user):
        self.user = user
        self.user_type = self.get_user_type()
    
    def get_user_type(self):
        from authuser.models import Student, Employee, Instructor, Institute
        if isinstance(self.user, Student):
            return 'student'
        elif isinstance(self.user, Employee):
            return 'employee'
        elif isinstance(self.user, Instructor):
            return 'instructor'
        elif isinstance(self.user, Institute):
            return 'institute'
        elif getattr(self.user, 'is_superuser', False):
            return 'superuser'
        return 'unknown'
    
    def __getattr__(self, attr):
        return getattr(self.user, attr)
    
    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_staff(self):
        return getattr(self.user, 'is_staff', False)

    @property
    def is_superuser(self):
        return getattr(self.user, 'is_superuser', False)

    def __str__(self):
        return str(self.user)
