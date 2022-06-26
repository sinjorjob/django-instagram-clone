from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import(LoginView, LogoutView)
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages
from .forms import EditProfileForm
from django.views import View
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from posts.models import Post
from posts.forms import CommentForm


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'accounts/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = 'accounts/login.html'


@login_required(login_url='login')
def home(request):
    form = CommentForm()
    posts = Post.objects.order_by("-created_at").all()
    context = {
        "posts": posts,
        "form": form,
    }
    return render(request, "home/home.html", context)


class ProfileView(LoginRequiredMixin, TemplateView):
    
    template_name = "accounts/profile_page.html"

    def post(self, request, *args, **kwargs):
        print("postがよればたよ")
        user_to_follow = get_object_or_404(Profile, username_slug=self.kwargs.get('username_slug'))
        print("post_user_to_follow=", user_to_follow)
        current_user = get_object_or_404(Profile, user__username=request.user.username)
        print("post_current_user=", current_user)
        
        if current_user != user_to_follow:
            current_user_profile = request.user.profile
            if request.POST.get("follow"):
                current_user_profile.follows.add(user_to_follow)
            
            elif request.POST.get("unfollow"):
                current_user_profile.follows.remove(user_to_follow)
                current_user_profile.save()        
        else:
            print("Warningがよばれたよ")
            messages.warning(request, "このプロファイルに対して変更することはできません。")

        user_posts = Post.objects.filter(owner=user_to_follow.user).order_by("created_at").all()

        context = {
            "user_profile": user_to_follow,  #現在表示しているユーザの情報
            "posts": user_posts,  #現在表示しているユーザが投稿した記事一覧を取得
            "viewer_profile": current_user,   #現在ログオンしているユーザ情報
         }
        return render(request, "accounts/profile_page.html", context)


    def get_context_data(self, *args, **kwargs):
        print("ProfileViewのget_context_dataがよばれたよ！")

        context = super().get_context_data(**kwargs)
        
        if not hasattr(self.request.user, 'profile'):
            missing_profile = Profile(user=self.request.user)
            missing_profile.save()
            
        user_to_follow = get_object_or_404(Profile, username_slug=self.kwargs.get('username_slug'))
        print("get_context_data_user_to_follow=", user_to_follow)
        user_posts = Post.objects.filter(owner=user_to_follow.user).order_by("created_at").all()
        current_user = get_object_or_404(Profile, user__username=self.request.user.username)     
        context = {
            "user_profile": user_to_follow,  #現在表示しているユーザの情報
            "posts": user_posts,  #現在表示しているユーザが投稿した記事一覧を取得
            "viewer_profile": current_user,   #現在ログオンしているユーザ情報
         }
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):

    model = Profile
    form_class =  EditProfileForm
    template_name = "accounts/edit_profile.html"
    
    def form_valid(self, form):
        print("form_validが呼ばれました")
        form.save()
        messages.success(self.request, 'プロファイルが更新されました。')
        return super().form_valid(form)

    
    def get_success_url(self):
  
        return reverse_lazy('accounts:user_profile', kwargs={'username_slug': self.request.user.profile.username_slug})
      
    
    def get_context_data(self, **kwargs):
       print("get_context_dataがよばれたよ")
       context = super(ProfileEditView, self).get_context_data(**kwargs)
       print("self.object.username_slug=",self.object.username_slug)

       context['user_profile'] = get_object_or_404(Profile, username_slug= self.object.username_slug)
 
       return context
   

def search(request):
    if "keyword" in request.GET:
        keyword = request.GET["keyword"]
        username = keyword.split("@")[1][:-1]
        if keyword:
            users = Profile.objects.filter(user__username__icontains=username).all()
            context = {
                "users": users,
            }
            return render(request, "home/home.html", context)
    form = CommentForm()
    
   
    context = {
    
        "form": form,
    }
    return render(request, "home/home.html", context)


   