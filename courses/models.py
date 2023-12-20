from django.db import models
from django.utils import timezone

class Course(models.Model):
    code = models.CharField(max_length=15, primary_key=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.code
    
class CourseStudent(models.Model):    
    documentType = models.CharField(max_length=4)
    documentNumber = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    cellphone = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    dateUpdate = models.DateTimeField(default=timezone.now, blank=True)       

    def __str__(self):
        return self.name + ' ' + self.lastName
    
class CourseCompetence(models.Model):    
    documentNumber = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    competence = models.CharField(max_length=255)
    learningResult = models.CharField(max_length=255)
    evaluationJudgment = models.CharField(max_length=50)
    official = models.CharField(max_length=70)
    dateUpdate = models.DateTimeField(default=timezone.now, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.documentNumber



    

    
