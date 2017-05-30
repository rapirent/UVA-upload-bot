from django.db import models

class User(models.Model):
    telegram_id = models.IntegerField()
    first_name = models.CharField(max_length=200, default='')
    last_name = models.CharField(max_length=200, default='')
    username = models.CharField(max_length=200, default='')
    states = models.IntegerField(default=-1)
    uva_id = models.CharField(max_length=200, default='')
    uva_passwd = models.CharField(max_length=200, default='')
    #明碼不安全，但也只能這樣了
    # language_code
