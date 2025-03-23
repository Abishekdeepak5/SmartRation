from django.db import models


class UserDetails:
    def __init__(self):
        pass
    def __init__(self, user_id=0, user_name="", password="", role="", phone_number="", gender="", email="", address="", pincode="", date_of_birth=""):
        self.__user_id = user_id
        self.__user_name = user_name
        self.__password = password
        self.__role = role
        self.__phone_number = phone_number
        self.__gender = gender
        self.__email = email
        self.__address = address
        self.__pincode = pincode
        self.__date_of_birth = date_of_birth

    # Getters
    def get_user_id(self):
        return self.__user_id

    def get_user_name(self):
        return self.__user_name

    def get_password(self):
        return self.__password

    def get_role(self):
        return self.__role

    def get_phone_number(self):
        return self.__phone_number

    def get_gender(self):
        return self.__gender

    def get_email(self):
        return self.__email

    def get_address(self):
        return self.__address

    def get_pincode(self):
        return self.__pincode

    def get_date_of_birth(self):
        return self.__date_of_birth

    # Setters
    def set_user_name(self, user_name):
        self.__user_name = user_name

    def set_password(self, password):
        self.__password = password

    def set_role(self, role):
        self.__role = role

    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number

    def set_gender(self, gender):
        self.__gender = gender

    def set_email(self, email):
        self.__email = email

    def set_address(self, address):
        self.__address = address

    def set_pincode(self, pincode):
        self.__pincode = pincode

    def set_date_of_birth(self, date_of_birth):
        self.__date_of_birth = date_of_birth

    # String Representation
    def __str__(self):
        return f"User: {self.__user_name}, Role: {self.__role}, Email: {self.__email}"

"""
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
"""