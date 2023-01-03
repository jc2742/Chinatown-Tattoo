from django.contrib import admin
from .models import Artist, Appointment, GetTimes, Portfolio
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .forms import UserAdminChangeForm, UserAdminCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Registering models here.
User = get_user_model()


class AppointmentAdmin(admin.ModelAdmin):
    """
    Creates AppointmentAdmin model
    """
    search_fields = ['name']

    class Meta:
        model = Appointment

#Creating Custom User Models
class UserAdmin(BaseUserAdmin):
    """
    Creates a Custom UserAdmin Model
    """
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['full_name', 'email',
                    'admin', 'staff', 'active']
    list_filter = ['admin', 'staff', 'active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('admin', 'staff', 'active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password_2')}
         ),
    )
    search_fields = ['email', 'full_name']
    ordering = ['full_name']
    filter_horizontal = ()


#Registering models to admin server
admin.site.unregister(Group)
admin.site.register(Artist)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(GetTimes)
admin.site.register(Portfolio)
