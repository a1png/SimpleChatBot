from django.db import models
from enum import Enum


class GenderEnum(Enum):
    female = 0
    male = 1
    unknown = 2


class SmokerEnum(Enum):
    no = 0
    yes = 1


class UserInfo(models.Model):
    """
    user information
    user_id: Here we use this field to connect user infomation to the logged in users. Users are not necessarily logged
    in during the chat, so this field could be empty.

    """
    name = models.CharField(max_length=50)
    gender = models.IntegerField(default=2)  # 0: female, 1: male, 2: unknown
    birth_date = models.DateField()
    smoker = models.IntegerField(default=0)  # 0: non smoker, 1: smoker
    user_id = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "UserInfo"
