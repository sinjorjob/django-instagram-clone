from django.urls import path
from . import views


app_name ='posts'

urlpatterns = [
    path("create/", views.PostCreateView.as_view(), name="create_post"),
    path("edit/<int:pk>", views.PostEditView.as_view(), name="edit_post"),
    path("delete/<int:pk>", views.PostDeleteView.as_view(), name="delete_post"),
    path("like/<int:post_id>", views.PostLikeView.as_view(), name="like_post"),
    path("like2/<int:post_id>", views.PostLikeView2.as_view(), name="like_post2"),
    path("comment/add/<int:post_id>", views.add_comment, name="add_comment"),
    path("<int:post_id>", views.single_post, name="single_post"),
    path("comment/delete/<int:pk>", views.CommentDeleteView.as_view(), name="delete_comment"),
    path('search/', views.search_person),
]