from django.db import models

# Create your models here.

class calendar(models.Model):
    date = models.DateField(auto_now_add=True)
    surname = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=80)
    city = models.CharField(max_length=40)
    phone = models.CharField(max_length=40)
    email = models.EmailField()
    job_type = models.CharField(max_length=40)
    category = models.CharField(max_length=40)
    installationManual = models.FileField(upload_to='Installation Manuals')

class client(models.Model):
    surname = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=80)
    city = models.CharField(max_length=40)
    phone = models.CharField(max_length=40)
    email = models.EmailField()
