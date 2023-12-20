from django.db import models

class Instructor(models.Model):
    name = models.CharField(max_length=255)
    document = models.CharField(max_length=255, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=255)
    contract_type = models.CharField(max_length=255)
    status = models.BooleanField(default=True)    
    image = models.ImageField(upload_to='static/images/instructors', null=True, blank=True)

    def __str__(self):
        return self.name
