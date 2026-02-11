from django.db import models

class Student(models.Model):
    student_id = models.CharField(max_length=100, unique=True)
    student_name = models.CharField(max_length=100)
    department_name = models.CharField(max_length=100)
    student_email = models.EmailField(unique=True, null=True, blank=True)
    student_age = models.IntegerField(default=18)
    student_address = models.TextField(blank=True, default="")
    student_marks = models.IntegerField()

    class Meta:
        ordering=['student_id']



