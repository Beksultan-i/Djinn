from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import *

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(PostImage)

