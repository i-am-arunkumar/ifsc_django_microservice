from ctypes import addressof
from django.db import models

class IFSC(models.Model):
    bank = models.CharField(max_length=250)
    ifsc = models.CharField(max_length=250,primary_key=True)
    micr_code = models.CharField(max_length=250)
    branch = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    district = models.CharField(max_length=250)
    state = models.CharField(max_length=250)

    @staticmethod
    def instance(record):
        return IFSC(
            bank=record["BANK"],
            ifsc=record["IFSC"],
            address=record["ADDRESS"],
            micr_code=record["MICR CODE"],
            branch=record["BRANCH"],
            district=record["DISTRICT"],
            city=record["CITY"],
            state=record["STATE"])

class ApiHistory(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    ifsc = models.CharField(max_length=250,null=True)
    endpoint = models.CharField(max_length=100,null=True)

