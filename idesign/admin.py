from django.contrib import admin
from .models import Web, Category, PostImage, Search, Slider, PostFile

# Register your models here.
# from .models import self


class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'parent', 'slug')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class PostImageAdmin(admin.StackedInline):
    model = PostImage


class PostFileAdmin(admin.StackedInline):
    model = PostFile


class WebAdmin(admin.ModelAdmin):
    inlines = [PostImageAdmin, PostFileAdmin]

    list_display = ('design_code', 'name', 'category',
                    'needle', 'stitch', 'area', 'Publish')
    list_editable = ('stitch', 'area')
    list_filter = ('created', 'published', 'updated')
    search_fields = ('name', 'category', 'design_code', 'stitch', 'needle')
    prepopulated_fields = {'slug': ('name',)}


class SearchAdmin(admin.ModelAdmin):

    list_display = ('keyword', 'count')


admin.site.register(Web, WebAdmin)
admin.site.register(Search, SearchAdmin)


class SliderAdmin(admin.ModelAdmin):

    list_display = ('first_small_heading', 'second_heading', 'third_heading')


admin.site.register(Slider, SliderAdmin)
