from django.shortcuts import render,redirect
from django.contrib.auth import logout
from .forms import SignupForm,UpdateProfileForm
from django.views import View
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import CustomUser, Wishlist, Chat, Message
from products.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q

class SignupView(View):
    def get(self,request):
        return render(request,'registration/signup.html',{'form':SignupForm})

    def post(self,request):
        form=SignupForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Your account is succesfully created ')
            return redirect('login')
        return render(request,'registration/signup.html',{'form':form})



class ProfileView(View):
    def get(self,request,username):
        user=get_object_or_404(CustomUser,username=username)
        return render(request,'profile.html',{'customuser':user})

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
        q = request.GET.get('q', '')
        if q:
            products = Product.objects.filter(title__icontains=q)
            wishlists = Wishlist.objects.filter(author=request.user, product__in=products)
        return render(request, 'wishlists.html', {"wishlists": wishlists})


class RecentlyViewedView(View):
    def get(self, request):
        if not "recently_viewed" in request.session:
            products = []
        else:
            r_viewed = request.session["recently_viewed"]
            products = Product.objects.filter(id__in=r_viewed)
            q = request.GET.get('q', '')
            if q:
                products = products.filter(title__icontains=q)
        return render(request, "recently_viewed.html", {'products': products})


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
