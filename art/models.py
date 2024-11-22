from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    

class Art(models.Model):
    IN_STOCK = 'vailable'
    SOLD = 'sold'

    STATUS_CHOICES = [
        (IN_STOCK, 'Available'),
        (SOLD, 'Sold Out'),
    ]

    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='art_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=IN_STOCK)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='art_pieces')


    def __str__(self):
        return self.title
    
from django.contrib.auth.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    art = models.ForeignKey(Art, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.art.title}"

