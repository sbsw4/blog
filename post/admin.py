# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
# Register your models here.

class PostModelAdmin(admin.ModelAdmin):
    list_display = ('title','created','desc')
    list_filter = ('created',)
    search_fields = ('title','content')

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post,PostModelAdmin)
