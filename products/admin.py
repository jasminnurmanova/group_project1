from django.contrib import admin
from .models import Product,Category,Comment,ProductImage


class ProductImageInLine(admin.TabularInline):
    model=ProductImage

class ProductAdmin(admin.ModelAdmin):
    list_display=['title','id','date','category','author']
    inlines=[ProductImageInLine]


admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(ProductImage)
admin.site.register(Product,ProductAdmin)