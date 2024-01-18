from django.contrib import admin

# Register your models here.

from django.contrib import admin
from doctor_infos_app.models import DoctorInfo, Address

class DoctorInfoAdmin(admin.ModelAdmin):
    pass
    # list_display = ['']

admin.site.register(DoctorInfo, DoctorInfoAdmin)

class AddressAdmin(admin.ModelAdmin):
    pass

admin.site.register(Address, AddressAdmin)