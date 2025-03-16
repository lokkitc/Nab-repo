from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Review, Brand
from django.utils.html import mark_safe


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'name', 'price', 'stock', 'created_at', 'category', 'brand', 'status')
    list_display_links = ('name',)
    list_editable = ('category', 'brand', 'status')
    ordering = ('-created_at',)
    list_per_page = 10
    prepopulated_fields = {'slug': ('name',)}
    actions = ['set_stock', 'set_published', 'set_draft']
    search_fields = ['name', 'description']
    list_filter = ['category', 'brand', 'status']

    @admin.action(description='Set Stock to 0')
    def set_stock(self, request, queryset):
        queryset.update(stock=0)

    @admin.action(description='Set Status to Published')
    def set_published(self, request, queryset):
        queryset.update(status='published')
            
    @admin.action(description="Set Status to Draft")
    def set_draft(self, request, queryset):
        queryset.update(status='draft')

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="100" />')
        return "No image"
    image_tag.short_description = 'Image'   

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 10

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'order_date')
    list_display_links = ('id',)
    list_editable = ('status',)
    list_filter = ('status', 'order_date')
    list_per_page = 10

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity')
    list_display_links = ('id',)
    list_per_page = 10

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'rating')
    list_display_links = ('id',)
    list_per_page = 10

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'created_at')
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 10
