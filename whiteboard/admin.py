from django.contrib import admin
from .models import Event,Comment
from import_export.admin import ImportExportModelAdmin
from import_export import resources

# Register your models here.




class EventResource(resources.ModelResource):
	class Meta:
		model = Event
		import_id_fields = ('id',)
		exclude =('',)

class EventAdmin(ImportExportModelAdmin):
	resource_class = EventResource
	list_display = ('name','venue','event_date')
	list_filter = ('type_e','venue','manager')
	search_fields = ['venue',]
	ordering = ('-event_date',)

admin.site.register(Event,EventAdmin)

class CommentResource(resources.ModelResource):
	class Meta:
		model = Comment
		import_id_fields = ('id',)
		exclude =('',)

class CommentAdmin(ImportExportModelAdmin):
	resource_class = CommentResource
	list_display = ('rma_id','username','cmt_time')
	list_filter = ('username',)
	search_fields = ['rma_id',]
	ordering = ('-cmt_time',)

admin.site.register(Comment,CommentAdmin)
