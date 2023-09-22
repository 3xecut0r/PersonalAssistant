from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('get_first_name',
                    'get_last_name',
                    'email',
                    'phone_number',
                    'birthday')
    search_fields = ('first_name',
                     'last_name',
                     'email',
                     'phone_number')

    def get_first_name(self, obj):
        return obj.first_name

    def get_last_name(self, obj):
        return obj.last_name

    get_first_name.short_description = 'First_name'
    get_last_name.short_description = 'Last_name'
