from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
from decimal import Decimal


class BaseModel(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name



class Category(BaseModel):
    def get_absolute_url(self) -> str:
        return reverse('product:category_detail', args=[self.slug])
    
    class Meta(BaseModel.Meta):
        verbose_name_plural = "Категории"

class Brand(BaseModel):
    logo = models.ImageField(upload_to='brands/%Y/%m/%d/', blank=True)
    characteristics = models.JSONField(default=dict, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='brands', null=True, blank=True)
    
    def get_absolute_url(self) -> str:
        return reverse('product:brand_detail', args=[self.slug])
    
    class Meta(BaseModel.Meta):
        verbose_name_plural = "Бренды"

class Product(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived')
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    characteristics = models.JSONField(default=dict, blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['created_at']),
            
        ]
    
    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self) -> str:
        return reverse('product:product_detail', args=[self.slug])
    
    def is_in_stock(self) -> bool:
        return self.stock > 0


class Order(models.Model):
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product, through='OrderItem')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=ORDER_STATUS, default='pending')
    shipping_address = models.TextField()
    order_date = models.DateTimeField(default=timezone.now)
    
    def get_absolute_url(self) -> str:
        return reverse('user:cart', args=[self.id])
    
    def get_total(self) -> Decimal:
        return sum((item.get_total() for item in self.orderitem_set.all()), Decimal('0'))
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
    
    def __str__(self) -> str:
        return f"Order #{self.id} by {self.user.username}"

    def save(self, *args, **kwargs):
        if self.pk is None or self.status in ['pending', 'processing']:
            active_orders = Order.objects.filter(
                user=self.user,
                status__in=['pending', 'processing']
            ).exclude(pk=self.pk)
            
            if active_orders.exists():
                raise ValueError("User already has an active order")
        
        super().save(*args, **kwargs)

    @classmethod
    def get_active_order(cls, user):
        return cls.objects.filter(
            user=user,
            status__in=['pending', 'processing']
        ).first()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказах'
    
    def __str__(self) -> str:
        return f"{self.quantity}x {self.product.name} in Order #{self.order.id}"
    
    def get_total(self) -> float:
        return self.quantity * self.price
    
    def save(self, *args, **kwargs):
        self.price = self.product.price
        self.total = self.price * self.quantity
        
        if self.product.stock < self.quantity:
            raise ValueError(f"Недостаточно товара на складе. Доступно: {self.product.stock}")
        
        self.product.stock -= self.quantity
        self.product.save()
        
        super().save(*args, **kwargs)
        
        self.order.total_amount = self.order.get_total()
        if self.order.status == 'pending':
            self.order.status = 'processing'
        self.order.save()


class Review(models.Model):
    RATING_CHOICES = [(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ['product', 'user'] 
        ordering = ['-created_at']
    
    def __str__(self) -> str:
        return f"Review by {self.user.username} on {self.product.name}"
    

