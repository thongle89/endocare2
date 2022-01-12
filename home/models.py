from django.db import models

class Dealer(models.Model):
	name = models.CharField('Name',max_length=50,primary_key=True)
	vie_name = models.CharField('Tên tiếng Việt',max_length=100)
	address = models.TextField('Địa chỉ',max_length = 150,blank=True,null=True)
	area = models.CharField('Khu vực',max_length=30,blank=True,null=True)
	contact = models.CharField('Người đại diện',max_length = 30,blank=True,null=True)
	contact_phone = models.CharField('Số điện thoại',max_length = 10,blank=True,null=True)
	contact_email = models.EmailField('Email',blank=True,null=True)
	engineer1 = models.CharField('Kỹ sư',max_length = 30,blank=True,null=True)
	engineer_phone = models.CharField('Số điện thoại',max_length = 10,blank=True,null=True)
	engineer_email = models.EmailField('Email',blank=True,null=True)
	
	def __str__(self):
		return self.name

class Customer(models.Model):
	exfm_code = models.CharField('Exfm Code',max_length=100,primary_key=True)
	exfm_name = models.CharField('Exfm Name',max_length=100,blank = True,null = True,)
	web_name = models.CharField('Tên hiển thị',max_length=100,blank=True,null=True)
	dealer = models.ForeignKey(Dealer,blank = True,null = True,on_delete = models.SET_NULL)
	address = models.CharField('Địa chỉ',max_length=100,blank=True,null=True)
	city = models.CharField('Tỉnh/thành',max_length=50,blank=True,null=True)
	head_of_endo = models.CharField('Trưởng Khoa',max_length=50,blank=True,null=True)
	phone_head = models.CharField('Số điện thoại',max_length=50,blank=True,null=True)
	email_head = models.EmailField('Email',max_length=50,blank=True,null=True)
	nurse = models.CharField('Điều dưỡng trưởng',max_length=50,blank=True,null=True)
	phone_nurse = models.CharField('Số điện thoại',max_length=50,blank=True,null=True)
	email_nurse = models.EmailField('Email',max_length=50,blank=True,null=True)
	

	

	def __str__(self):
		return self.exfm_code

class Exfm(models.Model):

	
	rma = models.CharField('rma',primary_key=True,max_length=20)
	customer = models.ForeignKey(Customer,blank=True,null=True,on_delete = models.SET_NULL)
	location  = models.CharField('Location',max_length=10,blank=True,null=True)
	model_d = models.CharField('Model',max_length=20,blank=True,null=True)
	sn = models.CharField('SN',max_length=15,blank=True,null=True)
	install_date = models.DateTimeField('installed date',blank=True,null=True)
	warranty_date = models.DateTimeField('Warranty_Date',blank=True,null=True)
	receive_date = models.DateTimeField('Receive',blank=True,null=True)
	inspection_date = models.DateTimeField('Inspection',blank=True,null=True)
	start_time = models.DateTimeField('Start Time',blank=True,null=True)
	end_time = models.DateTimeField('End Time',blank=True,null=True)
	wr_report  = models.CharField('Warranty',max_length=50,blank=True,null=True)
	repair_size = models.CharField('MJ_mn',max_length=5,blank=True,null=True)
	issue_part = models.CharField('Issue',max_length=50,blank=True,null=True)
	pic = models.CharField('PIC',max_length=30,blank=True,null=True)
	repair_status = models.CharField('Status',max_length=30,blank=True,null=True)
	e_score = models.FloatField('e_score',blank=True,null=True)
	w_score = models.FloatField('w_score',blank=True,null=True)
	update_time = models.DateTimeField('Update Time',blank=True,null=True)
	
	
	def __str__(self):
		return self.rma

class Pending(models.Model):
	rma_id = models.OneToOneField(Exfm,unique=True,on_delete = models.CASCADE)
	dealer= models.ForeignKey(Dealer,blank=True,null=True,on_delete = models.SET_NULL)
	type_s = models.CharField('Type',max_length=20,blank=True,null=True)
	tr_date = models.DateField('Technical_Report',blank=True,null=True)
	part_list_date = models.DateField('Part_List',blank=True,null=True)
	quotation_date = models.DateField('Quotation',blank=True,null=True)
	confirm_date = models.DateField('Confirmation Date',blank=True,null=True)
	return_date = models.DateField('Return Date',blank=True,null=True)
	repair_note = models.CharField('Note',max_length=100,blank=True,null=True)
	p_status = models.CharField('Status',max_length=50,blank=True,null=True)
	p_score = models.FloatField('Score',blank=True,null=True)

	superadmin = models.BooleanField('Super Admin',blank=True,null=True,default=False)

	def __str__(self):
		return self.rma_id.rma

class Part(models.Model):
	rma = models.ForeignKey(Exfm,blank=True,null=True,on_delete = models.CASCADE)
	part_no = models.CharField('Part No.',max_length = 15)
	part_description = models.CharField('Part Name',max_length = 50)
	part_new = models.CharField('Parts News',max_length= 20,blank=True,null=True)
	vie_name = models.CharField('Tên Tiếng Việt', max_length =50,null = True,blank = True)

	def __str__(self):
		return self.rma.rma

class Rcode(models.Model):
	rma = models.ForeignKey(Exfm,blank=True,null=True,on_delete = models.CASCADE)
	r_code = models.CharField('R-Code.',max_length = 15)
	r_description = models.CharField('Description',max_length = 50)
	vie_name = models.CharField('Tên Tiếng Việt', max_length =50,null = True,blank = True)

	def __str__(self):
		return self.rma.rma

class Device(models.Model):
	customer  = models.ForeignKey(Customer,on_delete = models.CASCADE)
	serial = models.CharField('Số máy',max_length=20,primary_key = True)
	model = models.CharField('Kiểu máy',max_length=20)
	type_s =models.CharField('Loại máy',max_length=50,blank=True,null=True)
	installed_date = models.DateField('Ngày lắp đặt',null = True,blank = True)
	warranty_date = models.DateField('Bảo hành đến',null = True,blank = True)
	last_repair_date = models.DateField('Lần cuối sửa chữa',null = True,blank = True)
	
	
