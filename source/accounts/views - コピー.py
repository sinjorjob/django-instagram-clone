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

class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'accounts/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = 'accounts/login.html'


@login_required(login_url='login')
def home(request):
    return render(request, "home/home.html")


@login_required(login_url='login')      
def profile_page(request, username_slug):
    
    #ユーザプロファイルがない場合自動作成する
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()


    if request.method == "POST":
        print("post!!")
        current_user = request.user
        user_to_follow = get_object_or_404(Profile, username_slug=username_slug)
        current_user = get_object_or_404(Profile, user__username=current_user.username)
        print("current_user_profile=", current_user, "user_profile=", user_to_follow)
        
        if current_user != user_to_follow:
            current_user_profile = request.user.profile
            if request.POST.get("follow"):
                current_user_profile.follows.add(user_to_follow)
            
            elif request.POST.get("unfollow"):
                current_user_profile.follows.remove(user_to_follow)
                current_user_profile.save()
                
        else:
            messages.warning(request, "このプロファイルに対して変更することはできません。")
            #return redirect('accounts:user_profile', username_slug)        
    
    user_to_follow = get_object_or_404(Profile, username_slug=username_slug)
    print("user_to_follow=",user_to_follow)
    context = {
            "user_profile": user_to_follow,
         }
    
    return render(request, "accounts/profile_page.html", context)


class ProfileView(LoginRequiredMixin, TemplateView):
    
    def get(self,request, username_slug):
        #ユーザプロファイルがない場合自動作成する
        print("getがよばれたよ")
        if not hasattr(request.user, 'profile'):
            missing_profile = Profile(user=self.request.user)
            missing_profile.save()
        
        user_to_follow = get_object_or_404(Profile, username_slug=username_slug)
        print("user_to_follow=",user_to_follow)
        context = {
            "user_profile": user_to_follow,
         }
        return render(request, "accounts/profile_page.html", context)
    
    
    def post(self, request, username_slug):
        print("postがよればたよ")
        
        current_user = self.request.user
        user_to_follow = get_object_or_404(Profile, username_slug=username_slug)
        current_user = get_object_or_404(Profile, user__username=current_user.username)
        print("current_user_profile=", current_user, "user_profile=", user_to_follow)
        
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

        user_to_follow = get_object_or_404(Profile, username_slug=username_slug)
        print("user_to_follow=",user_to_follow)
        context = {
            "user_profile": user_to_follow,}
        return render(request, "accounts/profile_page.html", context)


   

@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(Profile, user__username=request.user)
    print("edit_profileがよばれました", userprofile)
    if request.method == "POST":
       
        user_profile_edit_form = EditProfileForm(request.POST, instance=userprofile)
        if user_profile_edit_form.is_valid():

            user_profile_edit_form.save()
            messages.success(request, 'プロファイルが更新されました。')
            print("プロファイルが更新されました！")
            return redirect('accounts:edit_profile')
    else:
        user_profile_edit_form = EditProfileForm(instance=userprofile)

    context = {
        "form": user_profile_edit_form,
        "user_profile": userprofile,
    }

    return render(request, "accounts/edit_profile.html", context)


class ProfileEditView(LoginRequiredMixin, UpdateView):

    model = Profile
    form_class =  EditProfileForm
    template_name = "accounts/edit_profile.html"
    
    #登録処理が正常終了した場合の遷移先を指定
    #success_url = reverse_lazy('accounts:user_profile')
    
    
    def form_valid(self, form):
        print("form_validが呼ばれました")
        form.save()
        messages.success(self.request, 'プロファイルが更新されました。')
        return super().form_valid(form)

    
    def get_success_url(self):
  
        return reverse_lazy('accounts:user_profile', kwargs={'username_slug': self.request.user.profile.username_slug})
      
    
    def get_context_data(self, **kwargs):
       
       context = super(ProfileEditView, self).get_context_data(**kwargs)
       print("self.object.username_slug=",self.object.username_slug)

       context['user_profile'] = get_object_or_404(Profile, username_slug= self.object.username_slug)
 
       return context
   