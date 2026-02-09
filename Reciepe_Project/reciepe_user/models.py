from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    recipe_name = models.CharField(max_length=100)
    ingredient = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    recipe_image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)
    def __str__(self):
        return self.recipe_name
class StudentId(models.Model):
    student_id = models.CharField(max_length=100)
    def __str__(self):
        return self.student_id
class Department(models.Model):
    department_name = models.CharField(max_length=100)
    student_id = models.OneToOneField(StudentId, related_name="student", on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    student_email = models.CharField(max_length=100, unique=True)
    student_age = models.IntegerField(default=18)
    student_address = models.TextField()
    def __str__(self):
        return self.student_name
