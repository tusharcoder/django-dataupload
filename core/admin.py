from django.contrib import admin

# Register your models here.
from core.models import TestModel

class TestMOdelAdmin(admin.ModelAdmin):
    """Admin for the test model"""
    list_display = tuple(i.name for i in TestModel()._meta.get_fields() if not i.name == TestModel()._meta.pk.name)

admin.site.register(TestModel,TestMOdelAdmin)