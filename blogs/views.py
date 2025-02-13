from django.shortcuts import render , redirect , get_object_or_404
from .models import Blog
from django.http import HttpResponse
from django.contrib.auth import authenticate, login , logout

# Create your views here.
def create_blog(request):
    if request.user.is_authenticated:  # Corrected spelling

        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            image = request.FILES.get('image')
            user = request.user
            try:
                if image:
                    Blog.objects.create(title=title, content=content, author=user, image=image)
                    return redirect('home')
                else :
                    Blog.objects.create(title=title, content=content, author=user, )
                    return redirect('home')
            except Exception as e:
                print(e)
                return redirect('create_blog')
        return render(request, 'blogs/create_blog.html')
    else :
        return redirect('loginuser')


def yourblog(request):
    if request.user.is_authenticated:
        user = request.user
        blogs = Blog.objects.filter(author= user)
        return render(request, 'accounts/home.html' , {'blogs' : blogs})

    else :
        return redirect('loginuser')
    
def blog(request ,pk) :
    if request.user.is_authenticated:

        blog_post = get_object_or_404(Blog, pk=pk)
        return render(request, 'blogs/show.html' , {'blog' : blog_post})
    else :
            return redirect('loginuser')