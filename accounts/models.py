import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from .manager import UserManager


# Create your models here.
class User(AbstractUser):
    list_roles = (
        (1, 'Employee'),
        (2, 'Recruiter')
    )
    username = None
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    role = models.IntegerField(default=0, choices=list_roles)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'User'

class Employee(models.Model):
    account = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    avatar_url = models.CharField(null=True, max_length=1000, blank=True,
                                  default='https://res.cloudinary.com/dzqfmaj6i/image/upload/v1712999567/hireIT/default/user_default_hx8abj.jpg')
    pdf_file = models.CharField(null=True, max_length=1000, blank=True, default=None)

    class Meta:
        db_table = 'Employee'

    def __str__(self):
        return self.account.first_name + ' ' + self.account.last_name


class Recruiter(models.Model):
    account = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company_name = models.CharField(null=True, blank=True, max_length=500)
    address = models.CharField(null=True, blank=True, max_length=500)
    avatar_url = models.CharField(null=True, max_length=1000, blank=True,
                                  default='https://res.cloudinary.com/dzqfmaj6i/image/upload/v1712999567/hireIT/default/user_default_hx8abj.jpg')

    class Meta:
        db_table = 'Recruiter'

    def __str__(self):
        return self.account.first_name + ' ' + self.account.last_name
    
class JobRequirement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE, related_name='job_requirements')
    job_name = models.CharField(max_length=255)
    location = models.CharField(null=True, blank=True, max_length=100)
    pdf_upload = models.CharField(null=True, max_length=1000, blank=True, default=None)
    skills = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)


    class Meta:
        db_table = 'JobRequirement'

class ExtractCV(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True, related_name="extract_cv")
    phone_number = models.CharField(null=True, blank=True, max_length=12)
    location = models.CharField(null=True, blank=True, max_length=100)
    skills = models.TextField()
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'ExtractCV'