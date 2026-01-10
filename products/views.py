from http.client import HTTPResponse
from itertools import product
from django.http import HttpResponse

from django.shortcuts import render,redirect
from .forms import NewProductForm,ProductForm
from .models import ProductImage,Product,Comment
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def new_product(request):
    if request.method == "GET":
        form = NewProductForm
        return render (request,'product_new.html',{'form':form})

    elif request.method=="POST":
        form = NewProductForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            product=form.save(request)
            for image in request.FILES.getlist("images"):
                ProductImage.objects.create(image=image, product=product)
            messages.success(request, "Successfully Created!")
            return redirect('main:index')

        return render(request, 'product_new.html', {'form':form})

def product_detail (request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if "recently_viewed" in request.session:
        r_viewed = request.session["recently_viewed"]
        if not product.id in r_viewed:
            r_viewed.append(product.id)
            request.session.modified = True
    else:
        request.session["recently_viewed"] = [product.id, ]
    return render(request, 'product_detail.html', {'product': product})


@login_required
def product_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user==product.author:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                product = form.save()

                images = request.FILES.getlist('images')
                for img in images:
                    ProductImage.objects.create(
                        product=product,
                        image=img
                    )

                return redirect('products:detail', product.id)

        else:
            form = ProductForm(instance=product)

        return render(request, 'product_update.html', {'form': form,'product':product})

    else:
        return redirect('main:index')

@login_required
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user==product.author:
        if request.method== 'POST':
            product.delete ( )
            return redirect( 'main: index')
        return render (request, "product _delete.htm]", {'product':product})
    else:
        return redirect( 'main: index')

@login_required
def new_comment(request,product_id):
    product=get_object_or_404(Product,id=product_id)
    if request.method =="POST":
        Comment.objects.create(
            author=request.user,
            body=request.POST['body'],
            product=product,
        )
        return redirect('products:detail', product.id)
    return HttpResponse ('add comment')

@login_required
def delete_comment(request, product_id, comment_id):
    comment = get_object_or_404(Comment,id=comment_id,product_id=product_id )
    if request.user == comment.author:
        comment.delete()
    return redirect('products:detail', product_id)
