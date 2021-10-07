from django.db import models
from home.models import Exfm,Customer
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Comment(models.Model):
	rma_id = models.ForeignKey(Exfm,on_delete = models.CASCADE)
	username = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
	cmt_time = models.DateTimeField(auto_now_add=True)
	cmt_text = models.TextField('Nội dung')
	def __str__(self):
		return str(self.rma_id)


class Event(models.Model):
	# on_delete = model.CASCADE: when items deleted, rows deleted
	# on_delete = model.SET_NULL: when items deleted, items this row is null
	TYPE_CHOICES = ((1,'Bảo trì'),
					(2,'Training')
					)
	type_e = models.IntegerField('Type',choices=TYPE_CHOICES,default=1)
	name = models.CharField('Event Name',max_length =120)
	event_date = models.DateTimeField('Event Date')
	venue = models.ForeignKey(Customer,related_name='manager',blank = True,null = True,on_delete = models.CASCADE)
	# venue = models.CharField(max_length=120)
	# manager = models.CharField(max_length =120)
	manager = models.ForeignKey(User,blank = True,null = True, on_delete = models.SET_NULL)
	description = models.TextField(blank = True)
	attendees = models.ManyToManyField(User,related_name='attendees',blank=True)

	def __str__(self):
		return self.name



