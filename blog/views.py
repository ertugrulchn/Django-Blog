from django.shortcuts import render, get_object_or_404
from blog.models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Create your views here.


def index(request):
    context = dict()
    post_list = Post.objects.all()

    query = request.GET.get('q')
    
    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(
                user__first_name__icontains=query)
        ).distinct()

    paginator = Paginator(post_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    context['posts'] = posts
    context['post_list'] = Post.objects.all()
    return render(request, 'index.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    context = {
        'post': post,

    }

    return render(request, 'detail.html', context)
