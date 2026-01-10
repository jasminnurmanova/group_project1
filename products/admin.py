from django.contrib import admin
from .models import Product, Category, ProductImage, Comment


class CategoryAdminView(admin.ModelAdmin):
    class CategoryProductInline(admin.TabularInline):
        model = Product
        extra = 0

    empty_value_display = '-empty-'
    list_display=['id','name']
    inlines=[CategoryProductInline]
    search_fields=['id', 'name']
    ordering=['-updated_at']


class ProductAdminView(admin.ModelAdmin):
    class ProductImageInLine(admin.TabularInline):
        model = ProductImage

    empty_value_display = '-empty-'
    list_display=['id', 'title', 'category', 'author']
    fields=['title', ('category', 'author'), 'description', 'price']
    list_filter=['category', 'author']
    inlines=[ProductImageInLine]
    search_fields=['id', 'title', 'author', 'category', 'description', 'price']
    ordering=['-updated_at']


class ProductImageAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ['id', 'product', 'image']
    list_filter = ['product']
    ordering = ['-created_at']
    search_fields = ['id', 'product__title']

class CommentAdminView(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ['id', 'product', 'author', 'body']
    list_filter = ['product', 'author']
    ordering = ['-created_at']
    search_fields = ['id', 'product__title', 'author__username', 'body']


admin.site.register(Category, CategoryAdminView)
admin.site.register(Comment, CommentAdminView)
admin.site.register(Product, ProductAdminView)
admin.site.register(ProductImage, ProductImageAdmin)
