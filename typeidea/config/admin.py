from django.contrib import admin
from .models import Link,SideBar
from typeidea.custom_site import custom_side
# from typeidea.base_admin import BaseOwnerAdmin

class BaseOwnerAdmin(admin.ModelAdmin):
    """
    1.用来自动补充文章、分类、标签、侧边栏、友情链接这些Model的owner字段
    2.用来针对querset过滤当前用户的数据
    """

    exclude = ('owner',)

    def get_queryset(self, request):
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)

# Register your models here.
@admin.register(Link,site=custom_side)
class LinkAdmin(BaseOwnerAdmin):
    list_display = ('title','href','status','weight','created_time')
    fields = ('title','href','status','weight')

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(LinkAdmin,self).save_model(request,obj,form,change)

@admin.register(SideBar,site=custom_side)
class SideBarAdmin(BaseOwnerAdmin):
    list_display = ('title','display_type','content','created_time')
    fields = ('title','display_type','content')

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(SideBarAdmin,self).save_model(request,obj,form,change)