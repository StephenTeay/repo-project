# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = (
        ('STUDENT', 'Student'),
        ('STAFF', 'Staff'),
        ('ADMIN', 'Administrator'),
    )
    role = models.CharField(max_length=10, choices=ROLES, default='STUDENT')
    department = models.CharField(max_length=100, blank=True)
    matric_number = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

# projects/models.py
from django.db import models
from accounts.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class Project(models.Model):
    title = models.CharField(max_length=200)
    abstract = models.TextField()
    authors = models.ManyToManyField(User, related_name='authored_projects')
    supervisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='supervised_projects')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    keywords = models.CharField(max_length=200, help_text="Comma-separated list of keywords")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_projects')
    
    def __str__(self):
        return f"{self.title} ({self.year})"

class ProjectFile(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='project_files/%Y/%m/%d/')
    description = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(max_length=10, choices=(
        ('PDF', 'PDF Document'),
        ('ZIP', 'ZIP Archive'),
        ('DOC', 'Word Document'),
        ('OTH', 'Other')
    ))
    
    def __str__(self):
        return f"{self.project.title} - {self.file.name}"
