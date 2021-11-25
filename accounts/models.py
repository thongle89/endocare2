from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from home.models import Dealer,Customer
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
	full_name = models.CharField(verbose_name=_("Full Name"),max_length=50)#,null=True,blank=True)
	phone = models.CharField(verbose_name=_("Phone Number"),max_length=17)
	email = models.EmailField(unique=True)
	organization = models.CharField(verbose_name=_("Organization"),max_length=50)
	is_ffvn = models.BooleanField(verbose_name=_("FFVN members"),default=False)
	dealer = models.ForeignKey(Dealer,null=True,blank=True,on_delete = models.SET_NULL)
	customer = models.ForeignKey(Customer,null=True,blank=True,on_delete = models.SET_NULL)
	# def __str__(self):
	# 	return self.full_name
