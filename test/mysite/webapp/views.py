from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	)
from .forms import UserLoginForm, UserRegisterForm
#above are for login register and logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from .models import Post
from .forms import PostForm
#================================================================================================================

def index(request):
	return render(request, 'webapp/index.html', {})

def notify_success_login(request):
	return render(request, 'webapp/notify_success_login.html', {})

def notify_success_register(request):
	return render(request, 'webapp/notify_success_register.html', {})

def notify_success_create(request):
	return render(request, 'webapp/notify_success_create.html', {})

def notify_success_edit(request):
	return render(request, 'webapp/notify_success_edit.html', {})
#================================================================================================================

def postthread(request): #create
	# if request.user.is_staff or request.user.is_superuser:
	# 	raise Http404
	form = PostForm(request.POST or None, request.FILES or None)		
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		messages.success(request, "Post Successfully Created!")
		return HttpResponseRedirect(instance.get_absolute_url())
		#form.save()
	context = {
		"form" : form
	}
		#return redirect("/notify_success_create")
	return render(request, 'webapp/post_thread_view.html', context)	 

#================================================================================================================

def post_detail(request, slug=None): #retrieve read
	instance = get_object_or_404(Post, slug=slug)
	context = {
		"title": instance.title,
		"instance": instance,
	}
	return render(request, "webapp/post_detail.html", context)

#================================================================================================================
	
def viewguides(request): #list items
	queryset_list = Post.objects.all()#.order_by("-timestamp")
	#===code for search
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(title__icontains=query)
	paginator = Paginator(queryset_list, 10) # Show 25 contacts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
	    queryset = paginator.page(page)
	except PageNotAnInteger:
	    # If page is not an integer, deliver first page.
	    queryset = paginator.page(1)
	except EmptyPage:
	    # If page is out of range (e.g. 9999), deliver last page of results.
	    queryset = paginator.page(paginator.num_pages)
	context = {
		"object_list" : queryset,
		"title" : "List",
		"page_request_var": page_request_var
	}
	return render(request, 'webapp/viewguides.html', context)

#================================================================================================================
def post_update(request, slug=None):
	# if not request.user.is_authenticated or not request.user.is_superuser:
	# 	raise Http404
	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		#return redirect("/notify_success_edit")
		messages.success(request, "Post Successfully Updated!")
		return HttpResponseRedirect(instance.get_absolute_url())
		#form.save()
	context = {
		"title": instance.title,
		"instance": instance,
		"form": form,
	}
	return render(request, "webapp/post_thread_view.html", context)

#================================================================================================================

def post_delete(request, slug=None):
	# if not request.user.is_authenticated or not request.user.is_superuser:
	# 	raise Http404
	instance = get_object_or_404(Post, slug=slug)
	instance.delete()
	messages.success(request, "Post Successfully deleted!")
	return redirect("/viewguides")

	
#================================================================================================================

def login_view(request):
	print(request.user.is_authenticated())
	title = "Login"
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		login(request, user)
		return redirect("/notify_success_login")

	if request.user.is_authenticated() and request.user.is_staff:
		context = {
			"queryset": [123, 456]
		}
		
	return render(request, "webapp/login.html", {"form":form, "title":title})

#================================================================================================================

def register_view(request):
	title = "Register"
	form = UserRegisterForm(request.POST or None)

	context = {
		"form": form,
		"title": title
	}

	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()
		new_user = authenticate(username=user.username,password=password)
		login(request, user)
		return redirect("/notify_success_register")

	return render(request, "webapp/register.html", context)

#================================================================================================================

def logout_view(request):
	logout(request)
	return redirect("/login")

#================================================================================================================
# Create your views here.
