class Ration:
    TABLE_NAME="ration"
    def __init__(self, ration_id, staff, address, opening_days, pincode):
        self.__ration_id = ration_id
        self.__staff = staff 
        self.__address = address
        self.__opening_days = opening_days
        self.__pincode = pincode

    def get_ration_id(self):
        return self.__ration_id

    def get_staff(self):
        return self.__staff

    def get_address(self):
        return self.__address

    def get_opening_days(self):
        return self.__opening_days

    def get_pincode(self):
        return self.__pincode

    def set_staff(self, staff):
        self.__staff = staff

    def set_address(self, address):
        self.__address = address

    def set_opening_days(self, opening_days):
        self.__opening_days = opening_days

    def set_pincode(self, pincode):
        self.__pincode = pincode

    # String Representation
    def __str__(self):
        return f"Ration ID: {self.__ration_id}, Address: {self.__address}, Staff: {self.__staff.get_user_name()}, Pincode: {self.__pincode}"

  


"""
from django.db import models
class Ration(models.Model):
    ration_id = models.AutoField(primary_key=True)
    staff = models.ForeignKey("UserDetails", on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    opening_days = models.JSONField() 
    pincode = models.CharField(max_length=6)
"""