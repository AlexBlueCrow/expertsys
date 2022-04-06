from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.
class AppUser(models.Model):
    name = models.CharField(max_length = 10, blank = False)
    

class Domain(models.Model):
    CODE = models.CharField(max_length = 10, blank = False)
    name = models.CharField(max_length = 30, blank = False)
    parent = models.ForeignKey("self",blank = True, null = True, related_name="children", on_delete=models.CASCADE)
    edditable = models.BooleanField(default=True)

    def is_edditable(self):
        return self.edditable
    

# class Domain_extend(models.Model):
#     CODE = models.CharField(max_length = 10, blank = False)
#     parentCode = models.CharField(max_length = 10, blank = False)
#     name = models.CharField(max_length = 30, blank = False)

class ExpertInfo(models.Model): 
    states = [('active','active'),('inactive','inactive')]
    name = models.CharField(max_length = 10, blank = True, default = "")
    identity = models.CharField(max_length = 32)
    phone = models.CharField(max_length = 30 )
    domain_1 = models.CharField(max_length = 10, blank = True, default = "")
    domain_2 = models.CharField(max_length = 10, blank = True, default = "")
    domain_3 = models.CharField(max_length = 10, blank = True, default = "")
    domain_4 = models.CharField(max_length = 10, blank = True, default = "")
    domain_5 = models.CharField(max_length = 10, blank = True, default = "")
    Qualification = models.CharField(max_length = 32)
    education = models.CharField(max_length = 64, default="")
    domicile = models.CharField(max_length = 30, default = "")
    company = models.CharField(max_length = 64, default = "")
    remark = models.CharField(max_length = 64, default = "")
    status = models.CharField(max_length = 32, choices = states)
    EntryTime = models.DateField(default= timezone.now)
    EntryID = models.IntegerField(default=0)


    
class Project(models.Model):
    creator = models.ForeignKey(AppUser, null = True, on_delete = models.CASCADE)
    title = models.CharField(max_length = 64, default="", null = True)
    budget = models.CharField(max_length = 64, default="")
    num = models.CharField(max_length = 16, default="")
    time_create = models.DateTimeField(default = timezone.now)
    timespan = models.CharField(max_length = 64 , blank = True)
    address = models.CharField(max_length = 64, blank = True)
    
    
class Group(models.Model):
    Project = models.ForeignKey(Project, on_delete= models.CASCADE)
    picker = models.CharField(max_length = 16, default = "" )
    checker = models.CharField(max_length = 16, default = "" )
    active = models.BooleanField(default= True)
    def counts(self):
        return self.expert.all().count()

class ExpertToGroup(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="expert")
    expert = models.ForeignKey(ExpertInfo, on_delete=models.CASCADE)









    