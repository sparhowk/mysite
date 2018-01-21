from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from .models import Post
from .forms import EmailPostForm


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 1
    template_name = 'blog/post/list.html'


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


def post_share(request, post_id):
    # Pobranie posta na podstawie jego identyfikatora
    template_name = 'blog/post/share.html'
    post = get_object_or_404(Post, id=post_id, status='published')
    # post = Post.object.get(id=post_id)
    send = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) zachęca do przeczytania "{}"'.format(cd['name'], cd['email'], post.title)
            massage = 'Przeczytaj post "{}" na stronie {} \n\n Komentarz dodany\
                       przez {}: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, massage, 'admin@blog.com', [cd['to']])
            send = True
    else:
        form = EmailPostForm()

    context = {'post': post,
               'form': form,
               'send': send}
    return render(request, template_name, context)
