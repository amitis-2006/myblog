from django.urls import path
from . import views
from .views import PostCreateView , PostUpdateView , PostDeleteView
from django.contrib.auth import views as auth_views
#from .views import login_view
from .views import signup_view
from .views import home, post_detail,post_list , profile_view
from django.contrib.auth.views import LogoutView

app_name='blog'

urlpatterns = [
    path('', home, name='home'),
    path('index/', views.index, name='index'),
    path('postlist/', views.post_list, name='post_list'),
    path('postdetail/<slug:slug>/', views.post_detail, name='post_detail'),
    path('new/' , PostCreateView.as_view(), name='post_create'),
    path('edit/<slug:slug>/', PostUpdateView.as_view(), name='post_edit'),
    path('delete/<slug:slug>/', PostDeleteView.as_view(), name='post_delete'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', profile_view , name='profile'),
    path('post/<slug:slug>/request_publish/', views.request_publish, name='request_publish'),
    path('contact/', views.contact_us, name='contact_us'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),




]