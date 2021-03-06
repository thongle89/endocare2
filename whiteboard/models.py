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
	is_verified = models.BooleanField('Xác Nhận',blank=True,null=True)
	verifier = models.CharField('Người xác nhận',max_length=50,blank=True,null=True)
	verify_time = models.DateTimeField('Ngày xác nhận',blank=True,null=True)
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
	manager = models.ForeignKey(User,blank = True,null = True, on_delete = models.SET_NULL)
	description = models.TextField(blank = True)
	attendees = models.ManyToManyField(User,related_name='attendees',blank=True)

	def __str__(self):
		return self.name
class Media(models.Model):
	bao_tri_1 = models.CharField('Bảo trì 1',max_length=100)
	bao_tri_2 = models.CharField('Bảo trì 2',max_length=100)
	bao_tri_3 = models.CharField('Bảo trì 3',max_length=100)
	bao_tri_4 = models.CharField('Bảo trì 4',max_length=100)
	bao_tri_5 = models.CharField('Bảo trì 5',max_length=100)




