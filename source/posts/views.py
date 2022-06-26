from django.shortcuts import render
from .models import Post, PostLikes, PostComments
from accounts.models import Profile
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from django.contrib.auth.models import User
from django.views.generic import CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Post
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http import Http404
from .forms import CommentForm
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.
class PostCreateView(LoginRequiredMixin, CreateView):

    model = Post
    form_class = PostForm
    template_name = "posts/create_post.html"

    def form_valid(self, form):
        post = form.save(commit=False)
        # 投稿者のユーザ情報を取得してownerにセット
        user_profile = User.objects.get(username=self.request.user)
        post.owner = user_profile
        post.save()
        return redirect('accounts:home')


class PostEditView(LoginRequiredMixin, UpdateView):

    model = Post
    form_class =  PostForm
    template_name = "posts/edit_post.html"


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        print("self.object.owner.id=",self.object.owner.id, "request.user.id=",request.user.id)
        
        if self.object.owner.id != request.user.id:
            #raise Http404("対象データの更新権限がありません")
            #投稿者以外の削除を禁止,プロファイルページへリダイレクトさせる。
            return redirect('accounts:user_profile', username_slug=self.request.user.profile.username_slug)
        return super().get(request, *args, **kwargs)
    
        
    def form_valid(self, form):
        print("form_validが呼ばれました")
        form.save()
        messages.success(self.request, '記事が更新されました。')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounts:user_profile', kwargs={'username_slug': self.request.user.profile.username_slug})
      
 
class PostDeleteView(LoginRequiredMixin, DeleteView):

    model = Post
    template_name = 'posts/post_confirm_delete.html'


    def get(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        print("self.object.owner.id=",self.object.owner.id, "request.user.id=",request.user.id)
        #投稿者以外の削除を禁止
        if self.object.owner.id != request.user.id:
            #raise Http404("対象データの削除権限がありません")
            #投稿者以外の削除を禁止,プロファイルページへリダイレクトさせる。
            return redirect('accounts:user_profile', username_slug=self.request.user.profile.username_slug)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
    
            
    def form_valid(self, form):
        print("DeleteViewのform_validが呼ばれました")
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(self.request, '記事が削除されました。')
        print("messages=",messages)
        return HttpResponseRedirect(success_url)


    def get_success_url(self):
        return reverse_lazy('accounts:user_profile', kwargs={'username_slug': self.request.user.profile.username_slug})


class PostLikeView(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs.get('post_id'))
        liking_user_profile = Profile.objects.get(user=request.user)
        print("liking_user_profile=", liking_user_profile.user)
        is_liked_already = PostLikes.objects.filter(post=post, user=liking_user_profile.user).first()
        if is_liked_already:
            is_liked_already.delete()
            return redirect(request.META.get('HTTP_REFERER'))  #直前のページへ遷移
        post_like = PostLikes(user=liking_user_profile.user, post=post)
        post_like.save()
  
        return redirect(request.META.get('HTTP_REFERER'))  #直前のページへ遷移
    
    
class PostLikeView2(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        print("PostLikeView2のgetがよばれたよ！")
        post = Post.objects.get(pk=self.kwargs.get('post_id'))
        liking_user_profile = Profile.objects.get(user=request.user)
        #print("liking_user_profile=", liking_user_profile.user)
        is_liked_already = PostLikes.objects.filter(post=post, user=liking_user_profile.user).first()
        if is_liked_already:
            is_liked_already.delete()
            print(post.pk, "に対していいねデータを削除しました。")
            post_likes = PostLikes.objects.filter(post=post).count()
            print("いいねの数＝", post_likes)
            return JsonResponse({'post_likes': post_likes, 'status':200})
        post_like = PostLikes(user=liking_user_profile.user, post=post)
        post_like.save()
        print(post.pk, "に対していいねデータを登録しました。")
        post_likes = PostLikes.objects.filter(post=post).count()
        print("いいねの数＝", post_likes)            
        return JsonResponse({'post_likes': post_likes, 'status':200})
    
       
def add_comment(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(pk=post_id)
        current_user_profile = Profile.objects.get(user=request.user.id)
        print("add_comment_current_user_profile=", current_user_profile)
        content = request.POST["content"]
        comment = PostComments(user=current_user_profile.user, post=post, content=content)
        comment.save()
      
    return redirect('accounts:home')


def single_post(request, post_id):
    form = CommentForm()
    post = Post.objects.get(pk=post_id)
    current_user_profile = Profile.objects.get(user=request.user.id)
    comments = PostComments.objects.filter(post=post).all()
    context = {
        "post": post,
        "user_profile": current_user_profile,
        "form": form,
        "comments": comments,
    }
    return render(request, "posts/single_post.html", context)


class CommentDeleteView(LoginRequiredMixin, DeleteView):

    model = PostComments
    template_name = 'posts/comment_confirm_delete.html'


    def get(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        print("self.object.user.id=",self.object.user.id, "request.user.id=",request.user.id)
        #投稿者以外の削除を禁止
        if self.object.user.id != request.user.id:
            #raise Http404("対象データの削除権限がありません")
            #投稿者以外の削除を禁止,プロファイルページへリダイレクトさせる。
  
            comment = PostComments.objects.get(pk=self.kwargs.get('pk'))            
            return redirect('posts:single_post', post_id=comment.post.pk)
        
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
    
    def form_valid(self, form):
        print("CommentDeleteViewのform_validが呼ばれました")
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(self.request, 'コメントが削除されました。')
        print("messages=",messages)
        return HttpResponseRedirect(success_url)    

    def get_success_url(self, *args, **kwargs):
        comment = PostComments.objects.get(pk=self.kwargs.get('pk'))
        print("comment.post.pk=", comment.post.pk) 
        return reverse_lazy('posts:single_post', kwargs={'post_id': comment.post.pk})
       


def search_person(request):
    """
    ユーザーが検索ボックスに文字列を入力するたびにこの関数が実行される
    """
    name = request.GET.get("name")
    namelist = []
    print("search_person関数が実行されたよ")
    if name:
        #検索ボックスに入力された文字列を含む人名の情報をCustomersクラスからすべて取得
       
        user_objects = User.objects.filter(Q(username__icontains=name) | Q(profile__display_name__icontains=name)).distinct()
        
        print("user_objects=",user_objects)
        for user in user_objects:
            display_name = user.profile.display_name
            profile_picture = user.profile.profile_picture.url
            username_slug = user.profile.username_slug
            print("profile_picture=", profile_picture)
            namelist.append({"username": user.username, "username_slug": username_slug, "display_name": display_name + "(@" + user.username + ")", "profile_picture":profile_picture})
        
    return JsonResponse({'status':200, 'name':namelist})