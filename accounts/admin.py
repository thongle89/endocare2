from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import CustomUser
from home.admin import CustomerAdmin
from .forms import CustomUserCreationForm

from import_export.admin import ImportExportModelAdmin
from import_export import resources


class CustomUserResource(resources.ModelResource):
	class Meta:
		model = CustomUser
		import_id_fields = ('username',)
		exclude =('',)

# class CustomUserAdmin(ImportExportModelAdmin):
	

class CustomUserAdmin(ImportExportModelAdmin,UserAdmin):
	resource_class = CustomUserResource
	# model = CustomUser
	add_form = CustomUserCreationForm
	list_display = ('username','full_name','is_staff','organization','is_ffvn','dealer','customer')
	
	fieldsets = (
		*UserAdmin.fieldsets,
		(
			'Contat infomation',
			{
				'fields':['full_name',
					'phone','organization','is_ffvn',
					'dealer','customer']
			}
		)
	)
	def get_exfm_name(self, obj):
		if obj.customer.exfm_name:
			return obj.customer.exfm_name
		else:
			return '---'
	
	get_exfm_name.short_description = 'Units'
	get_exfm_name.admin_order_field = 'Exfm Name'
	get_exfm_name.empty_value_display = '???'

admin.site.register(CustomUser,CustomUserAdmin)

