from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db.models import Q

# Create your models here.
class AppUser(models.Model):
    roles = [('visitor','visitor'),('employee','employee'),('manager','manager'),('supermanager','supermanager')]
    openid = models.CharField( max_length=50, blank=False, default='', unique=True)

    gender = models.CharField(max_length=10, choices=[(
        'female', 'female'), ('male', 'male'), ('null', 'null')], default='null')
    avatar = models.CharField(max_length=150, blank=True, default='')  # 头像地址
    nickname = models.CharField(max_length=50, blank=False, default='')
    address = models.CharField(max_length=100, blank=True, default='')
    phonenumber = models.BigIntegerField(blank=True, default=0)
    name = models.CharField(max_length = 32, default='',blank=True)
    role = models.CharField(max_length = 32, choices = roles, default = 'visitor')
    department = models.CharField(max_length = 32,default = '')

    def __str__(self):
        if self.nickname == '':
            return 'openId:'+ self.openid[0:3]
        return self.nickname
    

class Domain(models.Model):
    code = models.CharField(max_length = 10, blank = False,unique = True)
    name = models.CharField(max_length = 30, blank = False)
    parent = models.ForeignKey("self",blank = True, null = True, related_name="sub_domain", on_delete=models.CASCADE)
    edditable = models.BooleanField(default=True)
    level = models.IntegerField(default=0)
    last_edditor = models.ForeignKey(AppUser,on_delete=models.SET_NULL,default='',blank=True,null=True)

    def is_edditable(self):
        return self.edditable
    
    def setlevel(self):
        if self.parent == None:
            self.level = 1
        else:
            self.level = self.parent.level+1
    
    def __str__(self):
        return "%s:%s" % (self.code,self.name)
    
    

    

# class Domain_extend(models.Model):
#     CODE = models.CharField(max_length = 10, blank = False)
#     parentCode = models.CharField(max_length = 10, blank = False)
#     name = models.CharField(max_length = 30, blank = False)

class ExpertInfo(models.Model): 
    states = [('active','active'),('inactive','inactive'),('new','new')]
    name = models.CharField(max_length = 10, blank = True, default = "")
    IDnum = models.CharField(max_length = 32)
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
    remarks = models.CharField(max_length = 64, default = "")
    status = models.CharField(max_length = 32, choices = states)
    time_enter = models.DateTimeField(default= timezone.now)
    uploaderID = models.IntegerField(default=0, null=True)
    checkerID = models.IntegerField(default=0, null=True)

    def __str__(self):
        return "%s -- %s" % (self.name,self.company)

class DomainToExpertInfo(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    expert = models.ForeignKey(ExpertInfo,on_delete=models.CASCADE, related_name="expertise")

    
class Project(models.Model):
    creator = models.ForeignKey(AppUser, null = True, on_delete = models.CASCADE)
    title = models.CharField(max_length = 64, default="", null = True)
    budget = models.CharField(max_length = 64, default="")
    num = models.CharField(max_length = 16, default="")
    time_create = models.DateTimeField(default = timezone.now)
    timespan = models.CharField(max_length = 64 , blank = True)
    address = models.CharField(max_length = 64, blank = True)
    sealed = models.BooleanField(default=False)
    
    
    
class Group(models.Model):
    project = models.OneToOneField(Project, on_delete= models.CASCADE, related_name = 'group',blank=True,null=True)
    picker = models.CharField(max_length = 16, default = "" )
    checker = models.CharField(max_length = 16, default = "" )
    active = models.BooleanField(default= True)
    time_create = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.project.title +'专家组'

class ExpertToGroup(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="member")
    expert = models.ForeignKey(ExpertInfo, on_delete=models.CASCADE)
    expertise = models.CharField(max_length = 32,default = '')
    remarks = models.CharField(max_length = 128,default = '', blank = True)
    
class CredentialImage(models.Model):
    expert = models.ForeignKey(ExpertInfo, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = None, max_length= 64,null = True)


class Key(models.Model):
    account = models.CharField(max_length = 50,default='')
    appid = models.CharField(max_length = 50,default='')
    secret = models.CharField(max_length = 50,default='')
    mch_id = models.CharField(max_length = 50,default='')
    mch_key = models.CharField(max_length = 50,default='')