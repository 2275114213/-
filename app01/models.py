from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

# 用户用户认证组件 auth-user
class UserInfo(AbstractUser):
    tel=models.CharField(max_length=32)

class Room(models.Model):
    """
    会议室表
    """
    caption = models.CharField(max_length=32)  # 会议室名称 301
    num = models.IntegerField()  # 容纳人数
    def __str__(self):
        return self.caption


class Book(models.Model):
    """
    会议室预定信息
    """
    # on_delete=models.CASCADE 级联删除: 删了一个内容和他关联的也就没有了
    # 也就是当删除主表的数据时候从表中的数据也随着一起删除, 外键关联的表是主表

    user = models.ForeignKey('UserInfo',on_delete=models.CASCADE,)
    room = models.ForeignKey('Room',on_delete=models.CASCADE)
    date = models.DateField()  # 年月日
    time_choices = (
        (1, '8:00'),
        (2, '9:00'),
        (3, '10:00'),
        (4, '11:00'),
        (5, '12:00'),
        (6, '13:00'),
        (7, '14:00'),
        (8, '15:00'),
        (9, '16:00'),
        (10, '17:00'),
        (11, '18:00'),
        (12, '19:00'),
        (13, '20:00'),
    )
    # IntegerField() 单纯存一个数字, 只能存1-13 这几个数
    time_id = models.IntegerField(choices=time_choices)

    class Meta:
        # 联合唯一, 防止重复预定
        unique_together = (
            ('room','date','time_id'),
        )

    def __str__(self):
        return str(self.user)+"预定了"+str(self.room)










