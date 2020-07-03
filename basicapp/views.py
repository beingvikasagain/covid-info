from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from basicapp.models import UserProfileInfoModel,Post,Comment
from basicapp.forms import UserProfileInfoForm,ProfileInfoForm
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.urls import reverse,reverse_lazy
from django.views.generic import (CreateView,UpdateView,DeleteView,DetailView,ListView)
from basicapp.forms import PostForm, CommentForm
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def index(request):
    return render(request,'basicapp/index.html',{})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def user_login(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user and user.is_active:
            login(request,user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponse("Login_failed!")
    return render(request,'basicapp/user_login.html',{})


def user_registration(request):
    registered = False



    if request.method=='POST':
        profile_form = ProfileInfoForm(request.POST)
        user_form = UserProfileInfoForm(request.POST)


        if profile_form.is_valid() and user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request,'basicapp/registration_error.html',{})
    else:
        profile_form = ProfileInfoForm()
        user_form = UserProfileInfoForm()



    return render(request,'basicapp/registration.html',{'user':user_form,'profile':profile_form,'registered':registered})

class PostListView(ListView):
    model = Post
    context_object_name = 'post_list'
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post
    context_object_name='post'


class PostCreateView(LoginRequiredMixin,CreateView):
    login_url="/login"
    redirect_field_name = 'basicapp/post_details.html'
    model = Post
    form_class = PostForm


    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        form.instance.author = request.user

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url='/login'
    redirect_field_name = 'basicapp/post_details.html'
    model = Post
    form_class = PostForm

class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

class DraftList(LoginRequiredMixin, ListView):
    login_url = '/login'
    redirect_field_name = 'basicapp/post_list.html'
    model = Post
    context_object_name = 'post'
    template_name = 'basicapp/post_draft_list.html'

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')



@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=post.pk)

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method=='POST':
        form =  CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post=post
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = CommentForm()
    return render(request,'basicapp/comment_form.html',{'form':form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.approve()
    return redirect('post_detail',pk=post_pk)

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    post_pk = comment.post.pk
    return redirect('post_detail',pk=post_pk)
