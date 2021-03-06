# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import os

from django.db.models import Q
from django.db import models
from django.db.models.signals import pre_save,post_save
from django.urls import reverse

from ecommerce.utils import unique_slug_generator
from django.contrib.auth import get_user_model
User = get_user_model()



PRODUCT_TYPES = (
		('pants','Pants'),
		('top','Top'),
		('accessory','Accessory'),
		('hat','Hat'),
		('footerwear','Footerwear'),
	)
PRODUCT_STATUS = (
		('new','New'),
		('sale','Sale'),
	)

class ProductView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email

def get_filename_ext(filename):
	base_name = os.path.basename(filename)
	name, ext = os.path.splitext(base_name)
	return name,ext

def upload_image_path(instance, filename):
	new_filename = random.randint(1,234234234)
	name, ext = get_filename_ext(filename)
	final_filename = '{new_filename}{ext}'.format(new_filename = new_filename,ext=ext)
	return "products/{new_filename}/{final_filename}".format(new_filename=new_filename,final_filename=final_filename)

class ProductQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)

	def featured(self):
		return self.filter(featured=True, active=True)

	def search(self,query):

		lookups = (Q(title__icontains=query) |
				  Q(description__icontains=query)	|
				  Q(price__icontains=query)	|
				  Q(tag__title__icontains=query) |
				  Q(product_type__icontains=query)
				  )

		# Q(tas__name__icontains=query)
		return self.filter(lookups).distinct()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    product = models.ForeignKey('Product', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email

class ProductManager(models.Manager):
	def get_queryset(self):
		return ProductQuerySet(self.model, using=self._db)

	def all(self):
		return self.get_queryset().active()

	def featured(self):
		return self.get_queryset().featured()

	def get_by_id(self, id):
		qs = self.get_queryset().filter(id=id)
		if qs.count() == 1:
			return qs.first()
		return None

	def search(self,query):
		return self.get_queryset().active().search(query)

# Create your models here.
class Product(models.Model):
	title    	= models.CharField(max_length=120)
	slug		= models.SlugField(blank=True,unique=True)
	description = models.TextField()
	price		= models.DecimalField(decimal_places=2,max_digits=20,default=39.99)
	before_discount_price = models.DecimalField(decimal_places=2,max_digits=20,blank=True,null=True)
	image		= models.ImageField(upload_to=upload_image_path,null=True,blank=True)
	image2		= models.ImageField(upload_to=upload_image_path,null=True,blank=True)
	image3		= models.ImageField(upload_to=upload_image_path,null=True,blank=True)
	product_type 		= models.CharField(max_length=120,default='accessory',choices=PRODUCT_TYPES)
	product_status 		= models.CharField(max_length=50,default='new',choices=PRODUCT_STATUS)
	featured	= models.BooleanField(default=False)
	active		= models.BooleanField(default=True)
	timestamp	= models.DateTimeField(auto_now_add=True)
	
	objects = ProductManager()

	def get_absolute_url(self):
		# return "/products/{slug}/".format(slug=self.slug)
		return reverse("products:detail",kwargs={"slug":self.slug})

	def __str__(self):   # Hien thi thong tin database
		return self.title
	def __unicode__(self):
		return self.title

	@property
	def name(self):
		return self.title
	@property
	def get_comments(self):
		return self.comments.all().order_by('-timestamp')
	@property
	def comment_count(self):
		return Comment.objects.filter(product=self).count()
	

def product_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver,sender=Product)
