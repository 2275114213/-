from django.contrib import admin
from app01.models import *
# Register your models here.

# 注册是admin.site.register  单例模式
admin.site.register(Book)
admin.site.register(UserInfo)
admin.site.register(Room)