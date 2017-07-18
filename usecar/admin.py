from django.contrib import admin
from usecar import models
# Register your models here.
admin.site.register(models.Companies)


class PersonsAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'state')
admin.site.register(models.Persons, PersonsAdmin)


class CarsAdmin(admin.ModelAdmin):
    list_display = ('license', 'brand', 'style', 'cap', 'state', 'co')
admin.site.register(models.Cars, CarsAdmin)


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'person', 'car', 'num', 'reason')
admin.site.register(models.Application, ApplicationAdmin)


class ExamAdmin(admin.ModelAdmin):
    list_display = ('id', 'exam1', 'att1', 'exam2', 'att2')
admin.site.register(models.Exam, ExamAdmin)


class CcAdmin(admin.ModelAdmin):
    list_display = ('id', 'to')
admin.site.register(models.Cc, CcAdmin)
