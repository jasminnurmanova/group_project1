from django.contrib import admin
from .models import CustomUser, Wishlist, Chat, Message
from products.models import Comment
from django.contrib.auth.models import Group


class CustomUserAdminView(admin.ModelAdmin):
    class UserProfileInline(admin.StackedInline):
        model = Comment
        can_delete = False
        verbose_name_plural = 'Comments'
        extra = 0

    empty_value_display = '-empty-'
    list_display = ['id', 'username', 'email', 'phone_number', 'tg_username']
    search_fields = ['id', 'username', 'email', 'phone_number', 'tg_username']
    ordering = ['-created_at']
    fields = [("first_name", "last_name",'username'), ('email', 'phone_number', 'tg_username'), 'avatar', 'password']


class WishlistAdminView(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ['id', 'product', 'author']
    list_filter = ['product', 'author']
    ordering = ['-created_at']


class ChatAdminView(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ['id', 'user1', 'user2', 'created_at', 'updated_at']
    list_filter = ['user1', 'user2', 'created_at']
    ordering = ['-updated_at']
    search_fields = ['id', 'user1__username', 'user2__username']


class MessageAdminView(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ['id', 'chat', 'sender', 'content', 'is_read', 'created_at']
    list_filter = ['chat', 'sender', 'is_read', 'created_at']
    ordering = ['-created_at']
    search_fields = ['id', 'sender__username', 'content', 'chat__user1__username', 'chat__user2__username']




admin.site.register(CustomUser, CustomUserAdminView)
admin.site.register(Wishlist, WishlistAdminView)
admin.site.register(Chat, ChatAdminView)
admin.site.register(Message, MessageAdminView)
admin.site.unregister(Group)
