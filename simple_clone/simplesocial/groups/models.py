from django.db import models
from django.utils.text import slugify

import misaka

from django.contrib.auth import get_user_model
User=get_user_model()

from django import template

register=template.Library()

class Group(models.Model):
    name=models.CharField(max_length=255,unique=True)
    slug=models.SlugField(unique=True,allow_unicode=True)
    description = models.TextField(blank=True,default='')
    description_html=models.TextField(default='',blank=True,editable=False)
    members=models.ManyToManyField(User,through="GroupMembers")

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.slug=slugify(self.name)
        self.description_html=misaka.html(self.description)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return revers('groups:single',kwargs={'slug':self.slug})

    class Meta:
        ordering=['name']



class GroupMembers(models.Model):
    group=models.ForignKey(Group,related_name="memberships")
    user=models.ForignKey(User,related_name="user_groups")

    def __str__(self):
        self.user.username
    class Meta:
        unique_together = ('group','user')
