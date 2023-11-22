from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Blog
from django.db.models import Q


class BlogsListView(View):
    def get(self, request):
        blogs = Blog.objects.filter(Q(is_active=True))
        return render(request, 'blogs_app/blogs_list.html', {'blogs': blogs})


class BlogDetailsView(View):
    def get(self, request, *args, **kwargs):
        blogs = Blog.objects.filter(Q(is_active=True), ~Q(slug=kwargs['slug'])).order_by('-publish_date')[:6]
        blog = get_object_or_404(Blog, slug=kwargs['slug'])
        return render(request, 'blogs_app/blog_details.html',
                      {'blog': blog, 'blogs': blogs})


# _____________________________________________ last_blogs

def last_blog(request):
    blogs = Blog.objects.filter(Q(is_active=True)).order_by('-publish_date')[:9]
    return render(request, 'blogs_app/partials/last_blogs.html', {'blogs': blogs})
