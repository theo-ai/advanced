from django.db import models

# Create your models here.

class Calendar(models.Model):
    date = models.DateField()
    surname = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=80)
    city = models.CharField(max_length=40)
    phone = models.CharField(max_length=40)
    email = models.EmailField()
    job_type = models.CharField(max_length=40)
    category = models.CharField(max_length=40)
    price = models.FloatField(default=0)
    paid = models.FloatField(default=0)
    comments = models.TextField(default=" ")
    installation_manual = models.FileField(upload_to='Installation Manuals/')

    def __str__(self):
        return self.surname

class Client(models.Model):
    surname = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=80)
    city = models.CharField(max_length=40)
    phone = models.CharField(max_length=40)
    email = models.EmailField()
    comments = models.TextField()

    def __str__(self):
        return self.surname
