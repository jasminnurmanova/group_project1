from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=17, blank=True, null=True)
    tg_username = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg')
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.phone_number:
            phone = self.phone_number.strip()

            if len(phone) == 9 and phone.isdigit():
                phone = f"+998{phone}"

            elif len(phone) == 12 and phone.isdigit():
                phone = f"+{phone}"

            elif phone.startswith("+") and phone[1:].isdigit():
                pass

            else:
                raise ValueError("Invalid phone number format")

            self.phone_number = phone

        super().save(*args, **kwargs)


class Wishlist(models.Model):
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Wishlist item by ' + str(self.author.username)

    class Meta:
        ordering = ['-updated_at']


class Chat(models.Model):
    user1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='chats_user1')
    user2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='chats_user2')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Chat between {self.user1.username} and {self.user2.username}'

    class Meta:
        ordering = ['-updated_at']
        unique_together = ('user1', 'user2')


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender.username} in chat {self.chat.id if self.chat else "Unknown"}'

    class Meta:
        ordering = ['created_at']


class Cart(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_cart')
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.author.username}"


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    )
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    address = models.CharField(max_length=256)
    phone = models.CharField(max_length=16)
    email = models.CharField(max_length=64)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    tg_username = models.CharField(max_length=32)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.owner.username


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    qnt = models.PositiveIntegerField()

    def __str__(self):
        return f"#{self.order.first_name} - {self.product.title}"


class DepositRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='deposit_request')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.user.username


class BalanceHistory(models.Model):
    TYPE_CHOICES = (
        ('in', 'Kirim'),
        ('out', 'Chiqim'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_balace')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    type = models.CharField(max_length=8, choices=TYPE_CHOICES)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} | {self.amount} | {self.type}"