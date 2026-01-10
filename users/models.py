from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=17, blank=True, null=True)
    tg_username = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg')
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
