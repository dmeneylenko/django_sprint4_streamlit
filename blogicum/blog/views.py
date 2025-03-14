from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from blog.forms import ComentPostsForm, EditProfileForm, PostCreateForm
from blog.models import Category, ComentPosts, Post, User
from blog.utils import paginator_def
from pages.views import page_not_found


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user and not post.is_published:
            return page_not_found(request, 'Страница отсутствует')
        return super().dispatch(request, *args, kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ComentPostsForm()
        context['comments'] = (
            self.object.posts_coment.select_related('author')
        )
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'name': self.request.user})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        post_update = self.get_object()
        if request.user != post_update.author:
            return redirect('blog:post_detail', pk=post_update.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'pk': self.get_object().pk}
        )


@login_required
def delete_post(request, pk):
    instance_del_post = get_object_or_404(Post, pk=pk)
    if request.user != instance_del_post.author:
        return redirect('blog:post_detail', pk=instance_del_post.id)
    form = PostCreateForm(instance=instance_del_post)
    context = {
        'form': form,
    }
    if request.method == 'POST':
        instance_del_post.delete()
        return redirect('blog:index')
    return render(request, 'blog/create.html', context)


def index(request):
    template_name = 'blog/index.html'
    post_list = (
        Post.postfilterallobj.select_related('author', 'category', 'location')
        .order_by('-pub_date')
    ).annotate(comment_count=Count('posts_coment'))
    page_obj = paginator_def(request, post_list)
    context = {
        'page_obj': page_obj,
    }
    return render(request, template_name, context)


def category_posts(request, category_slug):
    template_name = 'blog/category.html'
    category = get_object_or_404(
        Category.objects.filter(
            is_published=True,
            slug=category_slug,
        ).only('title', 'description')
    )
    post_list = (
        Post.postfilterallobj.select_related('author', 'category', 'location')
        .filter(
            category__slug=category_slug
        ).order_by('-pub_date')
    ).annotate(comment_count=Count('posts_coment'))
    page_obj = paginator_def(request, post_list)
    context = {
        'page_obj': page_obj,
        'category': category,
    }
    return render(request, template_name, context)


def profile(request, name):
    template_name = 'blog/profile.html'
    profile_setting = get_object_or_404(User, username=name)
    if request.user.username == profile_setting.username:
        post_list_user = (
            profile_setting.posts.all().order_by('-pub_date')
        ).annotate(comment_count=Count('posts_coment'))
    else:
        post_list_user = (
            profile_setting.posts.all().filter(
                pub_date__date__lte=datetime.now(),
                is_published=True,
            ).order_by('-pub_date')
        ).annotate(comment_count=Count('posts_coment'))
    page_obj = paginator_def(request, post_list_user)
    context = {
        'page_obj': page_obj,
        'profile': profile_setting,
    }
    return render(request, template_name, context)


@login_required
def edit_profile(request):
    template_name = 'blog/user.html'
    instance = get_object_or_404(User, pk=request.user.pk)
    form = EditProfileForm(request.POST or None, instance=instance)
    context = {
        'form': form,
    }
    if form.is_valid():
        form.save()
        return redirect('blog:profile', name=request.user.username)
    return render(request, template_name, context)


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = ComentPostsForm(request.POST)
    if form.is_valid():
        comentpost = form.save(commit=False)
        comentpost.author = request.user
        comentpost.post = post
        comentpost.save()
    return redirect('blog:post_detail', pk=pk)


@login_required
def edit_comment(request, post_pk, comment_pk):
    comment_edit = get_object_or_404(ComentPosts, pk=comment_pk)
    if request.user != comment_edit.author:
        return redirect('blog:post_detail', pk=post_pk)
    form = ComentPostsForm(request.POST or None, instance=comment_edit)
    context = {
        'form': form,
        'comment': comment_edit,
    }
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', pk=post_pk)
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, post_pk, comment_pk):
    comment_delete = get_object_or_404(ComentPosts, pk=comment_pk)
    if request.user != comment_delete.author:
        return redirect('blog:post_detail', pk=post_pk)
    context = {
        'comment': comment_delete,
    }
    if request.method == 'POST':
        comment_delete.delete()
        return redirect('blog:post_detail', pk=post_pk)
    return render(request, 'blog/comment.html', context)
