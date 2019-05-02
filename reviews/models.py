
from django.db import models


STARS = (1,2,3,4,5)

class Review(models.Model):
	user 			= models.OneToOneField(User, null=True, blank= True)
	product 		= models.OneToOneField(Product,null=True, blank =True)
	detail			= models.TextField(null=True,blank=True)
	stars 			= models.PositiveSmallIntegerField(default=5,choices=STARS)
	active			= models.BooleanField(default=True)
	timestamp		= models.DateTimeField(auto_now_add=True)
	
	objects = ReviewManager()


	def __str__(self):   # Hien thi thong tin database
		return self.stars
