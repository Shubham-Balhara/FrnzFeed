from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import  UserCreationForm
from django.urls import reverse
from django.utils.safestring import mark_safe
import json
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .forms import ProfileForm, PostForm
from .models import Post, UserProfile, Rqst, Friend, Like, Messages, Comments



@login_required
def index(request):
	user = request.user
	friend_list = []
	for friend in user.friend_set.all():
		friend_list.append(friend.name)
	post_list = Post.objects.order_by('-date')
	query = request.GET.get('q')
	all_users = User.objects.all()
	if query:
		results = all_users.filter(Q(username__icontains=query)).distinct()
		return render(request,'feed/search_result.html',{'results':results,'friend_list':friend_list})
	return render(request,'feed/index.html',{'friend_list':friend_list,'post_list':post_list})


def signup(request):
	form = UserCreationForm()
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username,password=raw_password)
			login(request, user)
			request.method = 'GET'
			return render(request,'feed/signedup.html',{'user':user})
	return render(request,'feed/signup.html',{'form':form})

def profile(request,pk):
	user = get_object_or_404(User,pk=pk)
	post_list = user.post_set.order_by('-date')
	return render(request,'feed/profile.html',{'user':user,'post_list':post_list})

def friends(request,pk):
	user = get_object_or_404(User,pk=pk)
	users = User.objects.all()
	friends = user.friend_set.all()
	friend_list = []
	for x in friends:
		friend_list.append(x.name)
	return render(request,'feed/friends.html',{'friends':friends,'users':users,'friend_list':friend_list})

def add_profile(request,user_id):
	user = get_object_or_404(User,pk=user_id)
	form = ProfileForm(request.POST or None,request.FILES or None)
	if form.is_valid():
		profile = form.save(commit=False)
		profile.photo = request.FILES['photo']
		profile.user = user
		profile.save()
		obj = Friend.objects.create(name=request.user.username)
		obj.save()
		return redirect('profile',user_id)
	return render(request,'feed/profile_form.html',{'form':form})

def fprofile(request,name):
	user = get_object_or_404(User,username=name)
	return render(request,'feed/fprofile.html',{'user':user})


def add_post(request):
	form = PostForm(request.POST or None,request.FILES or None)
	if form.is_valid():
		post = form.save(commit=False)
		post.pic = request.FILES['pic']
		post.user = request.user
		post.save()
		return redirect(profile,request.user.id)
	return render(request,'feed/profile_form.html',{'form':form})

class UpdateStatus(UpdateView):
	model = UserProfile
	fields = ['status']
	success_url = '/' 


class UpdateUserProfile(UpdateView):
	model = UserProfile
	fields = ['photo','status','phone_no'] 
	success_url = '/'

def sent_friend(request,pk):
	user = get_object_or_404(User,pk=pk)
	obj = Rqst.objects.create(receiver=user.username,sender = request.user.username)
	obj.save()
	return render(request,'feed/request_sent.html',{})

def notify(request):
	obj = Rqst.objects.filter(receiver=request.user.username)
	return render(request,'feed/notify.html',{'obj':obj})

def confirm_yes(request,name):
	user = get_object_or_404(User,username=name)
	obj = get_object_or_404(Friend,name=request.user.username)
	obj.user.add(user)
	obj.save()
	obj = get_object_or_404(Friend,name=user.username)
	obj.user.add(request.user)
	obj.save()
	Rqst.objects.filter(sender=user.username,receiver=request.user.username).delete()
	return redirect('friends',request.user.id)

def confirm_no(request,name):
	user = get_object_or_404(User,username=name)
	Rqst.objects.filter(sender=user.username,receiver=request.user.username).delete()
	return redirect('friends',request.user.id)

def like_yes(request,pk):
	obj = get_object_or_404(Post,pk=pk)
	list = obj.like_set.all()
	for x in list:
		if x.user_id == request.user.id:
			return HttpResponseRedirect( request.GET.get('next'))
	obj1 = Like.objects.create(post=obj,user_id=request.user.id)
	obj.likes = obj.like_set.count()
	obj.save()
	return HttpResponseRedirect( request.GET.get('next'))


def remove_yes(request,name):
	user = get_object_or_404(User,username=name)
	obj = get_object_or_404(Friend,name=request.user.username)
	obj.user.remove(user)
	obj.save()
	obj = get_object_or_404(Friend,name=user.username)
	obj.user.remove(request.user)
	obj.save()
	return redirect('friends',request.user.id)

def sort_helper(elm):
	return elm.date

def chatroom(request,frnd):
	name=request.user.username
	user = get_object_or_404(User,username=frnd)
	receiver = user.username
	mymsg = Messages.objects.filter(to=receiver,frm=name)
	urmsg = Messages.objects.filter(to=name,frm=receiver)
	msgs = []
	msgs += mymsg
	msgs += urmsg
	msgs.sort(key=sort_helper,reverse=True)
	return render(request,'feed/chatroom.html',{
		'receiver':receiver,
		'name_json':mark_safe(json.dumps(name)),
		'msgs':msgs
		})

def show_post(request,pk):
	obj = get_object_or_404(Post,pk=pk)
	return render(request,'feed/show_post.html',{'obj':obj,})

def add_comment(request,pk):
	if request.POST['comment']=='':
		return redirect('index')
	post = get_object_or_404(Post,pk=pk)
	obj = Comments.objects.create(post=post,comment=request.POST['comment'],user=request.user.username)
	obj.save()
	return redirect('show_post',post.id)
