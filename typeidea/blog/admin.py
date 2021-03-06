from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag
from .adminforms import PostAdminForm

from typeidea.custom_site import custom_side
# from typeidea.base_admin import BaseOwnerAdmin
# Register your models here.

class BaseOwnerAdmin(admin.ModelAdmin):
    """
    1.用来自动补充文章、分类、标签、侧边栏、友情链接这些Model的owner字段
    2.用来针对querset过滤当前用户的数据
    """

    exclude = ('owner',)

    def get_queryset(self, request):

        qs=super(BaseOwnerAdmin,self).get_queryset(request)
        return qs.filter(owner=request.user)

    def save_model(self,request,obj,form,change):
        obj.owner=request.user
        return super(BaseOwnerAdmin,self).save_model(request,obj,form,change)

class PostInline(admin.TabularInline):
    fields = ('title','desc')
    extra = 1
    model = Post


@admin.register(Category,site=custom_side)
class CategoryAdmin(BaseOwnerAdmin):

    inlines = [PostInline,]

    list_display = ('name','status','is_nav','created_time','post_count')
    fields = ('name','status','is_nav')

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(CategoryAdmin,self).save_model(request,obj,form,change)

    def post_count(self,obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'

@admin.register(Tag,site=custom_side)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name','status','created_time')
    fields = ('name','status')

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(TagAdmin,self).save_model(request,obj,form,change)




# 自定义list_filter

class CategoryOwnerFilter(admin.SimpleListFilter):
    """ 自定义过滤器只展示当前用户分类"""

    title = "分类过滤器"
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id','name')

    def queryset(self, request, queryset):
        category_id =self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset

@admin.register(Post,site=custom_side)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = [
        'title','category','status',
        'created_time','operator'
    ]
    list_display_links =[]
    list_filter = [CategoryOwnerFilter,]
    search_fields = ['title','category__name']

    actions_on_top = True
    actions_on_bottom = True

    #编辑页面
    save_on_top = True

    exclude = ('owner',)

    # fields = (
    #     ('category','title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )

    fieldsets = (
        ('基础配置',{
            'description':'基础配置描述',
            'fields':(
                ('title','category'),
                'status',

            ),
        }),
        ('内容',{
            'fields':(
                'desc',
                'is_md',
                'content_ck',
                'content_md',
                'content',
            ),
        }),
        ('额外信息',{
            'classes':('collapse',),
            'fields':('tag',),
        })
    )

    # filter_vertical =('tag',)
    filter_horizontal = ('tag',)

    def operator(self,obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args = (obj.id,))
        )
    operator.short_description = '操作'

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(PostAdmin,self).save_model(request,obj,form,change)
    #
    # def get_queryset(self, request):
    #     qs = super(PostAdmin,self).get_queryset(request)
    #     return qs.filter(owner=request.user)



    #自定义css和js的接口
    # class Media:
    #     css = {
    #         'all':("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),
    #     }
    #
    #     js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js', )