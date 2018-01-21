from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post


def post_list(request):
    template_name = 'blog/post/list.html'
    posts_list = Post.published.all()
    paginator = Paginator(posts_list, 1)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {'page': page,
               'posts': posts}
    return render(request, template_name, context)


def post_detail(request, year, month, day, post):
    template_name = 'blog/post/detail.html'
    # context = {'post': post, }
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day
                             )
    return render(request, template_name, {'post': post})
    # return render(request, template_name, context)
