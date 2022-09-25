from distutils.command.upload import upload
from email.mime import image
from msilib.schema import PublishComponent
from tabnanny import verbose
from turtle import title
from venv import create
from django.db import models
from django.forms import CharField, ImageField, SlugField
from django.utils import timezone
from extensions.utils import jalali_converter
from django.urls import reverse
from django.contrib.auth.models import User
               #tag
from taggit.managers import TaggableManager



# class ArticleManager(models.Manager):
#     def p(self,year):
#         return self.filter(published__year=year)
# =====MANAGER HA
# class ArticleManager(models.Manager):
#     def publish(self,year):
#       return self.filter(published__year=year)


# class manerManager(models.Manager):
#     def get_queryset(self):
#         return super(manerManager,self).get_queryset().filter(status='d')


class Category(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=50, unique=True)
    status = models.BooleanField(default=True)
    position = models.IntegerField()

    def __str__(self):
        return self.title


class Article(models.Model):
    STATUS_CHOICES = {
        ('p', 'published'),
        ('d', 'draft')
    }
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=50, unique=True)
    category = models.ManyToManyField(Category, related_name="article")
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="images")
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    objects = models.Manager

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-published"]

    #     verbose_name = 'مقاله'
    #     verbose_name_plural = ' مقاله ها'

    def jpublished(self):
        return jalali_converter(self.published)
    # jpublished.short_description="published" =farsi mikone

    # objects=ArticleManager()=====MANAGER HA
    # objects=models.Manager()
    # published=manerManager()


class Test(models.Model):
    STATUS_CHOICES = {
        ('p', 'published'),
        ('d', 'draft')
    }
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="images")
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    objects = models.Manager
    tags=TaggableManager()
    def __str__(self):
        return self.title

    
    def get_absolute_url(self):
     return reverse('blog:site', kwargs={'slug':self.slug,'pk':self.id})
 
 
 
#   >>>>>>>======KAR NAKARD(AVORDAN URL AZ DETABASE ) <<<<<<<<<<<<


class Account(models.Model):
    GENDER_CHOICES = {
        ('اقا', 'اقا'),
        ('خانم', 'خانم')
    }
    user=models.OneToOneField(User, on_delete=models.CASCADE,related_name="account")
    phone=models.CharField(max_length=11,null=True,blank=True)
    gender=models.CharField(max_length=5,choices=GENDER_CHOICES,default="خانم")
    address=models.TextField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    age=models.PositiveIntegerField(default=0,null=True,blank=True)
    def __str__(self):
        return self.user.first_name +" "+ self.user.last_name
    
    
    
    
    
    
    
#     (env) C:\Users\PC\Desktop\django2\config>python manage.py makemigrations
# You are trying to add the field 'created' with 'auto_now_add=True' to account without a default; the database needs something to populate existing rows.
#  1) Provide a one-off default now (will be set on all existing rows)        
#  2) Quit, and let me add a default in models.py
# Select an option: Traceback (most recent call last):  >>>>>DAR MOVAJEHE BA IN ERROR FILDHA RA
# =TRUENULL  GARAR MIDAHIM BAD MIGATIONS MIKONIM SEPAS DOBARE NULL RA BARMIDARIM  VA  DOBARE MIGATIONS MIKONIM 
# DAR AKHAR GOZINE 2 RA MIZANIM<<<<<


class Comment(models.Model):
    post=models.ForeignKey(Test,on_delete=models.CASCADE,related_name="comments")
    name=models.CharField(max_length=100)
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=False)

    class Meta:
        ordering=('created',)

    def __str__(self):
        return    " {1} بر روی پست {0}کامنت توسط ".format(self.name,self.post)
 







