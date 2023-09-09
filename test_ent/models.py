from django.db import models

# Create your models here.

class Client(models.Model):
    surname = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=80)
    city = models.CharField(max_length=40)
    phone = models.CharField(max_length=40)
    email = models.EmailField()
    comments = models.TextField()

    def __str__(self):
        return f"{self.surname}, {self.name}"

class Calendar(models.Model):
    date = models.DateField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    job_type = models.CharField(max_length=40, choices=[
        ('INSTALLATION', 'Installation'),
        ('ERROR', 'Error'),
        ('SERVICE', 'Service'),
        ('ADDITION', 'Addition'),
        ('REMAKE', 'Remake'),
        ('CHECK', 'Check'),
        ('CALIBRATION', 'Calibration'),
        ('OFFER', 'Offer'),
        ('COLLECTION', 'Collection'),
        ('OTHER', 'Other'),
    ])
    category = models.CharField(max_length=40, choices=[
        ('ALARM', 'Alarm'),
        ('DOORPHONE', 'Doorphone'),
        ('SATELLITE', 'Satellite'),
        ('TERRESTRIAL', 'Terrestrial'),
        ('CCTV', 'CCTV'),
        ('NETWORK', 'Network'),
        ('FIRE', 'Fire'),
        ('TELEPHONE CENTER', 'Telephone Center'),
        ('OTHER', 'Other'),
    ])
    price = models.FloatField(default=0)
    paid = models.FloatField(default=0)
    comments = models.TextField(default=" ")
    installation_manual = models.FileField(upload_to='Installation_Manuals/')

    def __str__(self):
        return f"{self.client.surname}, {self.client.name} - {self.date}"
