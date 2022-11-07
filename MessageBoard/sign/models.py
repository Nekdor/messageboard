# Импорт из Джанго
from django.db import models
from django.contrib.auth.models import User


class Code(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, null=False)

    def __str__(self):
        return str(self.id) + '. ' + str(self.user) + ' ' + str(self.code)