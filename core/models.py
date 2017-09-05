from django.db import models

# Create your models here.

class TestModel(models.Model):
    a = models.CharField(max_length=200,blank=True,null=True)
    b = models.CharField(max_length=200,blank=True,null=True)
    c = models.CharField(max_length=200,blank=True,null=True)
    d = models.CharField(max_length=200,blank=True,null=True)
    e = models.CharField(max_length=200,blank=True,null=True)
    f = models.CharField(max_length=200,blank=True,null=True)
    g = models.CharField(max_length=200,blank=True,null=True)

    def __str__(self):
        return str(self.pk)