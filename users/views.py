from django.shortcuts import render,redirect
from django.contrib.auth import logout
from .forms import SignupForm,UpdateProfileForm
from django.views import View
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin


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