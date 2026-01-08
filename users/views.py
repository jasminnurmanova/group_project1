from django.shortcuts import render,redirect
from .forms import SignupForm
from django.views import View
from django.contrib import messages


class SignupView(View):
    def get(self,request):
        return render(request,'registration/signup.html',{'form':SignupForm})

    def post(self,request):
        form=SignupForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.succes(request,'Your account is succesfully created ')
            return redirect('login')
        return render(request,'registration/signup.html',{'form':form})


