from django.contrib import admin
from .models import *
from products.models import Comment
from django.contrib.auth.models import Group


class CustomUserAdminView(admin.ModelAdmin):
    class UserProfileInline(admin.StackedInline):
        model = Comment
        can_delete = False
        verbose_name_plural = 'Comments'
        extra = 0

    empty_value_display = '-empty-'
    list_display = ['id', 'username', 'email', 'phone_number', 'tg_username', 'balance', 'created_at']
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

admin.site.register(Cart)
admin.site.register(OrderItem)


@admin.register(DepositRequest)
class DepositRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'amount']
    list_filter = ['status']
    actions = ['approved_deposit', 'cancelled_deposit']

    def approved_deposit(self, request, queryset):
        count = 0
        for deposit in queryset.filter(status='pending'):
            deposit.user.balance += deposit.amount

            BalanceHistory.objects.create(
                user=deposit.user,
                amount=deposit.amount,
                type='deposit',
                description='Account deposit approved'
            )

            deposit.status = 'approved'
            deposit.user.save()
            deposit.save()

            count += 1
        self.message_user(request, f"{count} ta sorov qabul qilindi")

    def cancelled_deposit(self, request, queryset):
        count = 0
        for deposit in queryset.filter(status='pending'):
            deposit.status = 'cancelled'
            deposit.save()
            count += 1
        self.message_user(request, f"{count} ta sorov bekor qilindi")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'status']
    list_filter = ['status']
    actions = ['paid_order', 'cancelled_order']

    def paid_order(self, request, queryset):
        for order in queryset.filter(status='pending'):
            order.status = 'paid'

            if order.owner.balance >= order.total_amount:
                for item in order.items.all():
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        price=item.price,
                        qnt=item.qnt
                    )

                BalanceHistory.objects.create(
                    user=order.owner,
                    amount=order.total_amount,
                    type='out',
                    description='Order payment'
                )
                order.owner.balance -= order.total_amount
                order.owner.save()
                order.save()

            self.message_user(request, 'Qabul qilindi')
        else:
            self.message_user(request, 'Mijoz balansida yetarli mablag yoq')
            self.cancelled_order(request, queryset)

    def cancelled_order(self, request, queryset):
        for order in queryset.filter(status='pending'):
            order.status = 'cancelled'
            order.save()
        self.message_user(request, 'Bekor qilindi')