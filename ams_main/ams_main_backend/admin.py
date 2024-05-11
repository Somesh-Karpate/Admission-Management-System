from django.contrib import admin
from .models import *

# Register your models here.
class obj_Student_detail(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name', 'gender', 'date_of_birth', 'nationality', 'annual_income',
                    'contact_number', 'alternate_contact_number', 'email', 'guardian_name', 'guardian_contact',
                    'address_line1', 'address_line2', 'landmark', 'town_city', 'pincode', 'district', 'state',
                    'permanent_address', 'file_tenth')

    search_fields = ('user_id', 'first_name', 'last_name', 'email', 'contact_number', 'guardian_name')
    list_filter = ('gender', 'nationality', 'permanent_address')
    ordering = ('user_id',)

admin.site.register(Student_detail, obj_Student_detail)
