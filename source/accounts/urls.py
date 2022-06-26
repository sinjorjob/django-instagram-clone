from django.urls import path
from . import views

app_name ='accounts'

urlpatterns =[
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path("home/", views.home, name="home"),
    #path("accounts/edit", views.edit_profile, name="edit_profile"),
    path("accounts/edit/<int:pk>", views.ProfileEditView.as_view(), name="edit_profile"),
    path("accounts/<str:username_slug>", views.ProfileView.as_view(), name="user_profile"),
    path("search/", views.search, name="search"),
]