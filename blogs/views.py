from django.http import HttpResponse, HttpResponseRedirect
from .forms import BlogForm, TagForm, CreateUserForm, CommentForm, SearchForm
from .models import Blog, Category, Comment
from django.db.models import Q, Count, Max
from django.views.generic import ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import BlogFilter
from django.core.paginator import Paginator
import datetime
from django import template

register = template.Library()

@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@method_decorator(login_required(login_url="/blogs/login"), name="dispatch")
class index(ListView):
  paginate_by = 9
  model: Blog

  def get(self, request):
    # filter = {'cat':self.request.GET.get("cat") if self.request.GET.get("cat")!=None else '', 'search': self.request.GET.get('search') if self.request.GET.get("search")!=None else '', 'page': self.request.GET.get('page') if self.request.GET.get('page')!=None else ''}
    # print(filter)
    # print(filter['search'])
    q = {
        'title__icontains':self.request.GET.get("search", "") 
    }
    lookups = {
        'category':self.request.GET.get("cat")
    }
    query = []
    if self.request.GET.get("search"): 
        query.append(Q(**q))
    if self.request.GET.get("cat"):
        query.append(Q(**lookups))
    
    
    # query = [Q(**lookups) | Q(**q)]
    # print('---------------------------------------->')
    print(query)
    # print(query.pop())
    # if lookups['category'] and lookups['search']:
    blogs = Blog.objects.filter(*query)

    print(blogs)
    # elif lookups['cat']:
    #   blogs = Blog.objects.filter(category=self.request.GET.get("cat"))

    # elif lookups['search']:
    #   blogs = Blog.objects.filter(title__icontains=filter['search'])
    # else:
    #   blogs = Blog.objects.filter()
    categories = Category.objects.all().order_by('blog')[:4]
    print(blogs, categories)
    # blog = Blog.objects.lookups(id=1)
    # blog.delete()
    # print('deleted')
    paginator = Paginator(blogs, self.paginate_by)
    page_number = self.request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(
        request,
        'home.html',
        {
            'Blogs': blogs,
            'Categories': categories,
            'page_obj':page_obj,
            'search': "&search="+self.request.GET.get("search") if self.request.GET.get("search") else "",
            'cat': "&cat="+ self.request.GET.get("cat") if self.request.GET.get("cat") else "",
            'page': "&page"+page_number if page_number else "",
            'addstr':addstr
        }
    )


@login_required(login_url="blogs/login")
def add_blog(request):

    if request.method == 'POST' or request.method == 'FILES':
        blog_form = BlogForm(request.POST, request.FILES)

        if blog_form.is_valid():
            names = blog_form.cleaned_data['category']

            getCategories = Category.objects.filter(name__in=names)
            obj = Blog.objects.create(
                title=blog_form.cleaned_data['title'],
                description=blog_form.cleaned_data['description'],
                created_date=datetime.date.today(),
                image_url=blog_form.cleaned_data['img'],
                content=blog_form.cleaned_data['content'],
                user=request.user
            )

            obj.category.set(names)
            obj.save()
            blog_form = BlogForm()
            return HttpResponseRedirect(reverse('blog-details', args=[obj.id]))

        else:
            print(blog_form.errors)

    else:
        blog_form = BlogForm()

    return render(request, 'addBlog.html', {'forms': blog_form, 'heading': 'Add New Blog'})


@login_required(login_url="blogs/login")
def add_tag(request):
    if request.method == 'POST' or request.method == 'FILES':
        category_form = TagForm(request.POST)
    
        if category_form.is_valid():
            obj = Category.objects.create(name=category_form.cleaned_data['name'])
            obj.save()
            category_form = TagForm()
            return HttpResponseRedirect(reverse('add-category'))

    else:
        category_form = TagForm()
        
    return render(request, 'addBlog.html', {'forms':category_form, 'heading':'Add New Tag'})


def register_page(request):

	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('blogs'))
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect(reverse('login'))
			

		context = {'form':form}
		return render(request, 'register.html', context)


def login_page(request):

	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('blogs'))
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return HttpResponseRedirect(reverse("blogs"))

			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'login.html', context)


def logout_user(request):
	logout(request)
	return HttpResponseRedirect(reverse("login"))



# def listBlog(request):
#     if not request.user.is_authenticated:
#         return HttpResponseRedirect("/blogs/login")
#     blog = Blog.objects.all()
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter ]
#     filterset_fields = ['id', 'title', 'description']
#     search_fields = ['id', 'title', 'description']
#     myFilter = BlogFilter(request.GET, queryset=blog)
#     blog = myFilter.qs

#     return render(request, 'listBlog.html', {'Blogs': blog, 'myFilter': myFilter})


@method_decorator(login_required(login_url="/blogs/login"), name="dispatch")
class ListBlog(ListView):
    paginate_by = 1

    def get(self, request):
        if self.request.GET.get("search"):
            query = self.request.GET.get("search")
            blogs = Blog.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
            paginator = Paginator(blogs, 1)
            search_form = SearchForm({'search': query})
        else:
            blogs = Blog.objects.filter()
            paginator = Paginator(blogs, 1)
            search_form = SearchForm({'search': ''})
        
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'listBlog.html', {'page_obj': page_obj, 'form': search_form})


# class listBlog(ListView):
#     paginate_by = 1

#     def get(self, request, id):
#         if id:
#             blogs = Blog.objects.filter(category=id)
#         else:
#             blogs = Blog.objects.filter()
#         categories = Category.objects.all().annotate(count=Count('blog'))[:4]
#         print(blogs)
#         paginator = Paginator(blogs, 1)
#         page_number = self.request.GET.get('page')
#         page_obj = paginator.get_page(page_number)

#         return render(request, 'base.html', {'categories': categories, 'Blogs': blogs, 'page_obj': page_obj})


@login_required(login_url="blogs/login")
def blog_details(request, id=1):

    blog = Blog.objects.get(id=id)
    num_comments = Comment.objects.filter(blog=blog).count()

    return render(request, 'blogDetails.html', {'blog': blog, 'num_comments': num_comments})


@login_required(login_url="blogs/login")
def add_comment(request, blog_id, id):
    blog = Blog.objects.get(id=blog_id)

    form = CommentForm(instance=blog)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=blog)

        if form.is_valid():
            name = request.user.username
            body = form.cleaned_data['comment_body']
            c = Comment(blog=blog, commenter=name, comment_body=body, date_added=datetime.date.today())
            c.save()
            return HttpResponseRedirect(reverse("blog-details", args=[blog.id]))

        else:
            print('form is invalid')    
    else:
        form = CommentForm()    


    context = {
        'form': form,
        'id': id
    }

    return render(request, 'add_comment.html', context)


@login_required(login_url="blogs/login")
def edit_comment(request, id, blog_id):
    print("id %s"%id)
    comment = Comment.objects.get(id=id)
    print("comment %s"%comment)
    form = CommentForm(instance=comment)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)

        if form.is_valid():
            name = request.user.username
            body = form.cleaned_data['comment_body']
            comment.comment_body = body
            comment.date_added = datetime.date.today()
            comment.save()
            return HttpResponseRedirect(reverse("edit-comment", args=[blog_id, id]))

        else:
            print('form is invalid')    
    else:
        form = CommentForm(instance=comment)


    context = {
        'form': form
    }

    return render(request, 'edit_comment.html', context)


@login_required(login_url="blogs/login")
def delete_comment(request, id, blog_id):
    comment = Comment.objects.filter(id=id).last()
    if comment: 
        comment.delete()
        return HttpResponseRedirect(reverse("delete-comment", args=[blog_id, id]))
    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))


class dummy(ListView):
    paginate_by = 1

    def get(self, request, id):
        if id:
            blogs = Blog.objects.filter(category=id)
        else:
            blogs = Blog.objects.filter()
        categories = Category.objects.all().annotate(count=Count('blog'))[:4]
        print(categories)
        print(blogs)
        paginator = Paginator(blogs, 1)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'base.html', {'categories': categories, 'Blogs': blogs, 'page_obj': page_obj})

@login_required(login_url="blogs/login")
def profile(request):
    user = request.user
    blogs = Blog.objects.filter(user=user)
    if blogs: 
        return render(request, 'userPage.html', {'blogs':blogs})
    return render(request, 'userPage.html')
