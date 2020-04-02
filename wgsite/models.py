from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    realname = models.CharField(max_length=12, null=False)
    sex = models.CharField(max_length=12, null=False)
    phone_number = models.CharField(max_length=12, null=False)
    college = models.CharField(max_length=50, null=False)
    weibo = models.CharField(max_length=50, null=True)
    def __str__(self):
        return self.user.username


class StaffUser(models.Model):
    myuser = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    department = models.CharField(max_length=30, null=False)
    birthdate = models.DateTimeField(null=False)
    other = models.CharField(max_length=500)

    def __str__(self):
        return self.user.username


class AdminUser(models.Model):
    staffuser = models.OneToOneField(StaffUser,
                                     on_delete=models.CASCADE,
                                     primary_key=True)
    other = models.CharField(max_length=500)

    def __str__(self):
        return self.user.username

class BsProject(models.Model):
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=500)
    able = models.BooleanField(default=True)

class BmBsProject(models.Model):
    STATUS = (
        ('1','已答题'),
        ('0','未答题'),
    )
    LQSTATUS = (
        ('1','已录取'),
        ('0','未录取'),
        ('2','等待结果'),
    )
    myuser = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    bsproject = models.ForeignKey(BsProject,on_delete=models.CASCADE)
    zkzh = models.CharField(max_length=50,default="等待分配")
    dtqk = models.CharField(max_length=1,choices=STATUS,default=STATUS[0][0])
    lqqk = models.CharField(max_length=1,choices=LQSTATUS,default='2')
    class Meta:
        unique_together = ('myuser','bsproject',)
