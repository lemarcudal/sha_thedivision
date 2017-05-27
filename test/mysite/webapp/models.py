from __future__ import unicode_literals
from django import forms
from django.db import models
from django.core.urlresolvers import reverse 
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
#new code below---------------------------------------

def upload_location(instance, filename):
	return "%s/%s" %(instance.id, filename)

class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	title = models.CharField(max_length=140, blank=False)
	slug = models.SlugField(unique=True)
	image = models.ImageField(upload_to=upload_location, 
			null=True,
			blank=True, 
			width_field="width_field", 
			height_field="height_field")
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	IGN = models.CharField(max_length=140, blank=False)
	Country = [('DENMARK','DENMARK'),('FINLAND','FINLAND'),('FRANCE','FRANCE'),
	('GERMANY','GERMANY'),('ITALY','ITALY'),('NETHERLADNS','NETHERLANDS'),
	('NORWAY','NORWAY'),('RUSSIA','RUSSIA'),('SPAIN','SPAIN'),('SWEDEN','SWEDEN'),
	('U.K.','U.K.'),('CANADA','CANADA'),('MEXICO','MEXICO'),('U.S.','U.S.'),
	('BRAZIL','BRAZIL'),('AUSTRALIA','AUSTRALIA'),('ARABIC','ARABIC')]
	country = models.CharField(max_length=20, choices=Country, blank=False)
	guide = models.TextField()
	email = models.EmailField()
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("detail", kwargs={"slug": self.slug})
		#return "/viewguides/detail/%s/" %(self.id)

	class Meta:
		ordering = ["-timestamp", "-updated"]

def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)

# Create your models here.
