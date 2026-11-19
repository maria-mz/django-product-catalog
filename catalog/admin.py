from django.contrib import admin

from .models import Category, Tag, Product

admin.site.register(Category)
admin.site.register(Tag)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('description', 'category')
    search_fields = ('description',)
    list_filter = ('category', 'tags')
    filter_horizontal = ('tags',)
