from django.contrib import admin
from .models import Pending,Dealer,Customer,Exfm
from import_export.admin import ImportExportModelAdmin
from import_export import resources



class PendingResource(resources.ModelResource):
	class Meta:
		model = Pending
		import_id_fields = ('rma_id',)
		exclude =('',)

class PendingAdmin(ImportExportModelAdmin):
	resource_class = PendingResource
	list_display = ('rma_id','dealer','quotation_date','p_status')
	list_filter = ('dealer','p_status')
	# search_fields = ['customer__exfm_name','model_d','sn','dealer__name']
	# ordering = ('rma','repair_status')

admin.site.register(Pending,PendingAdmin)

class ExfmResource(resources.ModelResource):
	class Meta:
		model = Exfm
		import_id_fields = ('rma',)
		exclude =('',)

class ExfmAdmin(ImportExportModelAdmin):
	resource_class = ExfmResource
	list_display = ('rma','customer','model_d','sn','repair_status')
	list_filter = ('model_d',)
	search_fields = ['customer__exfm_name','model_d','sn']
	ordering = ('rma','repair_status')

admin.site.register(Exfm,ExfmAdmin)

class DealerResource(resources.ModelResource):
	class Meta:
		model = Dealer
		import_id_fields=('name',)
		exclude = ('',)

class DealerAdmin(ImportExportModelAdmin):
	resource_class = DealerResource
	list_display = ('name','contact','engineer1')
	list_filter = ('name',)
	search_fields = ('name',)

admin.site.register(Dealer,DealerAdmin)

class CustomerResource(resources.ModelResource):
	class Meta:
		model = Customer
		import_id_fields = ('exfm_name',)
		exclude = ('id',)
class CustomerAdmin(ImportExportModelAdmin):
	resource_class = CustomerResource
	list_display = ('exfm_name','web_name','dealer','city','head_of_endo','nurse')
	list_filter = ('city',)
	search_fields =('web_name','dealer','city')

admin.site.register(Customer,CustomerAdmin)