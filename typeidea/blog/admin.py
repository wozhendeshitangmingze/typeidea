from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin
from .models import Post, Category, Tag
from .adminforms import PostAdminForm


class PostInline(admin.TabularInline):

    fields = ('title', 'desc')
    extra = 1
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', "status", "is_nav", "created_time", "post_count")
    fields = ("name", "status", "is_nav")
    inlines = [PostInline,]

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = "文章数量"


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ("name", "status", "created_time")
    fields = ("name", "status")


class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器只展示当前用户分类"""

    title = "分类过滤"
    parameter_name = "owner_category"

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list("id", "name")

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    list_display = ['title', 'category', 'status', 'created_time', 'owner', 'operator']
    list_display_links = ["title"]
    list_filter = [CategoryOwnerFilter]
    search_fields = ["title", "category__name"]

    actions_on_top = True
    date_hierarchy = "created_time"
    # actions_one_bottom = True

    # save_on_top = True
    # exclude = ('owner', )
    # fields = (('title', 'category'), 'desc', 'status', 'content', 'tag')
    fieldsets = (
        ('标题', {
            'description': '基础配置描述',
            'fields':(('title', 'category'),
                      'status',
                      ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('标签', {
            'classes': ('collapse', ),
            "fields":('tag',),
        })
    )
    filter_horizontal = ('tag',)
    form = PostAdminForm

    def operator(self,obj):
        return format_html('<a href="{}">编辑</a>', reverse('cus_admin:blog_post_change', args=(obj.id,)))

    operator.short_description = "编辑"

    # class Media:
    #     css = {
    #         'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css", ),
    #     }
    #     js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)