from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin



class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    year = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(null=True, blank=True,unique=True)
    RegNo = models.CharField(max_length=255, unique=True, null=True, blank=True)
    role = models.CharField(max_length=50, choices=[('ADMIN', 'Admin'), ('SUPERVISOR', 'Supervisor'), ('STUDENT', 'Student')])
    firstname = models.CharField(max_length=255)
    middlename = models.CharField(max_length=255)
    surname = models.CharField(max_length=255, null=True, blank=True)
    supervisors = models.ManyToManyField('self', through='Supervision', symmetrical=False, related_name='students')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'middlename', 'role']

    def __str__(self):
        return self.email or self.RegNo

class Supervision(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='supervision_student')
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='supervision_supervisor')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.student.firstname)  + ' ' +  str(self.student.surname)

class Dissertation(models.Model):
    title=models.CharField(max_length=250,unique=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dissertations')
    file = models.FileField(upload_to='dissertations/',null=True,blank=True)
    status = models.CharField(max_length=50, choices=[('PENDING', 'Pending'), ('VERIFIED', 'Verified'), ('REJECTED', 'Rejected')], default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.student.firstname) + str(self.student.surname) 

class Comment(models.Model):
    content = models.TextField()
    dissertation = models.ForeignKey(Dissertation, on_delete=models.CASCADE, related_name='comments')
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.supervisor.email} on {self.dissertation.student.email if self.dissertation.student.email else self.dissertation.student.RegNo}'
    



