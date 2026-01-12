from django.shortcuts import render,redirect
from django.contrib.auth import logout
from .forms import *
from django.views import View
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import *
from products.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q

class SignupView(View):

    def get(self, request):
        form = SignupForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)

            if 'avatar' in request.FILES:
                user.avatar = request.FILES['avatar']

            user.save()
            messages.success(request, 'Your account is successfully created')
            return redirect('login')

        return render(request, 'registration/signup.html', {'form': form})



class ProfileView(View):
    def get(self,request,username):
        user = get_object_or_404(CustomUser, username=username)
        products = Product.objects.filter(author=user)
        return render(request, 'profile.html', {'customuser': user, 'products': products})

class UpdateProfileView(View,LoginRequiredMixin):
    login_url='login'
    def get(self,request):
        form = UpdateProfileForm(instance=request.user)
        return render(request,'profile_update.html',{'form':form})

    def post(self,request):
        form=UpdateProfileForm(instance=request.user,data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Your account is succesfully updated')
            return redirect('users:profile',request.user)
        return render(request,'update_profile',{'form':form})


class AddRemoveWishlistView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        wishlist_product = Wishlist.objects.filter(author=request.user, product=product)
        if wishlist_product:
            wishlist_product.delete()
            messages.info(request, 'Removed.')
        else:
            Wishlist.objects.create(author=request.user, product=product)
            messages.info(request, 'Wishlist.')
        return redirect(request.META.get("HTTP_REFERER"))


class WishlistView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        wishlists = Wishlist.objects.filter(author=request.user)
        q = request.GET.get('q', '').strip()
        if q:
            wishlists = wishlists.filter(product__title__icontains=q)
        return render(request, 'wishlists.html', {"wishlists": wishlists})


class RecentlyViewedView(View):
    def get(self, request):
        q = request.GET.get('q', '').strip()

        if not "recently_viewed" in request.session:
            products = Product.objects.none()
        else:
            r_viewed = request.session["recently_viewed"]
            products = Product.objects.filter(id__in=r_viewed)

        if q:
            products = products.filter(title__icontains=q)

        return render(request, "recently_viewed.html", {'products': products})


@login_required(login_url='login')
def messenger_inbox(request):
    sender = request.user

    all_chats = Chat.objects.filter(
        Q(user1=sender) | Q(user2=sender)
    ).order_by('-updated_at')

    # Reuse the same chat UI, but with no active conversation selected.
    return render(request, 'chat/chat.html', {
        'recipient': None,
        'chat': None,
        'messages': [],
        'all_chats': all_chats,
    })


@login_required(login_url='login')
def messenger(request, pk):
    recipient = get_object_or_404(CustomUser, id=pk)
    sender = request.user

    if sender == recipient:
        messages.error(request, 'You cannot message yourself')
        return redirect('users:profile', username=recipient.username)

    chat = Chat.objects.filter(
        (Q(user1=sender) & Q(user2=recipient)) |
        (Q(user1=recipient) & Q(user2=sender))
    ).first()

    if not chat:
        chat = Chat.objects.create(user1=sender, user2=recipient)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                chat=chat,
                sender=sender,
                content=content
            )
            messages.success(request, 'Message sent!')
            return redirect('users:messenger', pk=recipient.pk)
        else:
            messages.error(request, 'Message cannot be empty')

    messages_list = chat.messages.all()
    Message.objects.filter(chat=chat, is_read=False).exclude(sender=sender).update(is_read=True)
    all_chats = Chat.objects.filter(
        Q(user1=sender) | Q(user2=sender)
    ).order_by('-updated_at')

    return render(request, 'chat/chat.html', {
        'recipient': recipient,
        'chat': chat,
        'messages': messages_list,
        'all_chats': all_chats
    })


class CartView(LoginRequiredMixin, View):
    login_url = '/account/login/'
    def get(self, request):
        carts = request.user.user_cart.select_related('product')
        total = sum(cart.quantity * cart.product.price for cart in carts)
        context = {
            'carts': carts,
            'total': total
        }
        return render(request, 'cart.html', context)


class CartCreateView(LoginRequiredMixin, View):
    login_url = '/account/login/'

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(author=request.user, product=product)
        if not created:
            cart.quantity += 1
        cart.save()

        return redirect('users:cart')


class CartUpdateView(LoginRequiredMixin, View):
    login_url = '/account/login/'

    def post(self, request, cart_id):
        cart = get_object_or_404(Cart, id=cart_id, author=request.user)
        action = request.POST.get('action')

        if action == 'increase':
            cart.quantity += 1
            cart.save()

        elif action == 'decrease':
            if cart.quantity > 1:
                cart.quantity -= 1
                cart.save()
            else:
                cart.delete()
        elif action == 'delete':
            cart.delete()

        return redirect('users:cart')


class OrderCreateView(LoginRequiredMixin, View):
    login_url = '/account/login/'

    def get(self, request):
        form = OrderForm()
        carts = Cart.objects.filter(author=request.user)
        total = sum(cart.quantity * cart.product.price for cart in carts)
        return render(request, 'order_create.html', {'form': form, 'total': total})

    def post(self, request):
        form = OrderForm(request.POST)
        carts = Cart.objects.filter(author=request.user)
        if not carts.exists(): 
            messages.error(request, 'Your cart is empty.')
            return redirect('users:cart')
        
        total = sum(cart.quantity * cart.product.price for cart in carts)


        promo_code_input = request.POST.get('promocode', '').strip()
        discount = 0
        promocode = None

        if promo_code_input:
            try:
                promocode = Promocode.objects.get(code__iexact=promo_code_input)
                if promocode.is_active:
                    discount = total * Decimal(promocode.percent) / Decimal('100')
                else:
                    messages.error(request, 'Promocode is inactive or expired.')
            except Promocode.DoesNotExist:
                messages.error(request, 'Promocode does not exist.')

        total -= Decimal(discount)


        if form.is_valid():
            order = form.save(commit=False)
            if promocode and promocode.is_active:
                order.promocode = promocode
            order.owner = request.user
            order.total_amount = total
            order.status = 'pending'
            order.save()

            for cart in carts:
                OrderItem.objects.create(
                    order=order,
                    product=cart.product,
                    price=cart.product.price,
                    qnt=cart.quantity
                )
            carts.delete()
            messages.success(request, 'Order created successfully!')
            return redirect('users:my-orders')
        return render(request, 'order_create.html', {'form': form, 'total': total})
    

class OrdersView(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.filter(owner=request.user).prefetch_related('items').order_by('-id')
        return render(request, 'orders.html', {'orders': orders})



class DepositRequestView(LoginRequiredMixin, View):
    def get(self, request):
        form = DepositRequestForm()
        user_requests = DepositRequest.objects.filter(user=request.user).order_by('-id')
        context = {
            'form': form,
            'user_requests': user_requests,
            'balance': request.user.balance
        }
        return render(request, 'deposit.html', context)

    def post(self, request):
        form = DepositRequestForm(request.POST)
        if form.is_valid():
            deposit = form.save(commit=False)
            deposit.user = request.user
            deposit.status = 'pending'
            deposit.save()
            messages.success(request, 'Deposit sorovi mufovavaqiyatli yuborildi! Admin tasdiqlashini kuting')
            return redirect('users:deposit')
        user_requests = DepositRequest.objects.filter(user=request.user, status='pending')
        context = {
            'form': form,
            'user_requests': user_requests,
            'balance': request.user.balance
        }
        messages.success(request, 'Ooo nimadir xato ketdi!')
        return render(request, 'deposit.html', context)
    

class BalaceHistoryView(LoginRequiredMixin, View):
    def get(self, request):
        deposits = BalanceHistory.objects.filter(user=request.user).order_by('-id')
        return render(request, 'balance_history.html', {'deposits': deposits})