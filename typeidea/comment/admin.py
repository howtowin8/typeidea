from django.contrib import admin
from .models import Comment
from typeidea.custom_site import custom_side
# Register your models here.
@admin.register(Comment,site=custom_side)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('target','nickname','content','website','created_time')