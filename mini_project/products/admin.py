from django.contrib import admin

from products.models import Category, Product


# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )
    list_filter = ('name', )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'description')
    search_fields = ('name', 'price', 'category', 'description')
    list_filter = ('name', 'price', 'category', 'description')
