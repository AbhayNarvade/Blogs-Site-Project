from django.shortcuts import render

# Create your views here.
def create_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.POST.get('author')
        image = request.FILES.get('image')
        try:
            Blog.objects.create(title=title, content=content, author=author, image=image)
            return redirect('home')
        except Exception as e:
            print(e)
            return redirect('create_blog')
    return render(request, 'blogs/create_blog.html')