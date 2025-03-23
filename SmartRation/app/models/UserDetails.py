from django.db import models

class UserDetails(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
    ]
    
    GENDER_CHOICES = [
        ('m', 'Male'),
        ('f', 'Female'),
        ('t', 'Transgender'),
    ]

    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50, null=False)
    password = models.CharField(max_length=50, null=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=False)
    phone_number = models.CharField(max_length=50, unique=True, null=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=False)
    email = models.EmailField(max_length=50, unique=True, null=False)
    address = models.CharField(max_length=100, null=False)
    pincode = models.CharField(max_length=6, null=False)
    date_of_birth = models.DateField(null=False)

    def __str__(self):
        return self.user_name
